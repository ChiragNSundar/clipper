import re
from .config import (
    COLOR_WHITE, COLOR_YELLOW_POP, COLOR_BLACK_OUTLINE, COLOR_SHADOW,
    DEFAULT_FONT, EMOJI_FONT, DEFAULT_FONT_SIZE, DEFAULT_OUTLINE,
    DEFAULT_SHADOW, CENSOR_DICT, SLANG_CORRECTIONS
)

EMOJI_REGEX = re.compile(
    r"[\U00010000-\U0010ffff]|[\u2600-\u27ff]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\u200d\ufe0f]"
)

def censor_text(text: str) -> str:
    """Mask vulgarity with first letter, last letter, and asterisks."""
    words = text.split()
    censored = []
    for w in words:
        clean = w.strip(".,?!\"'():;~[]")
        upper = clean.upper()
        if upper in CENSOR_DICT:
            censored.append(w.replace(clean, CENSOR_DICT[upper]))
        else:
            censored.append(w)
    return " ".join(censored)

def correct_slang(text: str) -> str:
    """Apply regional and gaming slang phonetic corrections."""
    lower_text = text.lower()
    for bad, good in SLANG_CORRECTIONS.items():
        if bad in lower_text:
            # Case-insensitive replacement preserving casing if possible
            pattern = re.compile(re.escape(bad), re.IGNORECASE)
            text = pattern.sub(good, text)
    return text

def format_emoji_text(text: str) -> str:
    """Wrap emojis with fallback Segoe UI Emoji font tags for ASS."""
    def replace_emoji(match):
        emoji_char = match.group(0)
        return f"{{\\fn{EMOJI_FONT}}}{emoji_char}{{\\fn{DEFAULT_FONT}}}"
    return EMOJI_REGEX.sub(replace_emoji, text)

def format_timestamp(seconds: float) -> str:
    """Format seconds into ASS timestamp H:MM:SS.cs"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def build_ass_script(
    events: list,
    out_path: str,
    margin_v: int = 260,
    font_size: int = DEFAULT_FONT_SIZE
) -> str:
    """
    Build a complete ASS subtitle file.
    Each event in events:
        dict(start=..., end=..., text=..., highlight_idx=...) or (start, end, text)
    """
    header = f"""[Script Info]
Title: Universal Reel Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{DEFAULT_FONT},{font_size},{COLOR_WHITE},&H000000FF,{COLOR_BLACK_OUTLINE},{COLOR_SHADOW},-1,0,0,0,100,100,0,0,1,{DEFAULT_OUTLINE},{DEFAULT_SHADOW},2,40,40,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    dialogue_lines = []
    for ev in events:
        if isinstance(ev, dict):
            start = ev["start"]
            end = ev["end"]
            text = ev["text"]
            highlight = ev.get("highlight", None)
        else:
            start, end, text = ev[0], ev[1], ev[2]
            highlight = None

        text = censor_text(text)
        text = correct_slang(text)

        # Handle active word pop highlight if specified
        if highlight:
            # highlight is the active word to pop
            words = text.split()
            formatted_words = []
            for w in words:
                if highlight.upper() in w.upper():
                    formatted_words.append(f"{{\\fscx115\\fscy115\\c{COLOR_YELLOW_POP}}}{w}{{\\fscx100\\fscy100\\c{COLOR_WHITE}}}")
                else:
                    formatted_words.append(w)
            body = " ".join(formatted_words)
        else:
            # If text already contains ASS formatting, keep it, otherwise default styling
            if "\\c&H" not in text and "\\fscx" not in text:
                body = f"{{\\fscx115\\fscy115\\c{COLOR_YELLOW_POP}}}{text}{{\\fscx100\\fscy100\\c{COLOR_WHITE}}}"
            else:
                body = text

        body = format_emoji_text(body)
        start_ts = format_timestamp(start)
        end_ts = format_timestamp(end)
        dialogue_lines.append(f"Dialogue: 0,{start_ts},{end_ts},Default,,0,0,{margin_v},,{body}")

    full_content = header + "\n".join(dialogue_lines) + "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    return out_path
