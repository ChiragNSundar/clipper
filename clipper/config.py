import os
import shutil

# FFmpeg Configuration
GYAN_FFMPEG_DIR = r"C:\Users\Chirag\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.1-full_build\bin"
if os.path.exists(GYAN_FFMPEG_DIR):
    os.environ["PATH"] = GYAN_FFMPEG_DIR + os.pathsep + os.environ.get("PATH", "")

FFMPEG = os.path.join(GYAN_FFMPEG_DIR, "ffmpeg.exe") if os.path.exists(GYAN_FFMPEG_DIR) else (shutil.which("ffmpeg") or "ffmpeg")
FFPROBE = os.path.join(GYAN_FFMPEG_DIR, "ffprobe.exe") if os.path.exists(GYAN_FFMPEG_DIR) else (shutil.which("ffprobe") or "ffprobe")

# Canvas Dimensions
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1920

# Colors (ASS format &H00BBGGRR&)
COLOR_WHITE = "&H00FFFFFF&"
COLOR_YELLOW_POP = "&H002EFFFF&"
COLOR_CYAN_POP = "&H00FFFF00&"
COLOR_BLACK_OUTLINE = "&H00000000&"
COLOR_SHADOW = "&H80000000&"

# Font Settings
DEFAULT_FONT = "Impact"
EMOJI_FONT = "Segoe UI Emoji"
DEFAULT_FONT_SIZE = 74
DEFAULT_OUTLINE = 8
DEFAULT_SHADOW = 3

# Directory for sticker images
STICKERS_DIR = "stickers"

def resolve_sticker_path(name: str) -> str:
    """Resolve sticker name or path to an absolute/relative path within stickers/."""
    if not name:
        return None
    candidates = [
        name,
        os.path.join(STICKERS_DIR, name),
        os.path.join(STICKERS_DIR, f"{name}.png"),
        os.path.join(STICKERS_DIR, f"{name}_sticker.png")
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return name

# Vulgarity / Censorship Filter
CENSOR_DICT = {
    "NIGGA": "N***A",
    "NIGGER": "N***A",
    "FUCK": "F**K",
    "FUCKING": "F*****G",
    "FUCKED": "F***ED",
    "DICK": "D**K",
    "SHIT": "S**T",
    "BITCH": "B***H",
    "RETARDED": "R******D",
    "CUNT": "C**T",
}

# Regional Slang & Phonetic Auto-Correction Glossary
# Standard Whisper phonetic mishearings -> Regional/Gaming context
SLANG_CORRECTIONS = {
    "mute made": "mute mado",
    "4 mutes": "mute mado",
    "be muted": "mute mado",
    "raised": "Raze",
    "into your mouth": "into your mom",
    "in your mouth": "in your mom",
    "cowed": "KO'd",
    "carr": "car",
    "chappri": "chappar",
    "bul bul": "Bulbul",
    "mathad kilva": "mathadakkilva",
    "mathadkilva": "mathadakkilva",
    "mathadkiva": "mathadakkilva",
    "olle hudga": "olle hudga",
    "nodak chandag": "nodak chandag",
    "preethi madak": "preethi madak"
}

# Regional vocabulary initial prompt for Whisper
WHISPER_REGIONAL_PROMPT = (
    "Kannada, Kanglish, Hinglish, gaming slang. "
    "Mute mado, chappar, gothaa, anthe, sumne iri, maga, macha, bro, da. "
    "Valorant, Raze, ults, lock-in, clutch. "
    "Bulbul mathadakkilva, naa olle hudga alva, naa nodak chandag ilva, nan preethi madak ilva."
)
