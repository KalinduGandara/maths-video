---
name: manim-video
description: Turn a maths question, concept, or rough script into a complete Manim explainer video — an improved narration script with a timeline, per-segment animation plan, timestamped TTS dialogue (SRT/TXT/JSON), and themed Manim Python code rendered to MP4. Creates and gets approval for a unique visual theme on first run, then always reuses it. Use when the user says "make a maths video", "manim video", "animate this concept", gives a maths problem/concept with a rough script, or invokes /manim-video.
---

# Manim Maths Video Builder

Produces one complete, narrated-ready maths video per request. Every video lives in its own folder; all videos share one approved visual theme.

## Paths (project root = `/Users/kalindu/MyWork/maths`)

| What | Where |
|---|---|
| Shared theme (code) | `theme/theme.py` |
| Theme description + approval status | `theme/THEME.md` |
| Theme preview still | `theme/preview.png` |
| Per-video folder | `videos/NNN-<slug>/` (NNN = next 3-digit number, slug = kebab-case topic) |
| Helper tool | `.claude/skills/manim-video/scripts/timeline_tool.py` |
| Python / manim | `.venv/bin/python`, `.venv/bin/manim` |

Always prefix render commands with the LaTeX path:
```bash
export PATH="/usr/local/texlive/2026/bin/universal-darwin:$PATH"
```

## Workflow

### Step 0 — Theme check (every run)

1. If `theme/THEME.md` exists and contains `status: approved` → read `theme/THEME.md` and `theme/theme.py` and go to Step 1. Never change the theme silently; only change it if the user asks.
2. Otherwise (first run, or theme not yet approved) → **create a unique theme**:
   - Read `references/theme-guide.md` and `references/theme_template.py`.
   - Invent an original, cohesive identity (name, palette, fonts, motion style, layout rules). Do not reuse manim defaults (black bg + YELLOW/BLUE) or the template's placeholder colours.
   - Write `theme/theme.py` (from the template, all values filled in) and `theme/THEME.md` with `status: pending`.
   - Render the preview: `.venv/bin/manim -qm -s --media_dir theme/media theme/theme.py ThemePreview -o preview` then copy the resulting PNG to `theme/preview.png`. Read the PNG to check it visually.
   - Show the user the preview and a short summary (name, palette with hex codes, fonts, motion feel), then ask with AskUserQuestion: Approve / Tweak (they describe changes) / Generate a completely different theme.
   - Iterate until approved, then set `status: approved` and the approval date in `theme/THEME.md`.
   - Don't start the video until the theme is approved.

### Step 1 — Understand the input

The user gives a question/concept and maybe a rough script. Work out:
- The maths itself. **Solve or verify it yourself first**, step by step. If the rough script has an error or typo, fix it and tell the user what you changed.
- Audience level (ask once only if it's really unclear; default: high-school / early university).
- Any length or style the user asked for. If none, the length comes from the content (Step 2).

### Step 2 — Write the improved script and timeline

Read `references/script-format.md` for the exact formats. Build the video from **segments**. Each segment has one narration line (or a few sentences) and the animations that play during it.

Story structure (adapt as needed):
1. **Hook** (5–15 s): a question or visual that makes people curious.
2. **Setup**: state the problem or concept, define notation.
3. **Build-up / steps**: one idea per segment, and each step is shown on screen.
4. **Key insight**: the "aha" moment, with a visual emphasis.
5. **Result**: the final answer, boxed/highlighted.
6. **Recap + outro** (10–20 s): summary of the method, plus an optional teaser.

Timing rules (these make the video long enough to cover the whole script):
- Narration speed: **2.5 words/second** (≈150 wpm). Segment duration = `max(words / 2.5 + 1.0, animation time needed)`, rounded up to 0.5 s.
- Add a 0.5–1.5 s visual "breath" after important results.
- The total video length = sum of the segments. Never cut narration to hit a length. If the user gave a target length, adjust how deep the content goes instead.
- Dialogue must be written for the ear: short sentences, spell out symbols the way they're spoken ("x squared", "sine of five x", "pi over ten"), no LaTeX, no markdown, no emoji.

Create the folder `videos/NNN-<slug>/` and write:
- `timeline.json`: the single source of truth (schema in `references/script-format.md`).
- `script.md`: the human-readable improved script: title, summary, a timeline table (time range | narration | on-screen animation), and notes on any corrections.

Then run:
```bash
.venv/bin/python .claude/skills/manim-video/scripts/timeline_tool.py check videos/NNN-<slug>
```
This validates the timeline: contiguous timestamps, no gaps or overlaps, and narration that fits each segment at 2.5 w/s. Fix any errors and re-run until it passes.

### Step 3 — Export TTS dialogue

```bash
.venv/bin/python .claude/skills/manim-video/scripts/timeline_tool.py export videos/NNN-<slug>
```
This writes into the video folder:
- `dialogue.srt`: standard subtitles with timestamps (works with most TTS/subtitle tools)
- `dialogue.txt`: `[00:00.000 - 00:06.500] text` lines, easy to read and paste
- `dialogue.json`: `[{id, start, end, duration, text}]` for scripted TTS pipelines

Re-run the export any time `timeline.json` changes.

### Step 4 — Write the Manim code

Write `videos/NNN-<slug>/scene.py`. Read `references/scene-patterns.md` first. Required rules:
- Import the theme. **Never hard-code colours, fonts, or backgrounds**. Use only `theme.py` tokens and helpers:
  ```python
  import sys, pathlib
  sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))  # project root
  from theme.theme import *
  ```
- One scene class `VideoScene(ThemedScene)`. It loads the timeline with `self.load_timeline(__file__)`.
- Each segment is one method `seg_<id>()`. Each method finishes with `self.sync(<segment id>)`, which waits until that segment's end timestamp. That way the animation matches the dialogue timestamps exactly. If a segment's animations run longer than its slot, `sync` raises an error: lengthen the segment in `timeline.json` (and re-export), or speed up the animations.
- Clear or transform old objects between sections so the screen never gets cluttered. Keep everything inside the safe area (`SAFE_W`, `SAFE_H` from the theme).
- Use `MathTex` with split substrings and `TransformMatchingTex` for algebra steps. Use axes/graphs/geometry when the concept is visual. Show, don't just write.

### Step 5 — Render and verify

```bash
export PATH="/usr/local/texlive/2026/bin/universal-darwin:$PATH"
cd /Users/kalindu/MyWork/maths
.venv/bin/manim -ql --media_dir videos/NNN-<slug>/media videos/NNN-<slug>/scene.py VideoScene   # fast draft
```
- Fix any errors. For layout checks, render stills of key moments (`-s` with `--from_animation_number`) and look at them with Read: check for overlaps, text off screen, and readability.
- Once the draft works, render the final at 1080p: `-qh` (or `-qk` for 4K if the user asks).
- Copy the final MP4 to `videos/NNN-<slug>/<slug>.mp4`.
- Verify the length: `.venv/bin/python .claude/skills/manim-video/scripts/timeline_tool.py verify videos/NNN-<slug>` (compares the MP4 duration with the timeline total, ±0.5 s).

### Step 6 — Add the narration (channel voice)

Generate the voice-over with the project's fixed narrator (Kokoro-82M, settings in `tts/voice.json`; never change voice/speed per video, so all videos sound the same) and combine it with the video:
```bash
.venv/bin/python tts/srt_to_voice.py videos/NNN-<slug> --mux
```
This writes `audio/<id>.wav` per segment, `audio/narration.wav`, and `<slug>_narrated.mp4`. It prints each clip's length vs its slot; a clip that doesn't fit is re-spoken faster (up to `max_speed`), and if it still doesn't fit, lengthen that segment in `timeline.json`, re-render, and re-run. If a word is mispronounced (e.g. point letters like "A B"), add a rule to `pronunciations` in `tts/voice.json` rather than misspelling the script.

Alternatively, if the user supplies their own TTS audio, either one file per segment as `audio/<id>.mp3|wav`, or one full narration file `audio/narration.mp3`, run:
```bash
.venv/bin/python .claude/skills/manim-video/scripts/timeline_tool.py mux videos/NNN-<slug>
```
This places each clip at its segment start time and writes `<slug>_narrated.mp4`. If a clip is longer than its segment, the tool warns: lengthen that segment, re-render, and re-mux.

### Step 7 — Report

Tell the user briefly:
- the folder path and final video path, and the total duration
- the narrated video (`<slug>_narrated.mp4`) and the dialogue files (`dialogue.srt` / `dialogue.txt` / `dialogue.json`)
- any maths corrections made to their rough script

## Final folder layout

```
videos/NNN-<slug>/
├── script.md          # improved script + timeline table
├── timeline.json      # source of truth: segments, dialogue, animations, times
├── dialogue.srt       # TTS / subtitles
├── dialogue.txt
├── dialogue.json
├── scene.py           # themed Manim code
├── <slug>.mp4         # final render
├── audio/             # (optional) user's TTS clips
└── media/             # manim build cache
```

## Editing an existing video

If the user asks for changes to an existing video, edit `timeline.json` first, then re-run `check` and `export`, then update `scene.py`, then re-render. Keep script, dialogue, and video in sync.
