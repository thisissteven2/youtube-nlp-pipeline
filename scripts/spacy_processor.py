import spacy
from pypinyin import pinyin, Style

nlp = spacy.load("zh_core_web_sm")

def process_subtitle_file(vtt_file):
    with open(vtt_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    subtitles = []
    nlp_groups = []

    for i, line in enumerate(lines):
        if "-->" in line:
            time_range = line.strip()
            text = lines[i+1].strip()
            begin, end = time_range.split(" --> ")
            subtitles.append({
                "begin": i * 1000,  # placeholder timing logic
                "end": (i+1) * 1000,
                "text": text
            })
            tokens = []
            doc = nlp(text)
            for token in doc:
                py = pinyin(token.text, style=Style.TONE3, heteronym=True)
                tones = [int(s[-1]) if s[-1].isdigit() else 0 for s in py[0]]
                tokens.append({
                    "deprel": token.dep_,
                    "feats": token.morph.to_json() or None,
                    "form": {
                        "text": token.text,
                        "pinyin": py[0],
                        "tones": tones
                    },
                    "form_norm": {
                        "text": token.lemma_,
                        "pinyin": pinyin(token.lemma_, style=Style.TONE3, heteronym=True)[0],
                        "tones": tones
                    },
                    "pointer": None,
                    "pos": token.pos_,
                    "xpos": token.tag_,
                    "diocoFreq": 0,
                    "freq": None
                })
            nlp_groups.append(tokens)

    return {
        "sourceSubs": {
            "state": "ready",
            "lang_G": "zh-CN",
            "type": "source",
            "tm": {
                "isTranslatedTrack": False,
                "isTranslatable": True,
                "isFromASR": False,
                "langCode_YT": "zh",
                "langCode_G": "zh-CN",
                "md5": "md5_placeholder",
                "vssId": "vss_placeholder",
                "name": "Chinese (auto)"
            },
            "data": {
                "subsType": "vtt",
                "subs": subtitles,
                "nlp": nlp_groups,
                "haveWordFrequency": True
            }
        }
    }
