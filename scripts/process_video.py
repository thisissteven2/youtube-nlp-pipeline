import subprocess
import os
import json
from scripts.spacy_processor import process_subtitle_file

def process_video(video_id):
    subtitle_path = f"{video_id}.en.vtt"
    if not os.path.exists(subtitle_path):
        subprocess.run([
            "yt-dlp",
            "--write-auto-sub", "--sub-lang", "en",
            "--skip-download",
            "-o", f"{video_id}.%(ext)s",
            f"https://www.youtube.com/watch?v={video_id}"
        ], check=True)

    return process_subtitle_file(subtitle_path)
