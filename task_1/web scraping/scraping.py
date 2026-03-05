import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import os
from groq import Groq

# Groq API setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None
    print("⚠️  GROQ_API_KEY not set. Email validation will be skipped.")

# Load the dataset
csv_path = "cleaned.csv"  # Make sure this file exists in the same folder as the script

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"❌ CSV file '{csv_path}' not found in current directory: {os.getcwd()}")

df = pd.read_csv(csv_path)

# 🔧 CONFIG: Change this if your URL column has a different name
URL_COLUMN = 'Website'

if URL_COLUMN not in df.columns:
    raise ValueError(f"Column '{URL_COLUMN}' not found. Available columns: {list(df.columns)}")

# Email regex pattern
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

def validate_email(email):
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

# List to store results
results = []

print(f"🔍 Starting to scrape {len(df)} URLs...\n")

for idx, row in df.iterrows():
    raw_url = row[URL_COLUMN]

    # Skip invalid/empty URLs
    if pd.isna(raw_url) or not isinstance(raw_url, str) or not raw_url.strip():
        print(f"[{idx}] no email")
        results.append({'url': raw_url, 'emails': 'no email'})
        continue

    # Normalize URL (add https:// if missing)
    url = raw_url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        print(f"[{idx}] 🌐 Scraping: {url}")
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0 (compatible; EmailBot/1.0)'})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        emails = re.findall(EMAIL_PATTERN, text)
        unique_emails = list(set(emails))  # Remove duplicates

        if unique_emails:
            valid_emails = [email for email in unique_emails if validate_email(email)]
            if valid_emails:
                email_str = ', '.join(valid_emails)
                print(f"  ✅ Found {len(valid_emails)} valid email(s): {valid_emails}")
            else:
                email_str = 'no email'
                print("  no valid email")
        else:
            email_str = 'no email'
            print("  no email")

        results.append({'url': url, 'emails': email_str})

    except Exception as e:
        print("  no email")
        results.append({'url': url, 'emails': 'no email'})

    # Be respectful: wait 1 second between requests
    time.sleep(1)

# Save all results to a new CSV
output_file = "extracted_emails.csv"
pd.DataFrame(results).to_csv(output_file, index=False)
print(f"\n✅ Done! Results saved to '{output_file}'")