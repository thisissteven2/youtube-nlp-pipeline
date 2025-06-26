from yt_dlp import YoutubeDL

def get_video_ids_from_playlist(playlist_url_or_id):
    ydl_opts = {'extract_flat': True, 'quiet': True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/playlist?list={playlist_url_or_id}", download=False)
        return [entry['id'] for entry in info['entries']]
