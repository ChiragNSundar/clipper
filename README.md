# 🎬 Universal Clipper Engine

A high-performance, modular CLI and Python framework designed for creating **Instagram Reels, TikToks, and YouTube Shorts (9:16 vertical video)** from gaming streams, podcasts, and video clips.

Built specifically to handle Indian regional slang (Kanglish/Hinglish), accurate acoustic micro-chunking, dynamic popping stickers, and 100% hang-proof FFmpeg rendering.

---

## 📁 Repository Structure

```
clipper/
│
├── clipper/                    # Core Python Engine
│   ├── __init__.py             # Public API exports
│   ├── config.py               # Paths, colors, font defaults, censorship, slang glossary
│   ├── engine.py               # Rendering pipeline, timeouts, -shortest guardrails
│   ├── layouts.py              # 9:16 layout generators (center, ambient, split)
│   ├── subtitles.py            # Micro-chunking, active pop highlight, ASS builder
│   └── transcribe.py           # Whisper wrapper with regional vocabulary priming
│
├── clipper.py                  # Unified CLI Tool
├── stickers/                   # 🎨 Dedicated folder for stickers, portraits & badges
│   ├── darshan_sticker.png     # Darshan Thoogudeepa smiling portrait card
│   ├── mustang_sticker.png     # Ford Mustang badge
│   ├── bonnie_sticker.png      # Bonnie Blue sticker card
│   └── chappar_sticker.png     # 100% Certified Chappar badge
│
├── reels/                      # 🎥 Output directory for completed .mp4 reels (gitignored)
├── CLIPPER_CONTEXT.md          # 📖 Single Source of Truth for slang glossary & rules
├── make_reels.py               # Legacy reference script
└── README.md                   # This documentation
```

---

## ⚡ Quick Start

Ensure you have Python 3.10+ and FFmpeg installed.

```bash
# Clone or navigate to the repository
cd e:\GitHub\clipper

# Test CLI help
python clipper.py --help
```

---

## 📖 CLI Commands & Usage

### 1. Inspect Video Details (`info`)
Quickly check resolution, duration, audio presence, and file size before processing.
```bash
python clipper.py info "your_video.mp4"
```

---

### 2. Transcribe Audio & Generate Subtitles (`transcribe`)
Extracts audio and produces tightly synced, micro-chunked ASS subtitles.
- Applies regional slang corrections automatically.
- Masks vulgarity (e.g., `DICK` $\rightarrow$ `D**K`, `FUCK` $\rightarrow$ `F**K`).
- Wraps emojis with `Segoe UI Emoji` glyph fallback.
```bash
python clipper.py transcribe "your_video.mp4" --out "subtitles.ass"
```

**Options:**
- `--model base` (default, fast on CPU) or `--model small` / `--model medium`
- `--margin-v 260` (bottom margin in pixels, clear of mobile UI)

---

### 3. Render 9:16 Vertical Reels (`render`)

The engine provides 3 standard layout templates designed for mobile short-form video:

#### Layout Mode A: `split` (Lobby + Discord Voice Overlay)
Perfect for multiplayer games where you want the **gameplay lobby** in the center and the **Discord voice chat overlay** prominent in the lower-middle with full profile pictures (pfps):
```bash
python clipper.py render "8mb.video-iaT-KJDaQyQ1.mp4" \
  --out "reels/bulbul_fans_reel.mp4" \
  --layout split \
  --top-header "BUL BUL FANS" \
  --sticker "darshan" \
  --subs "bulbul.ass"
```

#### Layout Mode B: `discord_game` (Top Gameplay + Center Discord Overlay Card)
Ideal for Discord calls + live gameplay (e.g. Brawlhalla / Valorant). Keeps the main game on top (`960x540` at `y:130`) and centers the enlarged Discord voice overlay card (`440x476` at `y:710`) with subtitles below in the safe zone:
```bash
python clipper.py render "Harish girl rekt.mp4" \
  --out "reels/harish_reel.mp4" \
  --layout discord_game \
  --cut 0:00-0:11,0:16-0:19,0:26-0:45 \
  --subs "subtitles.ass"
```

#### Layout Mode C: `center` (Direct 9:16 Center Crop)
Best for 1v1 fights, agent select screens, or action centered on screen:
```bash
python clipper.py render "gameplay.mp4" \
  --out "reels/clutch_reel.mp4" \
  --layout center \
  --cut 0:12-0:45 \
  --auto-subs
```

#### Layout Mode C: `ambient` (Blurred Background + 16:9 Letterbox)
Best for widescreen comedy, podcasts, or two-person interviews spanning 16:9:
```bash
python clipper.py render "interview.mp4" \
  --out "reels/interview_reel.mp4" \
  --layout ambient \
  --cut 1:00-1:30 \
  --auto-subs
```

---

### 4. Advanced Features

#### 🌐 Direct YouTube URL Input (No full VOD download!)
Pass YouTube links directly as input. Using `yt-dlp`, the engine downloads **only the exact slice** requested:
```bash
python clipper.py render "https://www.youtube.com/watch?v=FsxbjwDg9vA" \
  --out "reels/randeep_reel.mp4" \
  --cut 0:23-0:35,0:56-1:19 \
  --auto-subs
```

#### ✂️ Multi-Segment Stitching
Combine multiple non-adjacent moments into 1 continuous reel:
```bash
# Slices 0:23-0:35 and 0:56-1:19, auto-concatenates them, and renders:
python clipper.py render "input.mp4" \
  --out "reels/highlights.mp4" \
  --cut 0:23-0:35,0:56-1:19
```

#### ⏱️ Dynamic Popping Stickers
Stickers can pop up for a specific duration instead of staying the whole time:
```bash
python clipper.py render "gameplay.mp4" \
  --out "reels/mustang_reel.mp4" \
  --sticker "mustang" \
  --sticker-time 23.0-27.5
```

#### 🔍 Dynamic Snap-Zoom & Comedic SFX Layering
Zoom into a funny character moment and layer meme sound effects (e.g. Vine Boom) with millisecond delays and non-clipping volume mixing:
```bash
python clipper.py render "harish shemale.mp4" \
  --out "reels/harish_shemale_reel.mp4" \
  --layout center \
  --cut 0:16-0:42 \
  --zoom "23.0-26.0:450:800:650:120" \
  --sfx "8.0:sfx/vine_boom.mp3:0.40,23.0:sfx/vine_boom.mp3:0.45" \
  --subs "subtitles.ass"
```

---

### 5. Batch Processing (`batch`)
Process multiple reels from a single JSON configuration file:
```bash
python clipper.py batch reels.json
```

**Example `reels.json`:**
```json
[
  {
    "name": "Bulbul Fans Reel",
    "input": "8mb.video-iaT-KJDaQyQ1.mp4",
    "out": "reels/bulbul_fans_reel.mp4",
    "layout": "split",
    "top_header": "BUL BUL FANS",
    "sticker": "darshan",
    "subs": "bulbul.ass"
  },
  {
    "name": "Bonnie Blue Roast",
    "input": "raw_stream.mp4",
    "out": "reels/bonnie_reel.mp4",
    "layout": "center",
    "cut": "0:12-0:50",
    "sticker": "bonnie",
    "sticker_time": "0.6-3.6",
    "subs": "bonnie.ass"
  }
]
```

---

## 🎨 Sticker Asset Management

All sticker overlays, character portraits, and badges live inside the [`stickers/`](stickers/) folder.

- **Auto-Resolution**: You don't need to type the full path or extension. The CLI automatically searches `stickers/`:
  - `--sticker darshan` resolves to `stickers/darshan_sticker.png`
  - `--sticker mustang` resolves to `stickers/mustang_sticker.png`
  - `--sticker bonnie` resolves to `stickers/bonnie_sticker.png`
  - `--sticker chappar` resolves to `stickers/chappar_sticker.png`
- **Adding New Stickers**: Simply drop any 360x360 PNG image (with transparency) into `stickers/`.

---

## 🛡️ Anti-Hang & Reliability Architecture

This engine enforces strict safety guardrails to ensure renders **never get stuck**:

1. **No Synthetic Unbounded Filters**: Never use `color=...` or synthetic audio generators in filter graphs. Background frames are drawn using native bounded `drawbox` operations on existing video frames.
2. **Mandatory `-shortest`**: Every multi-stream composite pipeline enforces `-shortest` and `:shortest=1` so image loops never run past the end of the video.
3. **Subprocess Timeout**: All render commands run with a hard 180-second timeout.
4. **Mobile Video Compatibility**: Encodes with `-pix_fmt yuv420p`, `setsar=1`, and `scale=...:flags=lanczos` to guarantee playback compatibility across all Android, iOS, and Instagram decoders.

---

## 📜 Context & Slang Rules

For detailed linguistic rules, Kanglish vocabulary mappings, and transcription guidelines, see:
👉 [CLIPPER_CONTEXT.md](CLIPPER_CONTEXT.md)
