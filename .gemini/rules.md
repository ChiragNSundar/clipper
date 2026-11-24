# Clipper Video Production & Transcription Rules

## 1. Zero-Tolerance for Phonetic Hallucination (Kannada / Kanglish / Regional Slang)
- Do not let speech-to-text models force Indian regional languages (Kannada, Hindi, Tamil) into English words that sound vaguely similar.
- Never transcribe:
  - "Mute mado" as "4 mutes", "be muted", or "mute made". It is Kannada (ಮ್ಯೂಟ್ ಮಾಡು) meaning "Mute him/it".
  - "Chappar" as "chappri". Use the authentic Kannada slang "Chappar".
  - "Raze" as "raised". Cross-reference gaming visuals (Valorant agents: Raze, Yoru, Reyna, Sova, Jett).
  - "Your mom" as "your mouth". Recognize roast and mom-joke banter.
- Transcribe in Kanglish (Kannada + English) or Hinglish (Hindi + English) when spoken. Common words: *Gothaa?*, *Anthe*, *Thale novu*, *Sumne iri*, *Illa lo*, *Hange*, *Andhre*, *Bere level*, *Mado*, *Beda*, *Ashtena*.

## 2. Subtitle Pacing & Styling (Micro-Chunking)
- Subtitles must be micro-chunked (1 to 2 words per card, at most 3 short words) locked to exact acoustic speech onsets. Never show words early.
- Style: `Impact` font, size 78, 8px black outline, 3px shadow.
- Active spoken words must pop in Neon Yellow (`&H002EFFFF`) with 115% scale (`\fscx115\fscy115`).
- Emojis must use DirectWrite fallback: `{\fnSegoe UI Emoji}`.
- Vertical safe margin: `MarginV: 450` to `550` (measured from bottom).

## 3. Censorship Rules
- Mask vulgar words with first letter, last letter, and 2-3 stars:
  `DICK` -> `D**K`, `SHIT` -> `S**T`, `FUCK` -> `F**K`, `NIGGA` -> `N***A`, `RETARDED` -> `R******D`, `BITCH` -> `B***H`.

## 4. Workspace Cleanliness
- Always delete scratch scripts, extracted audio waveforms (`*.wav`, `*.aac`), frame previews (`*.jpg`), and `.ass` files after rendering.
- Keep only final `.mp4` reels in `reels/`.
- Ensure all media files remain ignored by Git via `.gitignore`.
