# YouTube Subtitle NLP Pipeline

Automated weekly subtitle + NLP processing using GitHub Actions.

```bash
python -m venv venv
source venv/bin/activate  # or .\\venv\\Scripts\\activate on Windows
pip install -r requirements.txt
python -m spacy download zh_core_web_sm
python -m spacy download ja_core_news_sm
python -m spacy download es_core_news_sm
```

Run:

```bash
python run_batch.py
```
