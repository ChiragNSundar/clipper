import os, sys
ffmpeg_dir = r"C:\Users\Chirag\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.1-full_build\bin"
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

import whisper
model = whisper.load_model("small")

print("\n=== TRANSCRIBING PART A (0:23 - 0:35) ===")
res_a = model.transcribe("part_a.mp4", word_timestamps=True)
print("Text A:", res_a["text"])
for seg in res_a["segments"]:
    print(f"[{seg['start']:.2f} - {seg['end']:.2f}] {seg['text']}")
    for w in seg.get("words", []):
        print(f"   {w['start']:.2f} - {w['end']:.2f}: {w['word']}")

print("\n=== TRANSCRIBING PART B (0:56 - 1:19) ===")
res_b = model.transcribe("part_b.mp4", word_timestamps=True)
print("Text B:", res_b["text"])
for seg in res_b["segments"]:
    print(f"[{seg['start']:.2f} - {seg['end']:.2f}] {seg['text']}")
    for w in seg.get("words", []):
        print(f"   {w['start']:.2f} - {w['end']:.2f}: {w['word']}")
