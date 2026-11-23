# Clipper Context & Master Rules Guide

This document persists all instructions, stylistic rules, language standards, and production pipelines for cutting Instagram Reels from the stream `https://www.youtube.com/live/RDhQI8-CcbM`.

---

## 1. Timestamps & Clip Metadata

| Reel ID | Start (Time) | End (Time) | Start (Sec) | End (Sec) | Duration | Context / Key Highlights |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Reel 01** | `00:12` | `00:50` | `12` | `50` | 38s | Bonnie Blue mention ("She feels like an alien", "Generous bro", "Small d**k reel", "Propaganda bro"). Bonnie Blue photo sticker overlay above text. |
| **Reel 02** | `11:24` | `12:09` | `684` | `729` | 45s | Marathi body & school comedy. Kanglish: *"Marathi body gothaa?"*, *"Yaaro hesar ittiddala? Pratham bro!"*, *"Mustang! Mustang! Marathi body anthe!"*, *"Humor bere level way over bro!"*, *"First second PU iddre alle, ya actually lo!"*. Mustang photo card overlay. |
| **Reel 03** | `18:21` | `19:10` | `1101` | `1150` | 49s | Kannada singing & gaming reactions: *"Rakthambara baale"*, mouth trumpet solo, *"The f**k I can't do YouTube fellow bro"*, *"Yaani naane neene maano"*, *"Ashtena? Ashteh. It's over."*, *"Dude has lost it bro"*. |
| **Reel 04** | `19:18` | `20:15` | `1158` | `1215` | 57s | Harish friend conversation. Vulgarity censorship applied: `N***A`, `F**K`. *"Just having... having the person"*, *"Eating them or what?!"*, *"Bro I'll kill you bro! Shanthanooo!"*. |
| **Reel 05** | `22:25` | `22:53` | `1345` | `1373` | 28s | **Corrected range** (User clarified: `22:25 - 22:53`). Kanglish dialogue: *"Thale novu ya... (headache bro)"*, *"Hange hange... nange... sumne iri!"*, *"Bro you actually got da"*, *"Illa lo, I stopped from so long bro"*, *"He has lost his mind because he doesn't have hugs!"*. |
| **Reel 06** | `23:53` | `24:01` | `1433` | `1441` | 8s | Kanglish Chappar punchline: *"Andhre even I'm chappar, even you're chappar, so together let's be chappar! Right? What is he saying bro I've lost it!"*. 100% Chappar sticker badge overlay. |
| **Reel 07** | `24:15` | `24:40` | `1455` | `1480` | 25s | Non-penetrative counting comedy: *"Non-pene also... non-penetrative also!"*, *"Even with that you're zero?!"*, *"You didn't have to clarify that like that man!"*, *"You KO'd me exactly in-game and IRL!"*. |

---

## 2. Language & Multilingual Standards (Kanglish / Hinglish)

1. **Kanglish Accuracy**:
   - YouTube English auto-captions butcher regional languages by trying to map Indian languages to English phonetic words.
   - Always listen directly to the audio waveform to identify the authentic Kannada / Kanglish / Hinglish expressions.
   - Common glossary:
     - **Chappar** (not "chappri"): Local Kannada slang for cheap / tacky / cringe.
     - **Gothaa?**: Do you know? / Did you know?
     - **Anthe**: He/she says (reporting speech).
     - **Thale novu**: Headache.
     - **Sumne iri**: Stay quiet / keep calm.
     - **Illa lo**: No dude.
     - **Hange**: That's how / like that.
     - **Andhre**: That means / in other words.
     - **Bere level**: Different level / next level.
     - **PU**: Pre-University college.
     - **Da / Lo**: Bro / dude / homie.

---

## 3. Vulgarity & Censorship Policy

All explicit or vulgar terms are masked with their **first letter, last letter, and 2–3 stars in between**:
- `NIGGA` / `NIGGER` $\rightarrow$ `N***A`
- `FUCK` $\rightarrow$ `F**K`
- `FUCKING` $\rightarrow$ `F*****G`
- `FUCKED` $\rightarrow$ `F***ED`
- `DICK` $\rightarrow$ `D**K`
- `SHIT` $\rightarrow$ `S**T`
- `BITCH` $\rightarrow$ `B***H`
- `RETARDED` $\rightarrow$ `R******D`
- `CUNT` $\rightarrow$ `C**T`

---

## 4. Subtitle Pacing: Micro-Chunking (Preventing "Early" Text)

- **Rule**: Never show full multi-word sentences before the speaker has uttered them.
- **Pacing**: Display **1 to 2 words per card** (at most 3 short words).
- **Highlight**: Active spoken word highlighted in **Neon Yellow** (`&H002EFFFF`) with a 112% scale pop, while other words remain clean white (`&H00FFFFFF`).
- **Font**: `Impact` (meme punchiness) paired with `Segoe UI Emoji` for fallback glyphs.
- **Positioning**: Safe zone at vertical margin `550px` from bottom (well clear of Instagram caption and UI).

---

## 5. Gen-Z & Viral Meme Emojis

Use contextual emojis that amplify the comedic mood:
- 🥀 **Wilted / Bent Rose**: Down bad, crushed, defeated, hopeless romance.
- 💔 **Broken Heart**: Emotional damage, relationship banter.
- 💀 **Skull**: Dead / dying of laughter / extreme shock.
- 😭 **Sobbing / Crying Face**: Hilarious breakdown / can't stop laughing.
- 🚗 **Car**: Speeding / Mustang reference.
- 👽 **Alien**: Out of this world / strange appearance.
- 🎺 **Trumpet**: Random vocal noises / humming solo.

---

## 6. Visual Stickers / Photo Overlays

When a person or prominent subject is confirmed in the audio, a clean rounded card with an 8px white border appears centered above the subtitle:
1. **Reel 01**: Bonnie Blue portrait sticker (`bonnie_sticker.png`) at `t = 0.0s` to `3.5s`.
2. **Reel 02**: Ford Mustang muscle car sticker (`mustang_sticker.png`) at `t = 23.2s` to `27.5s`.
3. **Reel 06**: `100% CHAPPAR` badge (`chappri_sticker.png`) at `t = 0.0s` to `5.0s`.

---

## 7. Storage & Cleanup Policy

- **Always delete intermediate files**:
  - `reels/raw_*.mp4` (temporary raw cuts)
  - `reels/clip_*.ass` (subtitle scripts)
  - `reels/audio_*.mp3` (scratch audio files)
  - Any temporary `.png` / `.jpg` test files in workspace root.
- **Keep only**:
  - `reels/reel_01.mp4` through `reels/reel_07.mp4`
  - `make_reels.py` (production script)
  - Persistent sticker assets (`bonnie_sticker.png`, `mustang_sticker.png`, `chappri_sticker.png`)
  - `CLIPPER_CONTEXT.md` (this guide)
