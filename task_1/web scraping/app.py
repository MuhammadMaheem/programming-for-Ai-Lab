import os
import re
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, send_file, jsonify, Response
from werkzeug.utils import secure_filename
from groq import Groq
import uuid
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

# Global variable to store progress updates
progress_updates = []

# Groq API setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None

# Email regex pattern
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

def validate_email(email):
    """Validate email using Groq API"""
    if not client:
        return True  # Assume valid if no client
    try:
        prompt = f"Is the email address '{email}' valid and appears to be an official business email? Answer only 'valid' or 'invalid'."
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content.strip().lower()
        time.sleep(0.5)  # Rate limiting
        return answer == 'valid'
    except Exception as e:
        print(f"Error validating email {email}: {e}")
        return False

def scrape_emails_from_url(url):
    """Scrape emails from a given URL"""
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0 (compatible; EmailBot/1.0)'})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        emails = re.findall(EMAIL_PATTERN, text)
        unique_emails = list(set(emails))

        if unique_emails:
            valid_emails = [email for email in unique_emails if validate_email(email)]
            return ', '.join(valid_emails) if valid_emails else 'no email'
        return 'no email'
    except Exception as e:
        return 'no email'

def process_file(filepath, session_id):
    """Process uploaded CSV/Excel file and scrape emails"""
    global progress_updates

    # Read file
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    # Check for Website column
    if 'Website' not in df.columns:
        raise ValueError("CSV/Excel must contain a 'Website' column")

    results = []
    total = len(df)

    for idx, row in df.iterrows():
        raw_url = row['Website']

        # Send progress update
        progress_data = {
            'session_id': session_id,
            'type': 'scraping',
            'current': idx + 1,
            'total': total,
            'url': raw_url if pd.notna(raw_url) and isinstance(raw_url, str) else 'N/A'
        }
        progress_updates.append(progress_data)

        # Skip invalid/empty URLs
        if pd.isna(raw_url) or not isinstance(raw_url, str) or not raw_url.strip():
            results.append({'url': raw_url, 'emails': 'no email'})
            continue

        # Normalize URL
        url = raw_url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        print(f"[{idx+1}/{total}] Scraping: {url}")
        email_str = scrape_emails_from_url(url)
        results.append({'url': url, 'emails': email_str})

        # Be respectful: wait 1 second between requests
        time.sleep(1)

    # Send completion update
    completion_data = {
        'session_id': session_id,
        'type': 'completed',
        'total_urls': total,
        'emails_found': len([r for r in results if r['emails'] != 'no email'])
    }
    progress_updates.append(completion_data)

    return pd.DataFrame(results)

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/download-sample')
def download_sample():
    """Download sample CSV template"""
    sample_data = pd.DataFrame({
        'Website': [
            'example.com',
            'github.com',
            'stackoverflow.com'
        ]
    })

    sample_path = os.path.join(app.config['RESULTS_FOLDER'], 'sample_template.csv')
    sample_data.to_csv(sample_path, index=False)

    return send_file(sample_path, as_attachment=True, download_name='sample_template.csv')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    session_id = request.form.get('session_id', str(uuid.uuid4()))

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        return jsonify({'error': 'Only CSV and Excel files are allowed'}), 400

    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        saved_filename = f"{timestamp}_{unique_id}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
        file.save(filepath)

        # Start processing in background (for now, we'll do it synchronously with progress updates)
        result_df = process_file(filepath, session_id)

        # Save results
        result_filename = f"results_{timestamp}_{unique_id}.csv"
        result_path = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
        result_df.to_csv(result_path, index=False)

        # Clean up uploaded file
        os.remove(filepath)

        return jsonify({
            'success': True,
            'message': f'Successfully processed {len(result_df)} URLs',
            'result_file': result_filename,
            'session_id': session_id,
            'total_urls': len(result_df),
            'emails_found': len(result_df[result_df['emails'] != 'no email'])
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download-results/<filename>')
def download_results(filename):
    """Download processed results"""
    filepath = os.path.join(app.config['RESULTS_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=filename)
    return jsonify({'error': 'File not found'}), 404

@app.route('/progress/<session_id>')
def progress(session_id):
    """Server-Sent Events endpoint for progress updates"""
    def generate():
        global progress_updates
        last_index = 0

        while True:
            # Check for new updates for this session
            current_updates = [update for update in progress_updates if update.get('session_id') == session_id]

            if len(current_updates) > last_index:
                for update in current_updates[last_index:]:
                    yield f"data: {json.dumps(update)}\n\n"
                last_index = len(current_updates)

            time.sleep(0.1)  # Small delay to prevent excessive CPU usage

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    print("🚀 Starting Email Scraper Application...")
    if not GROQ_API_KEY:
        print("⚠️  GROQ_API_KEY not set. Email validation will be skipped.")
    print("📍 Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
