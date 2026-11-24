import os
import subprocess
from .config import FFMPEG, WHISPER_REGIONAL_PROMPT
from .subtitles import correct_slang, censor_text

def extract_audio(video_path: str, audio_path: str) -> str:
    """Extract 16kHz mono audio from video file."""
    cmd = [
        FFMPEG, "-y",
        "-i", video_path,
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return audio_path

def transcribe_audio(
    audio_path: str,
    model_name: str = "base",
    initial_prompt: str = WHISPER_REGIONAL_PROMPT,
    word_timestamps: bool = True
) -> list:
    """
    Transcribe audio with regional vocabulary awareness.
    Returns list of dicts: [dict(start=..., end=..., text=..., words=[...])]
    """
    import whisper

    model = whisper.load_model(model_name)
    result = model.transcribe(
        audio_path,
        word_timestamps=word_timestamps,
        initial_prompt=initial_prompt,
        no_speech_threshold=0.15,
        temperature=0.0
    )

    chunks = []
    # If word timestamps are present, chunk into 1-2 words per card
    for seg in result.get("segments", []):
        words = seg.get("words", [])
        if words:
            # Group into 1-2 words per card
            i = 0
            while i < len(words):
                # Take 1 or 2 words
                take = 2 if (i + 1 < len(words)) else 1
                group = words[i : i + take]
                start_t = group[0]["start"]
                end_t = group[-1]["end"]
                group_text = " ".join(w["word"].strip() for w in group)
                group_text = correct_slang(group_text)
                group_text = censor_text(group_text)
                if group_text:
                    chunks.append({
                        "start": start_t,
                        "end": end_t,
                        "text": group_text,
                        "highlight": group[0]["word"].strip()
                    })
                i += take
        else:
            text = correct_slang(seg["text"].strip())
            text = censor_text(text)
            if text:
                chunks.append({
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": text,
                    "highlight": None
                })

    return chunks
