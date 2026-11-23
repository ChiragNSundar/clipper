import os
import sys
import shutil
import subprocess

# Configuration
URL = "https://www.youtube.com/live/RDhQI8-CcbM"
OUT_DIR = "reels"

# Stickers
BONNIE_IMG = "bonnie_sticker.png"
MUSTANG_IMG = "mustang_sticker.png"
CHAPPAR_IMG = "chappar_sticker.png"

# Locate FFmpeg
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

# Micro-chunked, tightly-synced Kanglish & English subtitle timings
# 1-2 words per card so text never shows early!
REELS_DATA = [
    {
        "id": 1,
        "start_str": "0:12", "end_str": "0:50", "start": 12, "end": 50,
        "overlay": {"img": BONNIE_IMG, "start": 0.0, "end": 3.5, "y": 800},
        "timings": [
            (0.0,  0.8,  "BONNIE BLUE 🥀"),
            (0.8,  1.6,  "IS LIKE SO..."),
            (1.6,  2.4,  "I DON'T KNOW"),
            (2.4,  3.2,  "BRO... 💀"),
            (3.2,  4.2,  "FEELS LIKE"),
            (4.2,  5.2,  "AN ALIEN 👽"),
            (5.2,  6.0,  "TO ME."),
            (6.0,  6.8,  "NAH BRO,"),
            (6.8,  7.6,  "SHE'S JUST"),
            (7.6,  8.6,  "GENEROUS BRO 🥀"),
            (8.6,  9.5,  "HAVEN'T SEEN THAT?"),
            (9.5,  10.8, "GENEROUS?! 😭"),
            (10.8, 12.0, "[LAUGHTER] 💀"),
            (12.0, 13.5, "THAT ONE REEL?"),
            (13.5, 15.0, "ONE GUY HAS"),
            (15.0, 16.5, "A SMALL D**K 💔"),
            (16.5, 17.8, "GETTING MADE FUN OF..."),
            (17.8, 19.0, "SHE STEPS UP 🧍"),
            (19.0, 20.2, "FOR HIM, LOWKEY."),
            (20.2, 21.8, "INFLUENCED BY THAT?! 😭"),
            (21.8, 23.0, "BY THAT DA?! 💀"),
            (23.0, 24.5, "ONE REEL PROPAGANDA 🥀"),
            (24.5, 26.5, "[LAUGHTER] 💀😭"),
            (26.5, 28.5, "SHANTHANOO 😭"),
            (28.5, 30.5, "CAN'T DEFEND YOU DA! 💀"),
            (30.5, 32.5, "TELLS ME R******D STUFF"),
            (32.5, 34.5, "I TELL MORE R******D STUFF 😭"),
            (34.5, 36.5, "THAT'S ALL THAT HAPPENS!"),
            (36.5, 38.0, "HOW DO YOU GET INFLUENCED?! 💀"),
        ]
    },
    {
        "id": 2,
        "start_str": "11:24", "end_str": "12:09", "start": 684, "end": 729,
        "overlay": {"img": MUSTANG_IMG, "start": 23.0, "end": 27.5, "y": 920},
        "timings": [
            (0.0,  1.5,  "WHICH LANGUAGE?"),
            (1.5,  3.0,  "MOST SIMILAR"),
            (3.0,  4.5,  "WHILE SPEAKING?"),
            (4.5,  6.0,  "THEN YOU'RE"),
            (6.0,  7.2,  "MARATHI BRO!"),
            (7.2,  9.0,  "MARATHI BODY GOTHAA? 😭"),
            (9.0,  10.5, "[LAUGHTER] 💀"),
            (10.5, 12.0, "YAARO HESAR ITTIDDALA?"),
            (12.0, 13.5, "PRASHASTHU? YAARO..."),
            (13.5, 15.0, "PRATHAM BRO! 😭"),
            (15.0, 16.5, "PRATHAM BRO! 💀"),
            (16.5, 18.5, "NO NO AVNU YAARO..."),
            (18.5, 20.2, "SOME CAR HE USED"),
            (20.2, 21.8, "TO TELL NO?"),
            (21.8, 23.2, "WHAT WAS THAT NAME?"),
            (23.2, 25.0, "MUSTANG! MUSTANG! 🚗"),
            (25.0, 27.5, "MARATHI BODY ANTHE! 😭🚗"),
            (27.5, 30.0, "[LAUGHTER] 💀😭"),
            (30.0, 32.5, "SCHOOL WAS ACTUALLY"),
            (32.5, 34.5, "GOATED BRO! 🐐"),
            (34.5, 36.5, "IN TERMS OF COMEDY"),
            (36.5, 38.5, "GOATED BRO 🐐"),
            (38.5, 40.5, "HUMOR BERE LEVEL! 🔥"),
            (40.5, 42.5, "WAY OVER BRO!"),
            (42.5, 45.0, "FIRST SECOND PU IDDRE ALLE 💀"),
        ]
    },
    {
        "id": 3,
        "start_str": "18:21", "end_str": "19:10", "start": 1101, "end": 1150,
        "overlay": None,
        "timings": [
            (0.0,  2.0,  "🎶 RAKTHAMBARA"),
            (2.0,  4.0,  "BAALE... 🎶"),
            (4.0,  6.0,  "🎶 RAKTHAMBARA"),
            (6.0,  8.5,  "BAALEEEEE 🎶"),
            (8.5,  12.8, "🎺 [MOUTH TRUMPET SOLO] 🎺"),
            (12.8, 15.0, "THE F**K I CAN'T"),
            (15.0, 17.2, "DO YOUTUBE BRO 💀"),
            (17.2, 19.5, "SHOULD BE A 'W'"),
            (19.5, 21.5, "WAIT... 🧍"),
            (21.5, 24.0, "🎶 ALLE BAELE"),
            (24.0, 26.5, "ALLE ALLE LE... 🎶"),
            (26.5, 28.5, "🎶 YAANI NAANE"),
            (28.5, 30.5, "NEENE MAANO... 🎶"),
            (30.5, 32.5, "🎶 HA AANE NINA"),
            (32.5, 34.5, "NAANE... 🎶"),
            (34.5, 36.5, "🎶 AANI NINNO"),
            (36.5, 38.5, "NAANI... 🥀"),
            (38.5, 40.0, "ASHTENA?"),
            (40.0, 41.5, "ASHTEH. IT'S OVER. 💀"),
            (41.5, 44.5, "DUDE HAS LOST IT BRO 😭"),
            (44.5, 48.8, "I CAN'T EVEN BRO 💀🥀"),
        ]
    },
    {
        "id": 4,
        "start_str": "19:18", "end_str": "20:15", "start": 1158, "end": 1215,
        "overlay": None,
        "timings": [
            (0.0,  1.8,  "WHAT HAPPENS?"),
            (1.8,  3.8,  "WHAT WOULD YOU DO N***A"),
            (3.8,  5.5,  "AT HARISH'S?"),
            (5.5,  7.0,  "NAH YOU TELL ME N***A"),
            (7.0,  8.5,  "WHAT WOULD YOU DO?"),
            (8.5,  10.5, "TELL YOU WHEN I DO"),
            (10.5, 12.5, "LOOKING FORWARD TO?"),
            (12.5, 14.5, "JUST LIKE HAVING BRO..."),
            (14.5, 16.5, "JUST HAVING?!"),
            (16.5, 18.0, "WHAT THE F**K?! 😭"),
            (18.0, 20.0, "HAVING WHAT?! 💀"),
            (20.0, 22.5, "MIDDLE OF THE NIGHT"),
            (22.5, 25.0, "FIND A..."),
            (25.0, 27.5, "HAVING THE PERSON"),
            (27.5, 29.5, "DID YOU JUST SAY..."),
            (29.5, 31.5, "PERSON BRO, PERSON!"),
            (31.5, 33.5, "HAVING A PERSON."),
            (33.5, 36.0, "AS IN EATING THEM?! 💀"),
            (36.0, 38.0, "OR WHAT?! [LAUGHS] 😭"),
            (38.0, 40.5, "HARISH IS YOUR FRIEND"),
            (40.5, 43.0, "HAVE HARISH AS A FRIEND"),
            (43.0, 45.5, "LIKE THAT!"),
            (45.5, 47.5, "HAVE THE GIRL AS A FRIEND?"),
            (47.5, 50.0, "NO NO! [LAUGHS] 😭"),
            (50.0, 52.5, "BRO I'LL KILL YOU BRO! 💀"),
            (52.5, 57.0, "SHANTHANOOO! 😭💀"),
        ]
    },
    {
        "id": 5,
        "start_str": "22:25", "end_str": "22:53", "start": 1345, "end": 1373,
        "overlay": None,
        "timings": [
            (0.0,  2.0,  "THALE NOVU YA... 😭"),
            (2.0,  3.5,  "[HEADACHE BRO!]"),
            (3.5,  5.0,  "HANGE HANGE..."),
            (5.0,  6.5,  "SUMNE IRI! 💀"),
            (6.5,  8.5,  "WHAT?! [LAUGHS] 😭"),
            (8.5,  10.5, "YOU ACTUALLY GOT DA..."),
            (10.5, 12.5, "YOU ACTUALLY GOT DA! 💀"),
            (12.5, 14.5, "YOU GOT LOST BRO..."),
            (14.5, 16.5, "YOU HAVE LOST BRO 🥀"),
            (16.5, 18.5, "ILLA LO, I STOPPED..."),
            (18.5, 20.5, "FROM SO LONG BRO!"),
            (20.5, 22.5, "IT DOESN'T MATTER SAME BRO"),
            (22.5, 24.5, "LOST HIS MIND 😭"),
            (24.5, 26.5, "NO HUGS! 💔🥀"),
            (26.5, 28.0, "NOT KIDDING BRO! 💀"),
        ]
    },
    {
        "id": 6,
        "start_str": "23:53", "end_str": "24:01", "start": 1433, "end": 1441,
        "overlay": {"img": CHAPPAR_IMG, "start": 0.0, "end": 5.0, "y": 980},
        "timings": [
            (0.0,  1.8,  "ANDHRE EVEN I'M CHAPPAR..."),
            (1.8,  3.5,  "EVEN YOU'RE CHAPPAR..."),
            (3.5,  5.5,  "TOGETHER LET'S BE CHAPPAR! 🥀"),
            (5.5,  7.0,  "WHAT IS HE SAYING BRO 💀"),
            (7.0,  8.0,  "I'VE LOST IT! 😭💀"),
        ]
    },
    {
        "id": 7,
        "start_str": "24:15", "end_str": "24:40", "start": 1455, "end": 1480,
        "overlay": None,
        "timings": [
            (0.0,  2.5,  "COUNTING THE NON..."),
            (2.5,  4.5,  "NON-PENE ALSO..."),
            (4.5,  6.5,  "NON-PENETRATIVE ALSO! 💀"),
            (6.5,  8.5,  "EVEN WITH THAT YOU'RE ZERO?! 😭"),
            (8.5,  10.5, "[LAUGHTER] 💀😭"),
            (10.5, 12.5, "YEAH YEAH YO! 🥀"),
            (12.5, 15.0, "DIDN'T HAVE TO CLARIFY THAT!"),
            (15.0, 17.5, "OBVIOUSLY EVEN I'M ZERO BRO 💔"),
            (17.5, 19.5, "BRO YOU KO'D ME 💀"),
            (19.5, 21.5, "AT THE SAME TIME!"),
            (21.5, 25.0, "KO'D ME IN-GAME AND IRL! 😭🔥"),
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
Style: TikTok,Impact,78,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,8,3,2,60,60,550,1

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
    if fname.startswith("test_") or fname.startswith("tiktok_") or fname.startswith("clip5_new_audio") or fname.startswith("check_clip3") or fname in ["bonnie_blue.jpg", "mustang.jpg", "bonnie_preview.jpg", "overlay_preview.jpg", "reel_preview.jpg", "sample_frame.jpg", "info.json", "chappri_sticker.png"]:
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

    # Step 2: Build TikTok dynamic ASS subtitles (1-2 words per pop with neon yellow highlight)
    events = []
    for start_t, end_t, phrase in reel["timings"]:
        phrase_c = censor_phrase(phrase)
        # Highlight phrase in neon yellow pop
        line = rf"{{\c&H002EFFFF&\fscx112\fscy112}}{phrase_c}{{\r\c&H00FFFFFF&}}"
        events.append(f"Dialogue: 0,{ts(start_t)},{ts(end_t)},TikTok,,0,0,0,,{line}")

    with open(ass_file, "w", encoding="utf-8") as f:
        f.write(ASS_HEADER + "\n".join(events) + "\n")
    print(f"Generated {len(events)} micro-chunked subtitle events in {ass_file}")

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

    # Immediately delete intermediate raw video and ass files
    if os.path.exists(raw_video):
        os.remove(raw_video)
    if os.path.exists(ass_file):
        os.remove(ass_file)

# Final cleanup of any non-mp4 files in OUT_DIR
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
