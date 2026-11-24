"""
Universal Clipper Engine for Instagram Reels & TikTok Shorts.
Built with regional slang accuracy, acoustic micro-chunking, and hang-proof FFmpeg pipelines.
"""

from .config import FFMPEG, FFPROBE, CANVAS_WIDTH, CANVAS_HEIGHT, CENSOR_DICT, SLANG_CORRECTIONS
from .subtitles import build_ass_script, censor_text, correct_slang
from .transcribe import extract_audio, transcribe_audio
from .layouts import create_banner_and_sticker_template
from .engine import render_reel, probe_video

__all__ = [
    "FFMPEG",
    "FFPROBE",
    "CANVAS_WIDTH",
    "CANVAS_HEIGHT",
    "CENSOR_DICT",
    "SLANG_CORRECTIONS",
    "build_ass_script",
    "censor_text",
    "correct_slang",
    "extract_audio",
    "transcribe_audio",
    "create_banner_and_sticker_template",
    "render_reel",
    "probe_video"
]
