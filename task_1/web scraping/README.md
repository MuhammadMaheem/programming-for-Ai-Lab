# Email Scraper Pro - Flask Web Application

A professional Flask-based web application for extracting email addresses from websites.

## Features

- 📤 Upload CSV/Excel files with website URLs
- 📥 Download sample template with correct format
- 🔍 Automated email extraction from websites
- ✅ AI-powered email validation using Groq API
- 💾 Download results in CSV format
- 🎨 Beautiful, professional UI with modern design
- 📱 Responsive design for all devices

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Set up your Groq API key (optional, for email validation):
```bash
export GROQ_API_KEY="your_api_key_here"
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Follow these steps:
   - Download the sample CSV template
   - Add your website URLs to the 'Website' column
   - Upload your CSV/Excel file
   - Wait for processing to complete
   - Download the results

## File Format

Your CSV/Excel file must contain a column named `Website` with URLs:

```csv
Website
example.com
github.com
stackoverflow.com
```

## API Endpoints

- `GET /` - Home page
- `GET /download-sample` - Download sample CSV template
- `POST /upload` - Upload and process file
- `GET /download-results/<filename>` - Download results

## Configuration

- Maximum file size: 16MB
- Supported formats: CSV, XLSX, XLS
- Rate limiting: 1 second between requests
- Email validation: Optional (requires Groq API key)

## Project Structure

```
.
├── app.py                  # Main Flask application
├── templates/
│   └── index.html          # Frontend HTML with CSS
├── uploads/                # Temporary upload storage (auto-created)
├── results/                # Processed results storage (auto-created)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Notes

- The application respects rate limiting (1 second between requests)
- If GROQ_API_KEY is not set, email validation will be skipped
- All uploaded files are automatically deleted after processing
- Results are stored in the `results/` folder

## License

This project is for educational purposes.
