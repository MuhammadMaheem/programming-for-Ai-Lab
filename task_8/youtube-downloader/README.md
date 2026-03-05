# YT Downloader

A slick Flask-based YouTube downloader powered by yt-dlp.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

You'll also need `ffmpeg` for merging video+audio streams:

- **macOS**: `brew install ffmpeg`
- **Ubuntu/Debian**: `sudo apt install ffmpeg`
- **Windows**: Download from https://ffmpeg.org/download.html and add to PATH

### 2. Run the app

```bash
python app.py
```

### 3. Open in browser

Visit: http://localhost:5000

---

## Usage

1. Paste a YouTube URL into the input
2. Click **Fetch** — video info and all available formats will load
3. Select your preferred format/resolution from the list
4. Click **Download** and watch the progress bar
5. Click **Save File** when done to save it to your computer

Downloaded files are saved to the `downloads/` folder next to `app.py`.

## Features

- **Format tabs**: Filter by Video, Audio-only, or All
- **Live progress**: Real-time download speed + ETA
- **Merged formats**: High-quality video-only streams are automatically merged with best audio via ffmpeg
- **Clean UI**: Dark, minimal interface

## Notes

- For personal use only — respect copyright laws and YouTube's Terms of Service
- The `downloads/` folder is created automatically on first run
