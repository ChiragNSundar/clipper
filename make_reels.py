import os
import sys
import shutil
import subprocess

# Set FFmpeg path in environment
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

# Hand-calibrated, acoustically locked Kanglish & English timings
REELS_DATA = [
    {
        "id": 1,
        "start_str": "0:12", "end_str": "0:50", "start": 12, "end": 50,
        "overlay": {"img": BONNIE_IMG, "start": 0.60, "end": 3.60, "y": 800},
        "timings": [
            (0.00,  0.60,  r"THAT..."),
            (0.60,  0.86,  r"BONNIE {\fnSegoe UI Emoji}🥀{\r}"),
            (0.86,  1.34,  r"IS LIKE..."),
            (1.42,  1.78,  r"I DON'T KNOW..."),
            (1.78,  2.10,  r"BRO..."),
            (2.26,  2.56,  r"SHE FEELS..."),
            (2.56,  3.16,  r"LIKE AN ALIEN {\fnSegoe UI Emoji}👽{\r}"),
            (3.16,  3.62,  r"TO ME. {\fnSegoe UI Emoji}👽{\r}"),
            (4.02,  4.68,  r"AH BRO, BRO... {\fnSegoe UI Emoji}💀{\r}"),
            (4.96,  5.42,  r"SHE'S JUST..."),
            (5.42,  6.36,  r"GENEROUS BRO! {\fnSegoe UI Emoji}🥀{\r}"),
            (6.66,  7.58,  r"HAVEN'T SEEN THAT, BRO?"),
            (9.56,  10.40, r"YOU HAVEN'T SEEN..."),
            (10.40, 11.14, r"THAT ONE REEL? {\fnSegoe UI Emoji}😭{\r}"),
            (11.32, 11.82, r"LIKE ONE GUY..."),
            (11.82, 12.86, r"HAS A SMALL D**K {\fnSegoe UI Emoji}💔{\r}"),
            (13.46, 14.50, r"GETTING MADE FUN OF... {\fnSegoe UI Emoji}💀{\r}"),
            (14.84, 15.72, r"AND SHE JUST BRO..."),
            (15.84, 16.60, r"SHE STEPS UP {\fnSegoe UI Emoji}🧍{\r}"),
            (16.60, 17.56, r"FOR HIM, LOWKEY {\fnSegoe UI Emoji}🥀{\r}"),
            (17.98, 19.60, r"IMPRESSED BY THAT, HUH?! {\fnSegoe UI Emoji}😭{\r}"),
            (20.04, 20.74, r"YEAH BRO..."),
            (20.86, 21.58, r"JUST ONE REEL..."),
            (21.58, 22.64, r"PROPAGANDA BRO! {\fnSegoe UI Emoji}🥀{\r}"),
            (22.88, 23.84, r"BRO THIS IS WHY..."),
            (23.84, 24.64, r"I HATE SHANTHANOO BRO! {\fnSegoe UI Emoji}💀{\r}"),
            (25.36, 26.86, r"SHANTHANOO, CAN'T DEFEND YOU HERE! {\fnSegoe UI Emoji}💀😭{\r}"),
            (26.86, 28.08, r"BRO I'M THINKING BRO..."),
            (28.24, 30.12, r"HE TELLS ME R******D S**T..."),
            (30.56, 32.56, r"THEN I TELL MORE R******D S**T... {\fnSegoe UI Emoji}😭{\r}"),
            (32.62, 33.46, r"BUT THAT'S ALL BRO!"),
            (33.72, 34.50, r"THAT'S ALL THAT HAPPENS!"),
            (34.62, 35.42, r"HOW DID YOU GET INFLUENCED?!"),
            (35.76, 37.40, r"HOW IMPRESSED BY THAT, DA?! {\fnSegoe UI Emoji}💀😭{\r}"),
        ]
    },
    {
        "id": 2,
        "start_str": "11:24", "end_str": "12:09", "start": 684, "end": 729,
        "overlay": {"img": MUSTANG_IMG, "start": 23.0, "end": 27.5, "y": 920},
        "timings": [
            (0.82,  2.50,  r"WHICH LANGUAGE IS YOURS"),
            (2.50,  4.62,  r"MOST SIMILAR WHILE SPEAKING?"),
            (5.90,  8.28,  r"IF HE'S BRO, THEN YOU'RE MARATHI BRO"),
            (10.48, 11.70, r"MARATHI BODY GOTHAA? {\fnSegoe UI Emoji}😭{\r}"),
            (11.70, 13.64, r"[LAUGHTER] {\fnSegoe UI Emoji}💀{\r}"),
            (13.64, 15.96, r"YAARO HESAR ITTIDDALA? PRASHASTHU?"),
            (15.96, 18.12, r"PRATHAM BRO! {\fnSegoe UI Emoji}😭💀{\r} [LAUGHS]"),
            (18.72, 21.10, r"NO NO AVNU YAARO..."),
            (21.10, 23.20, r"SOME CAR HE USED TO TELL NO?"),
            (23.20, 25.06, r"SOME CAR, WHAT WAS THAT NAME?"),
            (25.06, 27.58, r"MUSTANG! MUSTANG! {\fnSegoe UI Emoji}🚗{\r}"),
            (27.58, 30.00, r"MARATHI BODY ANTHE! {\fnSegoe UI Emoji}😭🚗{\r}"),
            (30.00, 31.54, r"[LAUGHTER] {\fnSegoe UI Emoji}💀😭{\r}"),
            (31.54, 33.04, r"SCHOOL WAS ACTUALLY GOATED BRO 🐐"),
            (33.04, 36.14, r"IN TERMS OF COMEDY BRO, GOATED BRO!"),
            (36.14, 38.70, r"HUMOR BERE LEVEL, WAY OVER BRO! 🔥"),
            (38.70, 42.28, r"FIRST SECOND PU IDDRE ALLE..."),
            (42.28, 44.78, r"YA ACTUALLY LO, SO GOATED! {\fnSegoe UI Emoji}💀{\r}"),
        ]
    },
    {
        "id": 3,
        "start_str": "18:21", "end_str": "19:10", "start": 1101, "end": 1150,
        "overlay": None,
        "timings": [
            (0.00,  2.00,  r"🎶 RAKTHAMBARA"),
            (2.00,  4.00,  r"BAALE... 🎶"),
            (4.00,  6.00,  r"🎶 RAKTHAMBARA"),
            (6.00,  8.50,  r"BAALEEEEE 🎶"),
            (8.50,  12.80, r"🎺 [MOUTH TRUMPET SOLO] 🎺"),
            (12.80, 15.00, r"THE F**K I CAN'T"),
            (15.00, 17.20, r"DO YOUTUBE BRO {\fnSegoe UI Emoji}💀{\r}"),
            (17.20, 19.50, r"SHOULD BE A 'W'"),
            (19.50, 21.50, r"WAIT... {\fnSegoe UI Emoji}🧍{\r}"),
            (21.50, 24.00, r"🎶 ALLE BAELE"),
            (24.00, 26.50, r"ALLE ALLE LE... 🎶"),
            (26.50, 28.50, r"🎶 YAANI NAANE"),
            (28.50, 30.50, r"NEENE MAANO... 🎶"),
            (30.50, 32.50, r"🎶 HA AANE NINA"),
            (32.50, 34.50, r"NAANE... 🎶"),
            (34.50, 36.50, r"🎶 AANI NINNO"),
            (36.50, 38.50, r"NAANI... {\fnSegoe UI Emoji}🥀{\r}"),
            (38.50, 40.00, r"ASHTENA?"),
            (40.00, 41.50, r"ASHTEH. IT'S OVER. {\fnSegoe UI Emoji}💀{\r}"),
            (41.50, 44.50, r"DUDE HAS LOST IT BRO {\fnSegoe UI Emoji}😭{\r}"),
            (44.50, 48.80, r"I CAN'T EVEN BRO {\fnSegoe UI Emoji}💀🥀{\r}"),
        ]
    },
    {
        "id": 4,
        "start_str": "19:18", "end_str": "20:15", "start": 1158, "end": 1215,
        "overlay": None,
        "timings": [
            (0.54,  2.50,  r"WHAT HAPPENS? WHAT WOULD YOU DO"),
            (2.50,  4.28,  r"N***A WHEN YOU'RE AT HARISH'S?"),
            (4.28,  6.44,  r"BRO, NAH YOU TELL ME N***A"),
            (6.44,  7.68,  r"WHAT WOULD YOU DO BRO?"),
            (7.68,  8.98,  r"I'LL TELL YOU WHEN I DO."),
            (9.36,  11.40, r"NO NO NO, WHAT ARE YOU LOOKING FORWARD TO?"),
            (11.40, 14.00, r"JUST LIKE HAVING BRO... JUST HAVING..."),
            (14.00, 16.50, r"JUST HAVING?! WHAT THE F**K?! {\fnSegoe UI Emoji}😭{\r}"),
            (16.50, 18.00, r"HAVING WHAT?! {\fnSegoe UI Emoji}💀{\r}"),
            (21.86, 24.78, r"GO TO THE STREET IN THE MIDDLE OF THE NIGHT"),
            (24.78, 27.50, r"AND FIND A... NO NO LISTEN FULLY!"),
            (27.50, 31.10, r"HAVING THE PERSON, GET IT?"),
            (31.60, 34.00, r"PERSON BRO, PERSON! HAVING A PERSON."),
            (34.00, 36.94, r"AS IN LIKE EATING THEM OR WHAT?! {\fnSegoe UI Emoji}💀{\r}"),
            (36.94, 39.12, r"[LAUGHTER] {\fnSegoe UI Emoji}😭{\r}"),
            (39.12, 42.50, r"NO NO NO, HARISH IS YOUR FRIEND..."),
            (42.50, 45.24, r"SO YOU HAVE HARISH AS A FRIEND, LIKE THAT!"),
            (47.00, 49.50, r"YOU'LL HAVE THE GIRL AS A FRIEND?"),
            (49.50, 52.34, r"NO NO! [LAUGHTER] BRO I'LL KILL YOU BRO! {\fnSegoe UI Emoji}💀{\r}"),
            (52.34, 57.00, r"SHANTHANOOO! [LAUGHS] {\fnSegoe UI Emoji}😭💀{\r}"),
        ]
    },
    {
        "id": 5,
        "start_str": "22:25", "end_str": "22:53", "start": 1345, "end": 1373,
        "overlay": None,
        "timings": [
            (0.00,  2.50,  r"THALE NOVU YA... {\fnSegoe UI Emoji}😭{\r}"),
            (2.50,  4.50,  r"[HEADACHE BRO!] HANGE HANGE..."),
            (4.76,  6.24,  r"NANGE... SUMNE IRI! {\fnSegoe UI Emoji}💀{\r}"),
            (6.24,  7.50,  r"WHAT?! {\fnSegoe UI Emoji}😭{\r} [LAUGHS]"),
            (11.62, 13.78, r"BRO YOU ACTUALLY GOT DA..."),
            (13.78, 14.78, r"YOU ACTUALLY GOT DA! {\fnSegoe UI Emoji}💀{\r}"),
            (14.78, 16.50, r"WHAT GOT BRO? YOU HAVE LOST BRO! {\fnSegoe UI Emoji}🥀{\r}"),
            (16.94, 20.14, r"ILLA LO, I STOPPED FROM SO LONG BRO!"),
            (20.14, 22.98, r"IT DOESN'T MATTER EVEN IF I TAKE IT, SAME BRO..."),
            (23.78, 26.10, r"LOST HIS MIND CUZ HE DOESN'T HAVE HUGS! {\fnSegoe UI Emoji}😭💔{\r}"),
            (26.10, 27.98, r"YEAH BRO LEGIT, I'M NOT KIDDING BRO! {\fnSegoe UI Emoji}💀{\r}"),
        ]
    },
    {
        "id": 6,
        "start_str": "23:53", "end_str": "24:01", "start": 1433, "end": 1441,
        "overlay": {"img": CHAPPAR_IMG, "start": 0.0, "end": 5.0, "y": 980},
        "timings": [
            (0.00,  1.80,  r"ANDHRE EVEN I'M CHAPPAR..."),
            (1.80,  3.50,  r"EVEN YOU'RE CHAPPAR..."),
            (3.50,  5.50,  r"TOGETHER LET'S BE CHAPPAR! {\fnSegoe UI Emoji}🥀{\r}"),
            (5.50,  7.00,  r"WHAT IS HE SAYING BRO {\fnSegoe UI Emoji}💀{\r}"),
            (7.00,  8.00,  r"I'VE LOST IT! {\fnSegoe UI Emoji}😭💀{\r}"),
        ]
    },
    {
        "id": 7,
        "start_str": "24:15", "end_str": "24:40", "start": 1455, "end": 1480,
        "overlay": None,
        "timings": [
            (0.00,  3.50,  r"FOR ME, I'M COUNTING THE NON..."),
            (3.50,  5.80,  r"NON-PENE ALSO... NON-PENETRATIVE ALSO!"),
            (5.80,  7.96,  r"EVEN THAT... EVEN WITH THAT YOU'RE ZERO?! {\fnSegoe UI Emoji}😭{\r}"),
            (9.00,  11.44, r"[LAUGHTER] {\fnSegoe UI Emoji}💀😭{\r}"),
            (11.44, 13.54, r"YEAH YEAH, YO! {\fnSegoe UI Emoji}🥀{\r}"),
            (14.44, 16.08, r"YOU DIDN'T HAVE TO CLARIFY THAT LIKE THAT MAN!"),
            (16.08, 18.70, r"I'M JUST KIDDING BRO, OBVIOUSLY EVEN I'M ZERO BRO {\fnSegoe UI Emoji}💔{\r}"),
            (18.70, 20.62, r"BRO YOU KO'D ME AT THE SAME TIME BRO! {\fnSegoe UI Emoji}💀{\r}"),
            (22.42, 24.98, r"YOU KO'D ME EXACTLY IN-GAME AND IRL! {\fnSegoe UI Emoji}😭🔥{\r}"),
        ]
    },
]

# Wipe old clips and start clean
print("🧹 Cleaning out older clips and scratch files...")
if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)
os.makedirs(OUT_DIR, exist_ok=True)

for fname in os.listdir("."):
    if fname.startswith("test_") or fname.startswith("tiktok_") or fname.startswith("clip") or fname.startswith("check_") or fname in ["bonnie_blue.jpg", "mustang.jpg", "bonnie_preview.jpg", "overlay_preview.jpg", "reel_preview.jpg", "sample_frame.jpg", "info.json", "chappri_sticker.png"]:
        try:
            os.remove(fname)
        except Exception:
            pass

# Process all 7 clips
for reel in REELS_DATA:
    cid = reel["id"]
    start = reel["start"]
    end = reel["end"]
    print(f"\n{'='*55}")
    print(f"🎬 Processing Reel {cid}/{len(REELS_DATA)}: [{reel['start_str']} - {reel['end_str']}] ({start}s - {end}s)")
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

    # Step 2: Build TikTok dynamic ASS subtitles (tight acoustic lockstep)
    events = []
    for start_t, end_t, phrase in reel["timings"]:
        phrase_c = clean_and_censor(phrase)
        line = rf"{{\c&H002EFFFF&\fscx112\fscy112}}{phrase_c}{{\r\c&H00FFFFFF&}}"
        events.append(f"Dialogue: 0,{ts(start_t)},{ts(end_t)},TikTok,,0,0,0,,{line}")

    with open(ass_file, "w", encoding="utf-8") as f:
        f.write(ASS_HEADER + "\n".join(events) + "\n")
    print(f"Generated {len(events)} acoustically synced subtitle events in {ass_file}")

    # Step 3: Render Reel (with optional image sticker overlay)
    safe_ass_path = ass_file.replace("\\", "/").replace(":", "\\:")
    overlay_info = reel.get("overlay")
    
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

    # Clean intermediate raw cuts and ass files
    if os.path.exists(raw_video):
        os.remove(raw_video)
    if os.path.exists(ass_file):
        os.remove(ass_file)

# Clean up any leftover non-mp4 files in OUT_DIR
for f in os.listdir(OUT_DIR):
    if not f.endswith(".mp4"):
        try:
            os.remove(os.path.join(OUT_DIR, f))
        except Exception:
            pass

print("\n" + "="*55)
print("🎉 ALL 7 REELS SUCCESSFULLY RENDERED & CLEANED! 🎉")
print("="*55)
for r in REELS_DATA:
    cid = r["id"]
    fpath = os.path.join(OUT_DIR, f"reel_{cid:02d}.mp4")
    if os.path.exists(fpath):
        size_mb = os.path.getsize(fpath) / (1024 * 1024)
        print(f" ✅ {fpath} ({size_mb:.2f} MB)")
