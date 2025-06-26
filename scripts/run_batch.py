import os
import json
from scripts.fetch_playlist import get_video_ids_from_playlist
from scripts.process_video import process_video

DATA_DIR = "data/processed"
PROCESSED_LIST_FILE = "data/processed_videos.json"
PLAYLIST_ID = "YOUR_PLAYLIST_ID"

os.makedirs(DATA_DIR, exist_ok=True)

# Load already processed videos
if os.path.exists(PROCESSED_LIST_FILE):
    with open(PROCESSED_LIST_FILE, "r") as f:
        processed_ids = set(json.load(f))
else:
    processed_ids = set()

video_ids = get_video_ids_from_playlist(PLAYLIST_ID)

for vid in video_ids:
    if vid not in processed_ids:
        print(f"Processing {vid}")
        result = process_video(vid)
        with open(os.path.join(DATA_DIR, f"{vid}.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        processed_ids.add(vid)
    else:
        print(f"Skipping {vid}, already processed")

# Save updated processed IDs
with open(PROCESSED_LIST_FILE, "w") as f:
    json.dump(list(processed_ids), f)
