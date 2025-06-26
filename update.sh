#!/bin/bash
set -e

CHANNELS_FILE="channels.txt"
ID_DIR="data/ids"
PROCESSED_DIR="data/processed_ids"
SUBTITLE_DIR="data/subtitles"

mkdir -p "$ID_DIR" "$PROCESSED_DIR" "$SUBTITLE_DIR"

echo "📄 Reading $CHANNELS_FILE..."

while read -r CHANNEL_URL LANG_CODE; do
    echo "🔍 Processing: $CHANNEL_URL [$LANG_CODE]"

    # Extract channel name (used for filenames)
    CHANNEL_NAME=$(basename "$CHANNEL_URL")
    ID_FILE="$ID_DIR/${CHANNEL_NAME}.txt"
    PROCESSED_FILE="$PROCESSED_DIR/${CHANNEL_NAME}.txt"
    touch "$ID_FILE" "$PROCESSED_FILE"

    echo "⏬ Fetching videos with subtitles..."
    yt-dlp --skip-download \
           --write-subs --write-auto-sub \
           --sub-lang "$LANG_CODE,en" \
           --match-filter "subtitles" \
           --flat-playlist \
           --print "%(webpage_url)s" \
           "$CHANNEL_URL" > "$ID_FILE.tmp"

    # Filter duplicates and save
    sort -u "$ID_FILE.tmp" > "$ID_FILE"
    rm "$ID_FILE.tmp"

    echo "✅ Saved URLs to $ID_FILE"

    while read -r VIDEO_URL; do
        VIDEO_ID=$(yt-dlp --get-id "$VIDEO_URL")

        if grep -q "$VIDEO_URL" "$PROCESSED_FILE"; then
            echo "🔁 Already processed: $VIDEO_ID"
            continue
        fi

        echo "📥 Downloading subtitles for $VIDEO_ID..."

        # Save subs to temp folder
        yt-dlp --skip-download \
               --write-subs --write-auto-sub \
               --sub-lang "$LANG_CODE,en" \
               --convert-subs srt \
               --output "${SUBTITLE_DIR}/${VIDEO_ID}/%(language)s.%(ext)s" \
               "$VIDEO_URL"

        echo "$VIDEO_URL" >> "$PROCESSED_FILE"
        echo "✅ Done: $VIDEO_ID"

    done < "$ID_FILE"

    echo "🚀 Finished channel: $CHANNEL_NAME"

done < "$CHANNELS_FILE"
