from yt_dlp import YoutubeDL


def get_video_ids_from_source(source_url_or_id):
    from yt_dlp import YoutubeDL

    if not source_url_or_id.startswith("http"):
        source_url_or_id = f"https://www.youtube.com/playlist?list={source_url_or_id}"

    print(f"📥 Fetching videos from: {source_url_or_id}")

    with YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(source_url_or_id, download=False)
        entries = info.get("entries", [])
        return [entry["id"] for entry in entries if entry and entry.get("id")]
