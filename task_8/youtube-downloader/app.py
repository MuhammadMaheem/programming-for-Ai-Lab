import os
import json
import re
import subprocess
import threading
import time
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, send_file, Response
import yt_dlp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Store progress per download ID with timestamp for cleanup
progress_store = {}
progress_store_lock = threading.Lock()
CLEANUP_TIMEOUT = 3600  # 1 hour in seconds


def cleanup_progress_store():
    """Remove old progress entries to prevent memory leaks."""
    with progress_store_lock:
        now = time.time()
        expired_keys = [
            key for key, data in progress_store.items()
            if now - data.get('timestamp', now) > CLEANUP_TIMEOUT
        ]
        for key in expired_keys:
            del progress_store[key]
            logger.info(f"Cleaned up progress entry: {key}")


def start_cleanup_thread():
    """Start background thread to periodically cleanup old progress entries."""
    def cleanup_loop():
        while True:
            time.sleep(600)  # Run cleanup every 10 minutes
            cleanup_progress_store()
    
    thread = threading.Thread(target=cleanup_loop)
    thread.daemon = True
    thread.start()
    logger.info("Progress store cleanup thread started")


def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/fetch-info", methods=["POST"])
def fetch_info():
    data = request.json
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        logger.info(f"Fetching info for URL: {url}")
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            logger.info(f"Successfully fetched info for: {info.get('title', 'Unknown')}")

        formats = info.get("formats", [])

        # Collect video+audio combined formats and video-only formats
        result_formats = []
        seen = set()

        # Best combined (progressive) formats
        for f in formats:
            vcodec = f.get("vcodec", "none")
            acodec = f.get("acodec", "none")
            height = f.get("height")
            ext = f.get("ext", "")
            fps = f.get("fps")

            if vcodec != "none" and acodec != "none" and height:
                key = (height, ext)
                if key not in seen:
                    seen.add(key)
                    label = f"{height}p"
                    if fps and fps > 30:
                        label += f" {int(fps)}fps"
                    label += f" · {ext.upper()} · Video+Audio"
                    result_formats.append({
                        "format_id": f["format_id"],
                        "label": label,
                        "height": height,
                        "ext": ext,
                        "type": "combined",
                        "fps": fps,
                        "filesize": f.get("filesize") or f.get("filesize_approx"),
                    })

        # Video-only formats (will be merged with best audio)
        for f in formats:
            vcodec = f.get("vcodec", "none")
            acodec = f.get("acodec", "none")
            height = f.get("height")
            ext = f.get("ext", "")
            fps = f.get("fps")

            if vcodec != "none" and acodec == "none" and height:
                key = (height, ext, "vo")
                if key not in seen:
                    seen.add(key)
                    label = f"{height}p"
                    if fps and fps > 30:
                        label += f" {int(fps)}fps"
                    label += f" · {ext.upper()} · Best Audio (merged)"
                    result_formats.append({
                        "format_id": f["format_id"] + "+bestaudio",
                        "label": label,
                        "height": height,
                        "ext": "mp4",
                        "type": "video_only",
                        "fps": fps,
                        "filesize": f.get("filesize") or f.get("filesize_approx"),
                    })

        # Audio-only
        audio_formats = []
        for f in formats:
            vcodec = f.get("vcodec", "none")
            acodec = f.get("acodec", "none")
            abr = f.get("abr")
            ext = f.get("ext", "")

            if vcodec == "none" and acodec != "none" and abr:
                audio_formats.append({
                    "format_id": f["format_id"],
                    "label": f"Audio · {int(abr)}kbps · {ext.upper()}",
                    "height": 0,
                    "ext": ext,
                    "type": "audio",
                    "abr": abr,
                    "filesize": f.get("filesize") or f.get("filesize_approx"),
                })

        # Deduplicate audio by abr+ext
        seen_audio = set()
        for af in audio_formats:
            key = (round(af["abr"]), af["ext"])
            if key not in seen_audio:
                seen_audio.add(key)
                result_formats.append(af)

        # Sort: combined & video_only desc by height, then audio desc by abr
        result_formats.sort(key=lambda x: (
            0 if x["type"] == "audio" else 1,
            -(x.get("height") or 0),
            -(x.get("fps") or 0),
        ), reverse=False)

        # Re-sort properly
        video_fmts = sorted(
            [f for f in result_formats if f["type"] != "audio"],
            key=lambda x: (-(x.get("height") or 0), -(x.get("fps") or 0))
        )
        audio_fmts = sorted(
            [f for f in result_formats if f["type"] == "audio"],
            key=lambda x: -(x.get("abr") or 0)
        )
        result_formats = video_fmts + audio_fmts

        thumbnail = info.get("thumbnail", "")
        # Prefer a smaller thumbnail
        thumbs = info.get("thumbnails", [])
        if thumbs:
            for t in reversed(thumbs):
                if t.get("url"):
                    thumbnail = t["url"]
                    break

        return jsonify({
            "title": info.get("title", "Unknown"),
            "channel": info.get("uploader", ""),
            "duration": info.get("duration"),
            "thumbnail": thumbnail,
            "formats": result_formats,
        })

    except Exception as e:
        logger.error(f"Error fetching video info: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/download", methods=["POST"])
def download_video():
    data = request.json
    url = data.get("url", "").strip()
    format_id = data.get("format_id", "bestvideo+bestaudio")
    title = sanitize_filename(data.get("title", "video"))
    ext = data.get("ext", "mp4")
    download_id = data.get("download_id", str(time.time()))

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    logger.info(f"Starting download {download_id} - Format: {format_id}")
    with progress_store_lock:
        progress_store[download_id] = {
            "status": "starting",
            "percent": 0,
            "speed": "",
            "eta": "",
            "timestamp": time.time()
        }

    output_template = os.path.join(DOWNLOAD_DIR, f"{title}.%(ext)s")

    def progress_hook(d):
        with progress_store_lock:
            if d["status"] == "downloading":
                percent_str = d.get("_percent_str", "0%").strip().replace("%", "")
                try:
                    percent = float(percent_str)
                except:
                    percent = 0
                progress_store[download_id] = {
                    "status": "downloading",
                    "percent": percent,
                    "speed": d.get("_speed_str", "").strip(),
                    "eta": d.get("_eta_str", "").strip(),
                    "filename": d.get("filename", ""),
                    "timestamp": time.time(),
                }
            elif d["status"] == "finished":
                progress_store[download_id] = {
                    "status": "processing",
                    "percent": 100,
                    "speed": "",
                    "eta": "",
                    "filename": d.get("filename", ""),
                    "timestamp": time.time(),
                }

    def run_download():
        try:
            logger.info(f"Download {download_id} starting for {title}")
            ydl_opts = {
                "format": format_id,
                "outtmpl": output_template,
                "progress_hooks": [progress_hook],
                "merge_output_format": "mp4" if ext == "mp4" else ext,
                "quiet": True,
                "no_warnings": True,
                "postprocessors": [],
            }
            if "+" in format_id or ext == "mp4":
                ydl_opts["merge_output_format"] = "mp4"

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                final_filename = ydl.prepare_filename(info)
                # Normalize extension
                base = os.path.splitext(final_filename)[0]
                for candidate in [final_filename, base + ".mp4", base + ".mkv", base + ".webm", base + ".mp3", base + ".m4a"]:
                    if os.path.exists(candidate):
                        final_filename = candidate
                        break

            with progress_store_lock:
                progress_store[download_id] = {
                    "status": "done",
                    "percent": 100,
                    "filename": final_filename,
                    "timestamp": time.time(),
                }
            logger.info(f"Download {download_id} completed successfully")
        except Exception as e:
            logger.error(f"Download {download_id} failed: {str(e)}")
            with progress_store_lock:
                progress_store[download_id] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": time.time(),
                }

    thread = threading.Thread(target=run_download)
    thread.daemon = True
    thread.start()

    return jsonify({"download_id": download_id})


@app.route("/api/progress/<download_id>")
def get_progress(download_id):
    with progress_store_lock:
        return jsonify(progress_store.get(download_id, {"status": "unknown"}))


@app.route("/api/get-file/<download_id>")
def get_file(download_id):
    info = progress_store.get(download_id, {})
    filename = info.get("filename", "")
    if not filename or not os.path.exists(filename):
        return jsonify({"error": "File not found"}), 404
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    # Start cleanup thread
    start_cleanup_thread()
    logger.info("Starting YouTube Downloader Flask app")
    # Bind to 0.0.0.0 for Heroku/cloud deployment, disable debug for production
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
