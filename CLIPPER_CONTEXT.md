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

## 6. Workspace & Git Cleanliness

- **Keep on Disk**:
  - Final `.mp4` video reels inside `reels/`.
  - Production scripts (`make_reels.py`).
  - Persistent sticker assets (`*.png`).
  - Context & rules guides (`CLIPPER_CONTEXT.md`, `.gemini/rules.md`, `.gitignore`).
- **Always Delete**:
  - Temporary audio (`*.wav`, `*.aac`, `*.mp3`).
  - Temporary video parts (`*.part`, `part_*.mp4`, `raw_*.mp4`).
  - Subtitle scripts (`*.ass`).
  - Test scripts and image previews (`test_*`, `check_*`, `sample_*`, `val_*`).
- **Git Hygiene**:
  - All media outputs in `reels/` and temporary media files are excluded via `.gitignore`.
