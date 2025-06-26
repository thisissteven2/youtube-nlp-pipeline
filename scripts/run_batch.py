import os
import json
from scripts.fetch_playlist import get_video_ids_from_playlist
from scripts.process_video import process_video

DATA_DIR = "data/processed"
PROCESSED_LIST_FILE = "data/processed_videos.json"

# Playlist ID → language code (YouTube-style)
LANG_PER_PLAYLIST = {
    "ZH_SIMPLIFIED_PLAYLIST_ID": "zh-CN",
    "ZH_TRADITIONAL_PLAYLIST_ID": "zh-TW",
    "JAPANESE_PLAYLIST_ID": "ja",
    "KOREAN_PLAYLIST_ID": "ko",
    "SPANISH_PLAYLIST_ID": "es"
}

os.makedirs(DATA_DIR, exist_ok=True)

# Load already processed videos
if os.path.exists(PROCESSED_LIST_FILE):
    with open(PROCESSED_LIST_FILE, "r") as f:
        processed_ids = set(json.load(f))
else:
    processed_ids = set()

for playlist_id, lang_code in LANG_PER_PLAYLIST.items():
    print(f"\n🔍 Fetching videos for playlist: {playlist_id} ({lang_code})")
    video_ids = get_video_ids_from_playlist(playlist_id)

    for vid in video_ids:
        if vid not in processed_ids:
            print(f"📼 Processing {vid}")
            try:
                result = process_video(vid, lang_code=lang_code)
                out_path = os.path.join(DATA_DIR, f"{vid}.json")
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                processed_ids.add(vid)
            except Exception as e:
                print(f"❌ Failed to process {vid}: {e}")
        else:
            print(f"✅ Skipping {vid}, already processed")

# Save updated processed IDs
with open(PROCESSED_LIST_FILE, "w") as f:
    json.dump(list(processed_ids), f)

print("\n🏁 Done.")
