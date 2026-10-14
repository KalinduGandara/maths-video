# Maths explainer videos

This project produces narrated maths explainer videos (problem walkthroughs, concept explainers) with [Manim Community](https://www.manim.community/) and a local text-to-speech narrator. Every video lives in its own folder and shares one visual theme and one narrator voice, so the videos look and sound like one channel.

## How a video is made

Use the `/manim-video` skill (`.claude/skills/manim-video/SKILL.md`). It runs the full pipeline:

1. **Solve and verify** the maths first.
2. **Timeline**: write `timeline.json` (segments with narration and the animation plan). Narration is budgeted at 2.5 words/s.
3. **Export dialogue**: produce `dialogue.srt/.txt/.json` from the timeline.
4. **Scene**: write `scene.py`, where each segment is a `seg_<id>()` method ending in `self.sync(id)` so the picture stays locked to the narration timestamps.
5. **Render** to `<slug>.mp4` and verify the length against the timeline.
6. **Narrate**: run `tts/srt_to_voice.py` to speak `dialogue.srt` and mux it into `<slug>_narrated.mp4`.

## Layout

| Path | What |
|---|---|
| `theme/theme.py` | **Neon Pulse** theme: colour role tokens, fonts, helpers (`heading`, `math`, `glow`, `pulse_bar`, `tag`, `result_box`, ...) and `ThemedScene` with timeline sync. |
| `theme/THEME.md` | Theme spec and approval status (approved; change it only when the user asks). |
| `tts/srt_to_voice.py` | SRT → voice tool. It uses Kokoro-82M locally, writes per-segment clips and `narration.wav`, and `--mux` combines them with the video. |
| `tts/voice.json` | The fixed channel narrator (voice `af_heart`, speed 0.95, loudness target, pronunciation rules). Changing it changes every future video. |
| `videos/NNN-<slug>/` | One video: `timeline.json` (source of truth), `script.md`, `dialogue.*`, `scene.py`. Renders (`*.mp4`, `media/`, `audio/`) are gitignored. |
| `.claude/skills/manim-video/` | Skill instructions, references and `scripts/timeline_tool.py` (`check`, `retime`, `export`, `verify`, `mux`). |

## Commands

```bash
export PATH="/usr/local/texlive/2026/bin/universal-darwin:$PATH"     # LaTeX for MathTex
D=videos/001-semicircle-chord-area
.venv/bin/python .claude/skills/manim-video/scripts/timeline_tool.py check  $D
.venv/bin/python .claude/skills/manim-video/scripts/timeline_tool.py export $D
.venv/bin/manim -ql --media_dir $D/media $D/scene.py VideoScene   # draft
.venv/bin/manim -qh --media_dir $D/media $D/scene.py VideoScene   # final 1080p, then copy to $D/<slug>.mp4
.venv/bin/python .claude/skills/manim-video/scripts/timeline_tool.py verify $D
.venv/bin/python tts/srt_to_voice.py $D --mux                     # narration + <slug>_narrated.mp4
```

## Setup

- Python 3.10 venv at `.venv`: `pip install -r requirements.txt`
- System: `brew install ffmpeg espeak-ng`, TeX Live 2026 (MacTeX)
- The Kokoro weights download from Hugging Face on first TTS run.

## Rules

- Scene files never hard-code colours or fonts. Use the theme tokens and helpers; add new ones to `theme/theme.py` without renaming existing ones.
- `timeline.json` is the source of truth. When editing a video, change it first, then run `check` and `export`, update `scene.py`, re-render and re-narrate.
- Narration is written for the ear: spoken maths ("R squared", "one half pi"), no symbols or LaTeX. Fix mispronunciations in `tts/voice.json` → `pronunciations`, not by misspelling the script.
- If a narration clip overruns its segment, lengthen the segment rather than speeding up the voice.
