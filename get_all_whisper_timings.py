import os, sys, shutil, subprocess
ffmpeg_dir = r"C:\Users\Chirag\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.1-full_build\bin"
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

import whisper
model = whisper.load_model("base")

CLIPS = [
    (2, 684, 729),
    (4, 1158, 1215),
    (5, 1345, 1373),
    (6, 1433, 1441),
    (7, 1455, 1480),
]

for cid, start, end in CLIPS:
    raw = f"reels/raw_{cid}.mp4"
    if not os.path.exists(raw):
        subprocess.run([
            sys.executable, "-m", "yt_dlp",
            "--ffmpeg-location", ffmpeg_dir,
            "--download-sections", f"*{start}-{end}",
            "-f", "bv*[height<=1080]+ba/b",
            "--merge-output-format", "mp4",
            "-o", raw, "https://www.youtube.com/live/RDhQI8-CcbM"
        ], check=True)
    
    print(f"\n=== CLIP {cid} ({start}s - {end}s) ===")
    res = model.transcribe(raw, word_timestamps=True)
    for seg in res["segments"]:
        print(f"[{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text']}")
