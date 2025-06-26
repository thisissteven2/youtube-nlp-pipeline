# YouTube Subtitle NLP Pipeline

Automated weekly subtitle + NLP processing using GitHub Actions.

Get inside python virtual environment:

```bash
pip -m venv venv
.\venv\Scripts\activate
```

Install requirements:

```bash
pip install -r requirements.txt
python -m spacy download zh_core_web_sm
python -m spacy download ja_core_news_sm
python -m spacy download es_core_news_sm
```

Fetch listed channels inside `channels.txt`:

```bash
fetch_channels.bat
```

Intended workflow:

- edit `channels.txt`, run `update.sh`, push updated folders/files to github repo.
- each row of `channels.txt` looks like `CHANNEL_URL LANG_CODE`, ex: `https://www.youtube.com/@xnzxnz zh-CN`

Code Needed:

- read `channels.txt` and fetch all video urls containing subtitles under that playlist, write it into `data/ids/{CHANNEL_NAME}.txt`
- for every video urls of `data/ids/{CHANNEL_NAME}.txt`, if it isn't inside `data/processed_ids/{CHANNEL_NAME}.txt`, process the video:

  - get subtitles of the video (lang_code and english), save it in `data/subtitles/{VIDEO_ID}` folder.
  - every processed video should be inside `data/processed_ids/{CHANNEL_NAME}.txt`

- done.
