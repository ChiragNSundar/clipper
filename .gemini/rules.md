# Clipper Video Production, Architecture & Transcription Rules

## 1. Zero-Pollution Workspace Architecture (STRICT)
- **NEVER create one-off scratch scripts** (e.g. `test_*.py`, `check_*.py`, `transcribe_*.py`, `build_*.py`, `part*.wav`) in the project repository root.
- **Always use the Universal Engine**: Modify only `clipper/` modules (`config.py`, `layouts.py`, `engine.py`, `subtitles.py`, `transcribe.py`) and invoke through `clipper.py` CLI or library calls.
- **All temporary processing MUST use `tempfile.TemporaryDirectory()`**:
  - Sliced video segments, audio extracts, temporary frames, and intermediate `.ass` files must live strictly in memory or in isolated system temp directories.
  - Zero intermediate files should ever appear in VS Code's file tree or trigger untracked Git markers.
- **Only Final Deliverables**: The only allowed new files are final rendered `.mp4` reels placed in `reels/`.

## 2. High-Precision Transcription Protocol (How to Get 100% Subtitle Accuracy)
Speech models like Whisper `base` will catastrophically hallucinate on overlapping voices, game audio, laughter, and Indian regional accents unless this exact protocol is followed:
1. **Contextual Prompt Priming**: Always pass an `initial_prompt` with the authentic vocabulary, actual usernames from the Discord overlay (e.g., `Lucid`, not `Lucy`), and regional slang (e.g., `idyella`, `yaaro idyella`, `mute mado`, `chappar`). This shifts the model's language prior probability toward the actual terms.
2. **Model Scaling for Difficult Audio**: When speech is quiet, accented, or overwhelmed by loud game SFX, use Whisper `medium` (or `small`). Fast `base` models should only be used on clear solo studio audio.
3. **Word-Level Onset Alignment**: Always transcribe with `word_timestamps=True` on isolated speech sections. Group subtitles into 1-2 words per event locked to physical acoustic onsets. Never display words before they are spoken.
4. **Speaker Attribution & Punchline Framing**: In banter or roast videos, attribute sudden speaker shifts (e.g., `[GIRL]: "N***A, SHUT THE F**K UP!"`) and the reaction (`SHE TOLD... "N***A, SHUT THE F**K UP", YO!`) to preserve the comedic timing and context.
5. **Zero-Tolerance for Phonetic English Forcing**: Never let the model force Kannada/Hindi/Tamil into English.
   - `yaaro idyella` -> never `ididyhalla` or `did he holler`
   - `Lucid` -> never `Lucy` or `Blue`
   - `Mute mado` -> never `4 mutes` or `mute made`
   - `Chappar` -> never `chappri`
   - `Raze` -> never `raised`
   - `into your mom` -> never `into your mouth`

## 3. Subtitle Pacing, Styling & Safe Zones
- **Font & Sizing**: `Impact` font, size 74-78, 8px black outline, 3px shadow.
- **Pop Highlight**: Active spoken word pops in Neon Yellow (`&H002EFFFF`) with 115% scale (`\fscx115\fscy115`).
- **Emoji DirectWrite Fallback**: All emojis wrapped in `{\fnSegoe UI Emoji}`.
- **Vertical Safe Margins**:
  - Standard Center / Split: `MarginV: 360` to `450` from bottom.
  - Subtitles must NEVER overlap either the top game video, the center Discord voice card, or the bottom Instagram engagement UI buttons.

## 4. Censorship Rules
- Mask vulgar words using first letter, last letter, and asterisks:
  `DICK` -> `D**K`, `SHIT` -> `S**T`, `FUCK` -> `F**K`, `NIGGA` -> `N***A`, `RETARDED` -> `R******D`, `BITCH` -> `B***H`.

## 5. Universal Layout Presets
- `center`: 9:16 center crop with optional dynamic popping sticker.
- `ambient`: Blurred 9:16 background with centered 16:9 feed.
- `split`: Valorant cards + Discord overlay + top banner header.
- `discord_game`: 16:9 gameplay at top (`y = 130-670`), enlarged Discord voice overlay card in center (`y = 695-1201`), subtitles in bottom safe margin (`MarginV: 360`).

## 6. Comedic Timing, Sound Effects & Visual Effects
- **Layered Sound Effects (`sfx/`)**:
  - Reusable comedic SFX (e.g. `sfx/vine_boom.mp3`) are stored in `sfx/`.
  - When layering under speech, maintain balanced volume (`volume=0.35` to `0.45`) and use `normalize=0` with `amix` to prevent audio ducking or speech clipping.
  - Place boom sound effects during awkward silences, sudden reveals, or sus moments.
- **Dynamic Snap-Zooms (`--zoom`)**:
  - For visual punchlines (e.g. characters in sus poses), use `--zoom "start-end:w:h:x:y"` to zoom in tightly for the punchline duration (typically 2-4 seconds).
- **Meta-Subtitle Annotations**:
  - When deadpan silence or an awkward pause occurs between dialogue, annotate it in subtitles between asterisks (e.g. `*AWKWARD SILENCE*... 💀🗿`).

