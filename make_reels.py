import os
import sys
import shutil
import subprocess

# Configuration
URL = "https://www.youtube.com/live/RDhQI8-CcbM"
OUT_DIR = "reels"

# Sticker images
BONNIE_IMG = "bonnie_sticker.png"
MUSTANG_IMG = "mustang_sticker.png"
CHAPPRI_IMG = "chappri_sticker.png"

# Find FFmpeg binary
def find_ffmpeg():
    cmd = shutil.which("ffmpeg")
    if cmd:
        return cmd
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    winget_path = os.path.join(
        local_app_data,
        r"Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.1-full_build\bin\ffmpeg.exe"
    )
    if os.path.exists(winget_path):
        return winget_path
    return "ffmpeg"

FFMPEG = find_ffmpeg()
print(f"Using FFmpeg: {FFMPEG}")

# Vulgarity / Censorship helper: First & last letter with 2-3 stars
def censor_word(w):
    clean = w.strip(".,?!\"'():;~[]")
    upper = clean.upper()
    
    censorship_map = {
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
    
    if upper in censorship_map:
        return w.replace(clean, censorship_map[upper])
    return w

def censor_phrase(phrase):
    words = phrase.split()
    return " ".join(censor_word(w) for w in words)

# Accurate Kanglish, English, and audio-synchronized timings
REELS_DATA = [
    {
        "id": 1,
        "start_str": "0:12", "end_str": "0:50", "start": 12, "end": 50,
        "overlay": {"img": BONNIE_IMG, "start": 0.0, "end": 3.5, "y": 800},
        "timings": [
            (0.0,  1.3,  "LIKE BONNIE", "IS LIKE SO..."),
            (1.3,  2.8,  "I DON'T KNOW BRO", "SHE FEELS LIKE"),
            (2.8,  4.2,  "AN ALIEN", "TO ME."),
            (4.2,  5.8,  "NAH BRO, BRO", "SHE'S JUST"),
            (5.8,  7.2,  "GENEROUS BRO,", "YOU HAVEN'T"),
            (7.2,  8.8,  "SEEN THAT REEL BRO.", ""),
            (8.8,  10.4, "GENEROUS?!", "[LAUGHS]"),
            (10.4, 12.0, "NAH YOU HAVEN'T", "SEEN THAT ONE REEL?"),
            (12.0, 14.0, "LIKE ONE GUY HAS", "LIKE A SMALL D**K,"),
            (14.0, 16.2, "AND HE'S GETTING", "MADE FUN OF..."),
            (16.2, 17.8, "AND SHE JUST BRO,", "SHE STEPS UP"),
            (17.8, 19.5, "FOR HIM BRO,", "LOWKEY."),
            (19.5, 21.8, "SO YOU GOT INFLUENCED", "BY THAT DA?! [LAUGHS]"),
            (21.8, 24.2, "YEAH BRO, JUST ONE", "REEL PROPAGANDA BRO"),
            (24.2, 26.5, "[LAUGHTER]", ""),
            (26.5, 29.0, "SHANTHANOO, I CAN'T", "DEFEND YOU HERE DA!"),
            (29.0, 31.8, "BRO I'M TELLING YOU BRO,", "HE TELLS ME"),
            (31.8, 34.0, "SOME R******D STUFF,", "THEN I GO ON"),
            (34.0, 36.2, "TO TELL MORE", "R******D STUFF..."),
            (36.2, 38.0, "HOW DO YOU GET INFLUENCED", "BY THAT DA?!"),
        ]
    },
    {
        "id": 2,
        "start_str": "11:24", "end_str": "12:09", "start": 684, "end": 729,
        "overlay": {"img": MUSTANG_IMG, "start": 23.2, "end": 27.5, "y": 920},
        "timings": [
            (0.0,  2.0,  "WHICH LANGUAGE IS YOURS", "MOST SIMILAR TO"),
            (2.0,  4.0,  "WHILE SPEAKING?", ""),
            (4.0,  7.0,  "IF HE'S BRO, THEN", "YOU'RE MARATHI BRO."),
            (7.0,  10.2, "MARATHI BODY GOTHAA?", "[LAUGHTER]"),
            (10.2, 13.0, "YAARO HESAR ITTIDDALA?", "PRASHASTHU? YAARO..."),
            (13.0, 16.0, "PRATHAM BRO!", "PRATHAM BRO! [LAUGHS]"),
            (16.0, 19.0, "NO NO AVNU YAARO...", ""),
            (19.0, 21.5, "SOME CAR HE USED", "TO TELL NO?"),
            (21.5, 23.5, "SOME CAR, WHAT WAS", "THAT NAME?"),
            (23.5, 26.5, "MUSTANG! MUSTANG!", "MARATHI BODY ANTHE! [LAUGHS]"),
            (26.5, 29.5, "[LAUGHTER]", "NO NO NO..."),
            (29.5, 32.5, "BRO SCHOOL WAS", "ACTUALLY GOATED BRO."),
            (32.5, 36.0, "IN TERMS OF COMEDY BRO,", "OUR SCHOOL WAS LIKE"),
            (36.0, 38.5, "GOATED BRO.", ""),
            (38.5, 41.5, "HUMOR BERE LEVEL", "WAY OVER BRO!"),
            (41.5, 43.5, "EVEN NOW IT'S...", ""),
            (43.5, 45.0, "FIRST SECOND PU IDDRE ALLE,", "YA ACTUALLY LO!"),
        ]
    },
    {
        "id": 3,
        "start_str": "18:21", "end_str": "19:10", "start": 1101, "end": 1150,
        "overlay": None,
        "timings": [
            (0.0,  3.8,  "🎶 RAKTHAMBARA", "BAALE... 🎶"),
            (3.8,  8.2,  "🎶 RAKTHAMBARA", "BAALEEEEE 🎶"),
            (8.2,  12.8, "[MOUTH TRUMPET", "SOLO]"),
            (12.8, 17.2, "THE F**K I CAN'T", "DO YOUTUBE BRO"),
            (17.2, 21.5, "OH SHOULD BE", "A 'W' WAIT..."),
            (21.5, 26.5, "🎶 ALLE BAELE", "ALLE ALLE LE... 🎶"),
            (26.5, 30.5, "🎶 YAANI NAANE", "NEENE MAANO... 🎶"),
            (30.5, 34.5, "🎶 HA AANE NINA", "NAANE... 🎶"),
            (34.5, 38.5, "🎶 AANI NINNO", "NAANI..."),
            (38.5, 41.5, "ASHTENA? ASHTEH.", "IT'S OVER."),
            (41.5, 45.5, "DUDE HAS LOST", "IT BRO [LAUGHS]"),
            (45.5, 48.8, "I CAN'T EVEN", "BRO!"),
        ]
    },
    {
        "id": 4,
        "start_str": "19:18", "end_str": "20:15", "start": 1158, "end": 1215,
        "overlay": None,
        "timings": [
            (0.0,  2.5,  "WHAT HAPPENS? WHAT WOULD YOU DO", "N***A WHEN YOU'RE AT HARISH'S?"),
            (2.5,  5.0,  "BRO, NAH YOU TELL ME N***A,", "WHAT WOULD YOU DO BRO?"),
            (5.0,  7.5,  "I'LL TELL YOU", "WHEN I DO."),
            (7.5,  10.5, "NO NO NO, LIKE WHAT ARE YOU", "LOOKING FORWARD TO BRO?"),
            (10.5, 14.0, "JUST LIKE HAVING BRO...", "JUST HAVING..."),
            (14.0, 18.0, "JUST HAVING?! WHAT THE F**K?!", "HAVING WHAT?!"),
            (18.0, 22.0, "GO TO THE STREET IN THE", "MIDDLE OF THE NIGHT AND FIND A..."),
            (22.0, 26.5, "NO NO NO, YOU DIDN'T LISTEN FULLY...", "HAVING THE PERSON, GET IT?"),
            (26.5, 30.0, "WAIT WAIT, DID YOU JUST SAY...", "PERSON BRO, PERSON!"),
            (30.0, 33.5, "HAVING A PERSON.", ""),
            (33.5, 38.0, "I MEAN, AS IN LIKE EATING THEM", "OR WHAT?! [LAUGHTER]"),
            (38.0, 42.0, "NO NO NO, ONLY GUYS... LIKE BRO,", "HARISH IS YOUR FRIEND..."),
            (42.0, 46.0, "SO YOU HAVE HARISH AS A FRIEND,", "LIKE THAT!"),
            (46.0, 49.0, "OKAY, YOU'LL HAVE THE GIRL", "AS A FRIEND?"),
            (49.0, 53.5, "NO NO! [LAUGHTER]", "BRO I'LL KILL YOU BRO!"),
            (53.5, 57.0, "SHANTHANOOO! [LAUGHS]", ""),
        ]
    },
    {
        "id": 5,
        "start_str": "22:25", "end_str": "22:53", "start": 1345, "end": 1373,
        "overlay": None,
        "timings": [
            (0.0,  3.2,  "THALE NOVU YA...", "[HEADACHE BRO!]"),
            (3.2,  6.2,  "HANGE HANGE... NANGE...", "SUMNE IRI!"),
            (6.2,  8.5,  "WHAT?! [LAUGHS]", "[LAUGHTER]"),
            (8.5,  12.0, "BRO YOU ACTUALLY GOT DA...", "YOU ACTUALLY GOT DA!"),
            (12.0, 15.0, "WHAT GOT BRO? YOU GOT LOST...", "YOU HAVE LOST BRO..."),
            (15.0, 19.0, "ILLA LO, I STOPPED...", "I STOPPED FROM SO LONG BRO!"),
            (19.0, 22.5, "IT DOESN'T MATTER EVEN IF I TAKE,", "SAME BRO IT'S LIKE..."),
            (22.5, 26.0, "HE HAS LOST HIS MIND", "BECAUSE HE DOESN'T HAVE HUGS!"),
            (26.0, 28.0, "YEAH BRO LEGIT,", "I'M NOT KIDDING BRO!"),
        ]
    },
    {
        "id": 6,
        "start_str": "23:53", "end_str": "24:01", "start": 1433, "end": 1441,
        "overlay": {"img": CHAPPRI_IMG, "start": 0.0, "end": 5.0, "y": 980},
        "timings": [
            (0.0,  2.5,  "ANDHRE EVEN I'M CHAPPRI,", "EVEN YOU'RE CHAPPRI..."),
            (2.5,  5.0,  "SO TOGETHER LET'S BE CHAPPRI!", "RIGHT?"),
            (5.0,  8.0,  "WHAT IS HE SAYING BRO", "I'VE LOST IT! [LAUGHS]"),
        ]
    },
    {
        "id": 7,
        "start_str": "24:15", "end_str": "24:40", "start": 1455, "end": 1480,
        "overlay": None,
        "timings": [
            (0.0,  2.5,  "FOR ME, I'M COUNTING THE NON...", ""),
            (2.5,  5.5,  "NON-PENE ALSO...", "NON-PENETRATIVE ALSO!"),
            (5.5,  8.5,  "EVEN WITH THAT YOU'RE ZERO?", "[LAUGHTER]"),
            (8.5,  12.0, "YEAH YEAH [LAUGHS] YO!", "YOU DIDN'T HAVE TO CLARIFY"),
            (12.0, 15.0, "THAT LIKE THAT MAN!", ""),
            (15.0, 18.5, "I'M JUST KIDDING BRO, OBVIOUSLY", "EVEN I'M ZERO BRO [LAUGHS]"),
            (18.5, 21.5, "BRO YOU KO'D ME AT THE", "SAME TIME BRO!"),
            (21.5, 25.0, "YOU KO'D ME EXACTLY IN-GAME", "AND IRL!"),
        ]
    },
]

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
Style: TikTok,Impact,76,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,8,3,2,60,60,550,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

# Delete all old clips and start completely fresh
print("🧹 Cleaning out older clips and temporary artifacts...")
if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)
os.makedirs(OUT_DIR, exist_ok=True)

# Delete root scratch files
for fname in os.listdir("."):
    if fname.startswith("test_") or fname.startswith("tiktok_") or fname.startswith("clip5_new_audio") or fname.startswith("check_clip3") or fname in ["bonnie_blue.jpg", "mustang.jpg", "bonnie_preview.jpg", "overlay_preview.jpg", "reel_preview.jpg", "sample_frame.jpg", "info.json"]:
        try:
            os.remove(fname)
        except Exception:
            pass

# Process and render all 7 reels
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
    ffmpeg_dir = os.path.dirname(FFMPEG)
    cmd_ytdlp = [
        sys.executable, "-m", "yt_dlp",
        "--ffmpeg-location", ffmpeg_dir,
        "--download-sections", f"*{start}-{end}",
        "-f", "bv*[height<=1080]+ba/b",
        "--merge-output-format", "mp4",
        "-o", raw_video,
        URL
    ]
    subprocess.run(cmd_ytdlp, check=True)

    # Step 2: Build TikTok dynamic ASS subtitles
    events = []
    for start_t, end_t, p1, p2 in reel["timings"]:
        p1_c = censor_phrase(p1)
        p2_c = censor_phrase(p2)
        
        if p2_c:
            mid_t = (start_t + end_t) / 2
            # Phase 1: p1 highlighted in yellow
            line1 = rf"{{\c&H002EFFFF&\fscx112\fscy112}}{p1_c}{{\r\c&H00FFFFFF&}} {p2_c}"
            events.append(f"Dialogue: 0,{ts(start_t)},{ts(mid_t)},TikTok,,0,0,0,,{line1}")
            # Phase 2: p2 highlighted in yellow
            line2 = rf"{p1_c} {{\c&H002EFFFF&\fscx112\fscy112}}{p2_c}{{\r\c&H00FFFFFF&}}"
            events.append(f"Dialogue: 0,{ts(mid_t)},{ts(end_t)},TikTok,,0,0,0,,{line2}")
        else:
            line = rf"{{\c&H002EFFFF&\fscx112\fscy112}}{p1_c}{{\r\c&H00FFFFFF&}}"
            events.append(f"Dialogue: 0,{ts(start_t)},{ts(end_t)},TikTok,,0,0,0,,{line}")

    with open(ass_file, "w", encoding="utf-8") as f:
        f.write(ASS_HEADER + "\n".join(events) + "\n")
    print(f"Generated {len(events)} tightly-synced TikTok subtitle events in {ass_file}")

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

    # Clean intermediate raw video and ass files immediately
    if os.path.exists(raw_video):
        os.remove(raw_video)
    if os.path.exists(ass_file):
        os.remove(ass_file)

# Clean any leftover non-mp4 files in OUT_DIR
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
