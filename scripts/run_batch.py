import os
import json
from scripts.fetch_playlist import get_video_ids_from_source
from scripts.process_video import process_video

DATA_DIR = "data/processed"
PROCESSED_MAP_FILE = "data/processed_by_channel.json"

LANG_PER_PLAYLIST = {
    "https://www.youtube.com/@xnzxnz": "zh-CN",
    # "https://www.youtube.com/@anotherchannel": "zh-TW",
    # "https://www.youtube.com/@anotherchannel": "ja",
    # "https://www.youtube.com/@anotherchannel": "ko",
    # "https://www.youtube.com/@anotherchannel": "es"
}

os.makedirs(DATA_DIR, exist_ok=True)

# Load processed IDs per channel
if os.path.exists(PROCESSED_MAP_FILE):
    with open(PROCESSED_MAP_FILE, "r", encoding="utf-8") as f:
        processed_by_channel = json.load(f)
else:
    processed_by_channel = {}

MAX_INITIAL_VIDEOS = 30

for playlist_url, lang_code in LANG_PER_PLAYLIST.items():
    print(f"\n🔍 Fetching videos from: {playlist_url} ({lang_code})")
    video_ids = get_video_ids_from_source(playlist_url)

    # Initialize per-channel set
    already_processed = set(processed_by_channel.get(playlist_url, []))

    # Limit to 30 on channel's first run
    is_first_time_for_channel = len(already_processed) == 0
    if is_first_time_for_channel:
        video_ids = video_ids[:MAX_INITIAL_VIDEOS]

    for vid in video_ids:
        if vid not in already_processed:
            print(f"📼 Processing {vid}")
            try:
                # result = process_video(vid, lang_code=lang_code)
                result = []
                out_path = os.path.join(DATA_DIR, f"{vid}.json")
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)

                already_processed.add(vid)
            except Exception as e:
                print(f"❌ Failed to process {vid}: {e}")
        else:
            print(f"✅ Skipping {vid}, already processed")

    # Save updated processed list for this channel
    processed_by_channel[playlist_url] = list(already_processed)

# Save map to disk
with open(PROCESSED_MAP_FILE, "w", encoding="utf-8") as f:
    json.dump(processed_by_channel, f, ensure_ascii=False, indent=2)

print("\n🏁 Done.")
