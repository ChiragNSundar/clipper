# Clipper Context & Master Rules Guide

This document is the **single source of truth** for video clipping, regional language transcription, subtitle synchronization, visual layout, and audio accuracy standards across all clips in this repository.

---

## 1. Golden Linguistic & Transcription Rules (Kanglish / Hinglish / Regional Slang)

### 🚨 Root Problem & Prevention:
Standard ASR engines (Whisper, Google Speech, etc.) default to English and suffer from severe phonetic bias—they repeatedly attempt to force Indian regional words (Kannada, Hindi, Tamil) into English words that sound vaguely similar, which completely destroys the comedic context of the clip.

### 🛡️ Non-Negotiable Standard Operating Procedure:
1. **Never Blindly Trust English Transcriptions**:
   - Whenever an utterance sounds grammatically broken or out of context in English, it is **almost certainly** Kannada (Kanglish), Hindi (Hinglish), or Indian gaming slang.
   - Cross-check with regional phonetics before ever rendering a subtitle.
2. **Context-Aware Vocabulary Mapping**:
   - Always inspect visual elements on screen (e.g. Valorant agent select screen $\rightarrow$ Raze, Yoru, Reyna, Sova, Jett; Brawlhalla $\rightarrow$ legends, KO; Ascent map, ults, lock-in).
   - Never transcribe gaming terminology as common English phonetic errors (e.g. "Raze" $\neq$ "raised", "ult / ults" $\neq$ "all / out", "KO'd" $\neq$ "cowed").
   - Catch roast / mom humor accurately (e.g. *"ults into your mom"* $\neq$ *"into your mouth"*).

### 📖 Master Kanglish & Regional Slang Glossary:
- **Mute mado** (ಮ್ಯೂಟ್ ಮಾಡು): *"Mute him / mute it"*. (NEVER transcribe as "4 mutes", "be muted", or "mute made").
- **Chappar** (ಚಪ್ಪಾರ್): Local Kannada slang for cheap, cringe, tacky, down-bad. (NEVER transcribe as Hindi "chappri").
- **Gothaa?** (ಗೊತ್ತಾ?): *"Do you know?" / "Did you know?"*
- **Anthe** (ಅಂತೆ): *"He/she says"* (reported speech, e.g. *"Mustang anthe"* $\rightarrow$ *"He says it's a Mustang"*).
- **Thale novu** (ತಲೆ ನೋವು): *"Headache"*.
- **Sumne iri** (ಸುಮ್ನೆ ಇರಿ): *"Stay quiet" / "Keep quiet" / "Shut up"*.
- **Illa lo / Illa da** (ಇಲ್ಲ ಲೋ / ಇಲ್ಲ ಡಾ): *"No dude" / "No bro"*.
- **Hange** (ಹಂಗೆ): *"Like that" / "That's how"*.
- **Nange** (ನಂಗೆ): *"To me" / "For me"*.
- **Andhre** (ಅಂದ್ರೆ): *"Meaning" / "In other words" / "That means"*.
- **Bere level** (ಬೇರೆ ಲೆವೆಲ್): *"Different level" / "Next level"*.
- **Mado / Maadu** (ಮಾಡು): *"Do it"*.
- **Beda** (ಬೇಡ): *"Don't want" / "No"*.
- **Ashtena? / Ashteh** (ಅಷ್ಟೇನಾ? / ಅಷ್ಟೇ): *"Is that all? / That's all"*.
- **Houda?** (ಹೌದಾ?): *"Is it?" / "Really?"*.
- **Bulbul mathadakkilva** (ಬುಲ್ ಬುಲ್ ಮಾತಾಡಕಿಲ್ವಾ): Iconic song hook from Darshan Thoogudeepa's superhit movie *Bul Bul* ("Bulbul, won't you speak?!").
- **Naa olle hudga alva?** (ನಾ ಒಳ್ಳೆ ಹುಡ್ಗ ಅಲ್ವಾ?): *"Am I not a good boy?"* (Verse from *Bul Bul* song).
- **Naa nodak chandag ilva?** (ನಾ ನೋಡಕ್ ಚಂದಾಗ್ ಇಲ್ವಾ?): *"Do I not look handsome?"* (Verse from *Bul Bul* song).
- **Nan preethi madak ilva?** (ನನ್ ಪ್ರೀತಿ ಮಾಡಕ್ ಇಲ್ವಾ?): *"Won't you love me?"* (Verse from *Bul Bul* song).
- **Yaaro idyella!** (ಯಾರೋ ಇದ್ಯಲ್ಲಾ!): *"Someone is there right?!"* (NEVER transcribe as English "ididyhalla" or "did he holler").
- **Lucid**: Gamer / Discord teammate handle (NEVER transcribe as "Lucy" or "Blue").
- **Yaaro hesar ittiddala?**: *"Someone named it right?"*.
- **Lo / Da / Guru / Macha / Maga**: Regional informal address (*Bro / dude / homie*).
- **PU**: Pre-University college (11th & 12th grade in Karnataka).

---

## 2. Vulgarity & Censorship Policy

Mask vulgarity with **first letter, last letter, and 2–3 stars in between**:
- `DICK` $\rightarrow$ `D**K`
- `SHIT` $\rightarrow$ `S**T`
- `FUCK` / `FUCKING` $\rightarrow$ `F**K` / `F*****G`
- `NIGGA` / `NIGGER` $\rightarrow$ `N***A`
- `RETARDED` $\rightarrow$ `R******D`
- `BITCH` $\rightarrow$ `B***H`
- `CUNT` $\rightarrow$ `C**T`

---

## 3. Subtitle Timing & Pacing: Micro-Chunking

- **Lockstep Onsets**: Never display multi-word sentences before the speaker has spoken them.
- **Pacing**: Display **1 to 2 words per card** (at most 3 short words) locked directly to the acoustic speech onset.
- **Pop Highlight**: Active spoken word highlighted in **Neon Yellow** (`&H002EFFFF`) with a 115% scale pop (`\fscx115\fscy115`), while other words remain clean white (`&H00FFFFFF`).
- **Font & Styling**:
  - Font: `Impact`, Fontsize: 78.
  - BorderStyle: 1, Outline: 8 (pure black outline `&H00000000`), Shadow: 3 (`&H80000000`).
  - Fallback Font: `{\fnSegoe UI Emoji}` for emojis.
  - Safe Margin: Vertical margin `450px` to `550px` from bottom (well clear of Instagram Reels descriptions, like buttons, and UI controls).

---

## 4. Visual Layout & Aspect Ratio

- **Target Format**: 9:16 vertical canvas (**1080x1920**).
- **Framing Strategy**:
  1. **Direct Center Crop** (`crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920`): Used when key gameplay or characters are already dead-center (e.g. Valorant Agent Select, Brawlhalla gameplay).
  2. **Blurred Ambient Background**: Used when action spans widescreen (e.g. 16:9 real-world comedy/interviews where characters are on opposite sides):
     `[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg]; [0:v]scale=1080:-1[fg]; [bg][fg]overlay=(W-w)/2:(H-h)/2`

---

## 5. Visual Stickers / Photo Overlays

When a person or prominent subject is confirmed in the audio, a rounded portrait card with an 8px white border appears centered above the subtitle:
- **Bonnie Blue**: `bonnie_sticker.png` (appears *only* while Bonnie is mentioned).
- **Ford Mustang**: `mustang_sticker.png` (appears during Mustang car reference).
- **Chappar Badge**: `chappar_sticker.png` (`100% CHAPPAR` badge).

---

## 6. Universal Clipper Engine & Architecture

The workspace contains a standardized CLI and Python module (`clipper/` + `clipper.py`) to eliminate repetitive ad-hoc scripts and prevent stuck renders.

### Universal CLI Commands:
```bash
# 1. Inspect Video Details
python clipper.py info "video.mp4"

# 2. Transcribe & Auto-Generate Subtitles (with Kanglish slang glossary & micro-chunking)
python clipper.py transcribe "video.mp4" --out "subtitles.ass"

# 3. Render Direct from YouTube URL with Exact Slices (No Full VOD Download)
python clipper.py render "https://www.youtube.com/watch?v=FsxbjwDg9vA" \
  --out "reels/randeep_reel.mp4" \
  --cut 0:23-0:35,0:56-1:19 \
  --auto-subs

# 4. Render with Dynamic Popping Sticker (e.g. Mustang / Bonnie popping only during reference)
python clipper.py render "gameplay.mp4" \
  --out "reels/mustang_reel.mp4" \
  --sticker "mustang_sticker.png" \
  --sticker-time 23.0-27.5 \
  --subs "subtitles.ass"

# 5. Render Split / Discord Overlay Reel
python clipper.py render "video.mp4" --out "reels/output.mp4" --layout split \
  --top-header "BUL BUL FANS" \
  --sticker "darshan_sticker.png" \
  --subs "subtitles.ass"

# 6. Batch Render Multiple Reels from JSON
python clipper.py batch reels.json
```

### 🚨 Critical Anti-Hang / FFmpeg Guardrails:
1. **Never Use Unbounded Filter Sources**: Filters like `color=...` or synthetic audio generators produce infinite frames when piped into `overlay` without strict limits. Always use `drawbox` directly on video frames instead of synthetic color layers.
2. **Strict Loop & Bounds Flag**: Always pass `-shortest` on composite commands and `:shortest=1` on overlay graphs.
3. **Subprocess Timeout**: All render operations in `clipper/engine.py` are wrapped in a hard timeout (`timeout_sec=180`) to guarantee an execution never runs unchecked.
4. **Discord Crop Left Edge**: When cropping Discord overlays, always start at `x: 0` to preserve the full circular avatar pfps of speaking teammates.

---

## 7. Workspace Architecture & Zero Pollution (MANDATORY)

- **NEVER create scratch `.py` scripts** (`test_*.py`, `check_*.py`, `transcribe_*.py`, `build_*.py`, etc.) in the workspace root.
- **Universal Code First**: Add any new features, layout presets, or slang to the `clipper/` package directly and run through `clipper.py`.
- **Use `tempfile.TemporaryDirectory()`**: All intermediate cuts, extracted audio files, concat lists, and templates must be created inside isolated system temporary directories that automatically clean up upon completion.
- **Deliverables Only**: The only files permitted to be created in the repository are finished `.mp4` reels inside `reels/`.

---

## 8. High-Precision Transcription Protocol (How Subtitles Are Made 100% Accurate)

1. **Contextual Prompt Priming**: Always inject Discord usernames (`Lucid`, etc.), regional terms (`idyella`, `mado`, etc.), and game terms into Whisper's `initial_prompt`. This prevents Whisper from hallucinating English words.
2. **Model Scaling for Difficult Audio**: When background game audio, laughter, or heavy accents are present, `whisper base` hallucinates. Fall back to `small` or `medium` to accurately resolve acoustic phonetics.
3. **Word-Level Onset Alignment**: Always transcribe with `word_timestamps=True` on isolated speech sections. Micro-chunk words to their exact physical speech onset times.
4. **Speaker Attribution & Punchline Framing**: When a funny moment occurs (e.g. teammate snapping in Discord call), attribute the speaker (`[GIRL]: "N***A, SHUT THE F**K UP!"`) and the reaction (`SHE TOLD... "N***A, SHUT THE F**K UP", YO!`) to preserve comedic timing.
5. **Censorship**: Strictly apply asterisks to vulgarity (`N***A`, `F**K`, `D**K`, `B***H`, `S**T`).

---

## 9. Comedic Effects: SFX Layering & Snap-Zooms

- **Dedicated SFX Assets (`sfx/`)**: Reusable comedic sound effects (e.g. `sfx/vine_boom.mp3`) are stored in `sfx/`.
- **Audio Mixing Protocol**: When layering SFX under active speech or during awkward silences, set volume to `0.35`–`0.45` and mix with `amix=inputs=...:duration=first:normalize=0` so speech volume is not attenuated.
- **Dynamic Snap-Zoom**: For visual punchlines (e.g. characters in sus poses), use `--zoom "start-end:w:h:x:y"` (e.g. `--zoom "23.0-26.0:450:800:650:120"`).
- **Meta-Subtitle Annotations**: When deadpan silence occurs, annotate with asterisk-bracketed meta-subtitles (e.g. `*AWKWARD SILENCE*... 💀🗿`).


