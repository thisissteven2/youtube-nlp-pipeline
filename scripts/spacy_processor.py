import spacy
from pypinyin import pinyin, Style
from konlpy.tag import Okt


# Map langCode_G to spaCy model names
LANG_MODEL_MAP = {
    "zh-CN": "zh_core_web_sm",
    "zh-TW": "zh_core_web_sm",
    "ja": "ja_core_news_sm",
    "ko": None,
    "es": "es_core_news_sm"
}


def get_nlp(lang_code):
    if lang_code == "ko":
        return Okt()
    else:
        model_name = LANG_MODEL_MAP.get(lang_code)
        if model_name:
            return spacy.load(model_name)
        raise ValueError(f"Unsupported language code: {lang_code}")


def process_subtitle_file(vtt_file, lang_code):
    nlp = get_nlp(lang_code)
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

            if lang_code == "ko":
                for word, pos in nlp.pos(text):
                    tokens.append({
                        "deprel": None,
                        "feats": None,
                        "form": {
                            "text": word,
                            "pinyin": [""],
                            "tones": []
                        },
                        "form_norm": {
                            "text": word,
                            "pinyin": [""],
                            "tones": []
                        },
                        "pointer": None,
                        "pos": pos,
                        "xpos": pos,
                        "diocoFreq": 0,
                        "freq": None
                    })
            else:
                doc = nlp(text)
                for token in doc:
                    if lang_code.startswith("zh"):
                        py = pinyin(token.text, style=Style.TONE3,
                                    heteronym=True)
                        tones = [int(s[-1]) if s[-1].isdigit()
                                 else 0 for s in py[0]]
                    else:
                        py = [""]
                        tones = []
                    tokens.append({
                        "deprel": token.dep_,
                        "feats": token.morph.to_json() or None,
                        "form": {
                            "text": token.text,
                            "pinyin": py[0],
                            "tones": tones
                        },
                        "form": {
                            "text": token.text,
                            "pinyin": py[0],
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
