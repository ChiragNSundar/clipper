import os
import sys
import shutil
import subprocess
import whisper

# Set FFmpeg path in environment so Whisper can use it
FFMPEG_DIR = r"C:\Users\Chirag\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.1-full_build\bin"
os.environ["PATH"] = FFMPEG_DIR + os.pathsep + os.environ.get("PATH", "")

FFMPEG = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
if not os.path.exists(FFMPEG):
    FFMPEG = shutil.which("ffmpeg") or "ffmpeg"

print(f"Using FFmpeg: {FFMPEG}")

# Configuration
URL = "https://www.youtube.com/live/RDhQI8-CcbM"
OUT_DIR = "reels"

# Sticker images
BONNIE_IMG = "bonnie_sticker.png"
MUSTANG_IMG = "mustang_sticker.png"
CHAPPAR_IMG = "chappar_sticker.png"

# Exact Clips (Clip 5 corrected: 22:25 to 22:53 = 1345s to 1373s)
CLIPS = [
    {"id": 1, "start_str": "0:12",  "end_str": "0:50",  "start": 12,   "end": 50},
    {"id": 2, "start_str": "11:24", "end_str": "12:09", "start": 684,  "end": 729},
    {"id": 3, "start_str": "18:21", "end_str": "19:10", "start": 1101, "end": 1150},
    {"id": 4, "start_str": "19:18", "end_str": "20:15", "start": 1158, "end": 1215},
    {"id": 5, "start_str": "22:25", "end_str": "22:53", "start": 1345, "end": 1373},
    {"id": 6, "start_str": "23:53", "end_str": "24:01", "start": 1433, "end": 1441},
    {"id": 7, "start_str": "24:15", "end_str": "24:40", "start": 1455, "end": 1480},
]

# Overlays config
OVERLAYS = {
    1: {"img": BONNIE_IMG, "start": 0.0, "end": 3.2, "y": 800},
    2: {"img": MUSTANG_IMG, "start": 22.8, "end": 27.2, "y": 920},
    6: {"img": CHAPPAR_IMG, "start": 0.0, "end": 5.0, "y": 980},
}

# Censorship filter
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

def clean_and_censor(text):
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

def ts(seconds):
    h = int(seconds // 3600)
    m = int(seconds % 3600 // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TikTok,Impact,78,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,8,3,2,60,60,550,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

# Delete older reels and scratch files completely
print("🧹 Cleaning out older clips and temporary artifacts...")
if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)
os.makedirs(OUT_DIR, exist_ok=True)

for fname in os.listdir("."):
    if fname.startswith("test_") or fname.startswith("tiktok_") or fname.startswith("clip") or fname.startswith("check_") or fname in ["bonnie_blue.jpg", "mustang.jpg", "bonnie_preview.jpg", "overlay_preview.jpg", "reel_preview.jpg", "sample_frame.jpg", "info.json"]:
        try:
            os.remove(fname)
        except Exception:
            pass

# Load Whisper model for exact acoustic word timestamps
print("🧠 Loading OpenAI Whisper model for acoustic alignment...")
whisper_model = whisper.load_model("base")

# Process all 7 clips
for clip in CLIPS:
    cid = clip["id"]
    start = clip["start"]
    end = clip["end"]
    print(f"\n{'='*55}")
    print(f"🎬 Processing Reel {cid}/{len(CLIPS)}: [{clip['start_str']} - {clip['end_str']}] ({start}s - {end}s)")
    print(f"{'='*55}")

    raw_video = os.path.join(OUT_DIR, f"raw_{cid}.mp4")
    ass_file = os.path.join(OUT_DIR, f"clip_{cid}.ass")
    final_reel = os.path.join(OUT_DIR, f"reel_{cid:02d}.mp4")

    # Step 1: Download section
    print(f"Downloading stream section ({start}s to {end}s)...")
    cmd_ytdlp = [
        sys.executable, "-m", "yt_dlp",
        "--ffmpeg-location", FFMPEG_DIR,
        "--download-sections", f"*{start}-{end}",
        "-f", "bv*[height<=1080]+ba/b",
        "--merge-output-format", "mp4",
        "-o", raw_video,
        URL
    ]
    subprocess.run(cmd_ytdlp, check=True)

    # Step 2: Extract exact acoustic word timestamps using Whisper
    print("Extracting acoustic word timestamps with Whisper...")
    result = whisper_model.transcribe(raw_video, word_timestamps=True)
    
    acoustic_words = []
    for seg in result.get("segments", []):
        for w in seg.get("words", []):
            word_str = w["word"].strip()
            if word_str:
                acoustic_words.append({
                    "start": max(0.0, w["start"]),
                    "end": max(w["start"] + 0.15, w["end"]),
                    "word": word_str
                })

    # Step 3: Format into micro-chunks (1 to 2 words per pop) with Kanglish corrections & Gen-Z emojis
    events = []

    if cid == 1:
        # Reel 1: Bonnie Blue, small d**k, propaganda
        # Replace misheard words with Bonnie, generous, etc.
        corrected = []
        for w in acoustic_words:
            w_text = w["word"].upper()
            if w_text in ["MORNING", "BODY"]:
                w_text = "BONNIE"
            elif w_text == "JEALOUS":
                w_text = "GENEROUS"
            corrected.append({"start": w["start"], "end": w["end"], "word": w_text})

        # Group 1-2 words
        i = 0
        while i < len(corrected):
            chunk = corrected[i:i+2]
            text = " ".join(cw["word"] for cw in chunk)
            start_t = chunk[0]["start"]
            end_t = chunk[-1]["end"]
            
            # Add emojis to punchline words
            if "BONNIE" in text: text += r" {\fnSegoe UI Emoji}🥀{\r}"
            elif "ALIEN" in text: text += r" {\fnSegoe UI Emoji}👽{\r}"
            elif "DICK" in text or "D**K" in text: text += r" {\fnSegoe UI Emoji}💔{\r}"
            elif "STEPS" in text: text += r" {\fnSegoe UI Emoji}🧍{\r}"
            elif "PROPAGANDA" in text: text += r" {\fnSegoe UI Emoji}🥀{\r}"
            elif "DEFEND" in text: text += r" {\fnSegoe UI Emoji}💀{\r}"
            
            censored = clean_and_censor(text)
            line = rf"{{\c&H002EFFFF&\fscx112\fscy112}}{censored}{{\r\c&H00FFFFFF&}}"
            events.append(f"Dialogue: 0,{ts(start_t)},{ts(end_t)},TikTok,,0,0,0,,{line}")
            i += 2

    elif cid == 2:
        # Reel 2: Marathi body gothaa, Pratham bro, Mustang
        i = 0
        while i < len(acoustic_words):
            chunk = acoustic_words[i:i+2]
            text = " ".join(cw["word"].upper() for cw in chunk)
            start_t = chunk[0]["start"]
            end_t = chunk[-1]["end"]

            # Kanglish injection
            if "MARATHI" in text and "BODY" in text:
                text = r"MARATHI BODY GOTHAA? {\fnSegoe UI Emoji}😭{\r}"
            elif "PRASHASTHU" in text or "PRATHAM" in text:
                text = r"PRATHAM BRO! {\fnSegoe UI Emoji}💀{\r}"
            elif "MUSTANG" in text:
                text = r"MUSTANG! MUSTANG! {\fnSegoe UI Emoji}🚗{\r}"
            elif "HUMOR" in text or "LEVEL" in text:
                text = r"HUMOR BERE LEVEL! {\fnSegoe UI Emoji}🔥{\r}"
            elif "FIRST" in text and "SECOND" in text:
                text = r"FIRST SECOND PU IDDRE ALLE {\fnSegoe UI Emoji}💀{\r}"

            censored = clean_and_censor(text)
            line = rf"{{\c&H002EFFFF&\fscx112\fscy112}}{censored}{{\r\c&H00FFFFFF&}}"
            events.append(f"Dialogue: 0,{ts(start_t)},{ts(end_t)},TikTok,,0,0,0,,{line}")
            i += 2

    elif cid == 3:
        # Reel 3: Kannada singing & comedy
        raw_events = [
            (0.0,  2.0,  r"🎶 RAKTHAMBARA"),
            (2.0,  4.0,  r"BAALE... 🎶"),
            (4.0,  6.0,  r"🎶 RAKTHAMBARA"),
            (6.0,  8.5,  r"BAALEEEEE 🎶"),
            (8.5,  12.8, r"🎺 [MOUTH TRUMPET SOLO] 🎺"),
            (12.8, 15.0, r"THE F**K I CAN'T"),
            (15.0, 17.2, r"DO YOUTUBE BRO {\fnSegoe UI Emoji}💀{\r}"),
            (17.2, 19.5, r"SHOULD BE A 'W'"),
            (19.5, 21.5, r"WAIT... {\fnSegoe UI Emoji}🧍{\r}"),
            (21.5, 24.0, r"🎶 ALLE BAELE"),
            (24.0, 26.5, r"ALLE ALLE LE... 🎶"),
            (26.5, 28.5, r"🎶 YAANI NAANE"),
            (28.5, 30.5, r"NEENE MAANO... 🎶"),
            (30.5, 32.5, r"🎶 HA AANE NINA"),
            (32.5, 34.5, r"NAANE... 🎶"),
            (34.5, 36.5, r"🎶 AANI NINNO"),
            (36.5, 38.5, r"NAANI... {\fnSegoe UI Emoji}🥀{\r}"),
            (38.5, 40.0, r"ASHTENA?"),
            (40.0, 41.5, r"ASHTEH. IT'S OVER. {\fnSegoe UI Emoji}💀{\r}"),
            (41.5, 44.5, r"DUDE HAS LOST IT BRO {\fnSegoe UI Emoji}😭{\r}"),
            (44.5, 48.8, r"I CAN'T EVEN BRO {\fnSegoe UI Emoji}💀🥀{\r}"),
        ]
        for st, et, txt in raw_events:
            line = rf"{{\c&H002EFFFF&\fscx112\fscy112}}{txt}{{\r\c&H00FFFFFF&}}"
            events.append(f"Dialogue: 0,{ts(st)},{ts(et)},TikTok,,0,0,0,,{line}")

    elif cid == 4:
        # Reel 4: Harish, having a person, N***A censored
        i = 0
        while i < len(acoustic_words):
            chunk = acoustic_words[i:i+2]
            text = " ".join(cw["word"].upper() for cw in chunk)
            start_t = chunk[0]["start"]
            end_t = chunk[-1]["end"]

            if "PERSON" in text: text += r" {\fnSegoe UI Emoji}🧍{\r}"
            elif "EATING" in text: text += r" {\fnSegoe UI Emoji}💀{\r}"
            elif "KILL" in text: text += r" {\fnSegoe UI Emoji}💀{\r}"
            elif "SHANTHANOO" in text: text += r" {\fnSegoe UI Emoji}😭💀{\r}"

            censored = clean_and_censor(text)
            line = rf"{{\c&H002EFFFF&\fscx112\fscy112}}{censored}{{\r\c&H00FFFFFF&}}"
            events.append(f"Dialogue: 0,{ts(start_t)},{ts(end_t)},TikTok,,0,0,0,,{line}")
            i += 2

    elif cid == 5:
        # Reel 5: 22:25 - 22:53 Kanglish (Thale novu ya, Sumne iri, Illa lo, No hugs)
        raw_events = [
            (0.0,  1.8,  r"THALE NOVU YA... {\fnSegoe UI Emoji}😭{\r}"),
            (1.8,  3.2,  r"[HEADACHE BRO!]"),
            (3.2,  4.8,  r"HANGE HANGE..."),
            (4.8,  6.2,  r"SUMNE IRI! {\fnSegoe UI Emoji}💀{\r}"),
            (6.2,  8.0,  r"WHAT?! {\fnSegoe UI Emoji}😭{\r}"),
            (8.0,  10.0, r"YOU ACTUALLY GOT DA..."),
            (10.0, 12.0, r"YOU ACTUALLY GOT DA! {\fnSegoe UI Emoji}💀{\r}"),
            (12.0, 14.0, r"YOU GOT LOST BRO..."),
            (14.0, 16.0, r"YOU HAVE LOST BRO {\fnSegoe UI Emoji}🥀{\r}"),
            (16.0, 18.0, r"ILLA LO, I STOPPED..."),
            (18.0, 20.0, r"FROM SO LONG BRO!"),
            (20.0, 22.0, r"IT DOESN'T MATTER SAME BRO"),
            (22.0, 24.0, r"LOST HIS MIND {\fnSegoe UI Emoji}😭{\r}"),
            (24.0, 26.0, r"NO HUGS! {\fnSegoe UI Emoji}💔🥀{\r}"),
            (26.0, 28.0, r"NOT KIDDING BRO! {\fnSegoe UI Emoji}💀{\r}"),
        ]
        for st, et, txt in raw_events:
            line = rf"{{\c&H002EFFFF&\fscx112\fscy112}}{txt}{{\r\c&H00FFFFFF&}}"
            events.append(f"Dialogue: 0,{ts(st)},{ts(et)},TikTok,,0,0,0,,{line}")

    elif cid == 6:
        # Reel 6: Chappar comedy
        raw_events = [
            (0.0,  1.6,  r"ANDHRE EVEN I'M CHAPPAR..."),
            (1.6,  3.2,  r"EVEN YOU'RE CHAPPAR..."),
            (3.2,  5.2,  r"TOGETHER LET'S BE CHAPPAR! {\fnSegoe UI Emoji}🥀{\r}"),
            (5.2,  6.8,  r"WHAT IS HE SAYING BRO {\fnSegoe UI Emoji}💀{\r}"),
            (6.8,  8.0,  r"I'VE LOST IT! {\fnSegoe UI Emoji}😭💀{\r}"),
        ]
        for st, et, txt in raw_events:
            line = rf"{{\c&H002EFFFF&\fscx112\fscy112}}{txt}{{\r\c&H00FFFFFF&}}"
            events.append(f"Dialogue: 0,{ts(st)},{ts(et)},TikTok,,0,0,0,,{line}")

    elif cid == 7:
        # Reel 7: Non-penetrative
        raw_events = [
            (0.0,  2.2,  r"COUNTING THE NON..."),
            (2.2,  4.2,  r"NON-PENE ALSO..."),
            (4.2,  6.2,  r"NON-PENETRATIVE ALSO! {\fnSegoe UI Emoji}💀{\r}"),
            (6.2,  8.2,  r"EVEN WITH THAT YOU'RE ZERO?! {\fnSegoe UI Emoji}😭{\r}"),
            (8.2,  10.2, r"[LAUGHTER] {\fnSegoe UI Emoji}💀😭{\r}"),
            (10.2, 12.2, r"YEAH YEAH YO! {\fnSegoe UI Emoji}🥀{\r}"),
            (12.2, 14.8, r"DIDN'T HAVE TO CLARIFY THAT!"),
            (14.8, 17.2, r"OBVIOUSLY EVEN I'M ZERO BRO {\fnSegoe UI Emoji}💔{\r}"),
            (17.2, 19.2, r"BRO YOU KO'D ME {\fnSegoe UI Emoji}💀{\r}"),
            (19.2, 21.2, r"AT THE SAME TIME!"),
            (21.2, 25.0, r"KO'D ME IN-GAME AND IRL! {\fnSegoe UI Emoji}😭🔥{\r}"),
        ]
        for st, et, txt in raw_events:
            line = rf"{{\c&H002EFFFF&\fscx112\fscy112}}{txt}{{\r\c&H00FFFFFF&}}"
            events.append(f"Dialogue: 0,{ts(st)},{ts(et)},TikTok,,0,0,0,,{line}")

    with open(ass_file, "w", encoding="utf-8") as f:
        f.write(ASS_HEADER + "\n".join(events) + "\n")
    print(f"Generated {len(events)} acoustic-aligned subtitle events in {ass_file}")

    # Step 4: Render Reel with FFmpeg
    safe_ass_path = ass_file.replace("\\", "/").replace(":", "\\:")
    overlay_info = OVERLAYS.get(cid)
    
    if overlay_info and os.path.exists(overlay_info["img"]):
        img_path = overlay_info["img"]
        o_start = overlay_info["start"]
        o_end = overlay_info["end"]
        o_y = overlay_info["y"]
        print(f"Adding photo overlay '{img_path}' ({o_start}s to {o_end}s)...")
        filter_complex = (
            f"[0:v]crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920:flags=lanczos,setsar=1[bg]; "
            f"[bg][1:v]overlay=(W-w)/2:{o_y}:enable='between(t,{o_start},{o_end})'[v]; "
            f"[v]subtitles='{safe_ass_path}'[outv]"
        )
        cmd_ffmpeg = [
            FFMPEG, "-y",
            "-i", raw_video,
            "-i", img_path,
            "-filter_complex", filter_complex,
            "-map", "[outv]", "-map", "0:a",
            "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            final_reel
        ]
    else:
        vf_filter = f"crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920:flags=lanczos,setsar=1,subtitles='{safe_ass_path}'"
        cmd_ffmpeg = [
            FFMPEG, "-y",
            "-i", raw_video,
            "-vf", vf_filter,
            "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            final_reel
        ]

    print(f"Rendering final Reel -> {final_reel}...")
    subprocess.run(cmd_ffmpeg, check=True)

    # Immediately delete intermediate raw video and ass files
    if os.path.exists(raw_video):
        os.remove(raw_video)
    if os.path.exists(ass_file):
        os.remove(ass_file)

# Clean up any leftover temporary files in reels
for f in os.listdir(OUT_DIR):
    if not f.endswith(".mp4"):
        try:
            os.remove(os.path.join(OUT_DIR, f))
        except Exception:
            pass

print("\n" + "="*55)
print("🎉 ALL 7 REELS SUCCESSFULLY GENERATED & CLEANED! 🎉")
print("="*55)
for clip in CLIPS:
    cid = clip["id"]
    fpath = os.path.join(OUT_DIR, f"reel_{cid:02d}.mp4")
    if os.path.exists(fpath):
        size_mb = os.path.getsize(fpath) / (1024 * 1024)
        print(f" ✅ {fpath} ({size_mb:.2f} MB)")
