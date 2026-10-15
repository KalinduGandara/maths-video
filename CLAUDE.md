# Maths explainer videos

This project produces narrated maths explainer videos (problem walkthroughs, concept explainers) with [Manim Community](https://www.manim.community/) and a local text-to-speech narrator. Every video lives in its own folder and shares one visual theme and one narrator voice, so the videos look and sound like one channel.

## How the channel works

Two skills work together:

- **`/channel-planner`** (`.claude/skills/channel-planner/`) is the strategist and content manager. It asks for the audience, region and goals, researches the market and monetization rules, and writes `channel/` (profile, research, strategy, idea backlog, calendar, and one production brief per video in `channel/briefs/`). Given analytics, it reviews and updates the plan.
- **`/manim-video`** (`.claude/skills/manim-video/`) turns a brief or a question into a finished video:
  1. **Research** the problem and solution methods, then write `research.md`. **Solve and verify** with Python.
  2. **Script**: `timeline.json` + `script.md`, following `references/style-guide.md` (calm, professional tone, plain titles, a real hook).
  3. **Script review gate**: the `video-script-review` workflow (`.claude/workflows/`). Five independent reviewers cover the maths, the steps, clarity, the hook and tone, and the narration. No `scene.py` is written until they approve.
  4. **Narration first**: `tts/srt_to_voice.py` writes the clips and `voice_timing.json` (real word times); `tts/check_pronunciation.py` checks them; `timeline_tool.py fit` sizes the segments to the real voice.
  5. **Scene**: `scene.py`, with `self.cue(id, "phrase")` locking each animation to the spoken word and `self.sync(id)` ending each segment.
  6. **Render**, then `verify`, `frames`, and `mux`. The outputs are a silent video, separate audio, and a combined file.
  7. **QA gate**: the `video-qa` workflow (pronunciation, theme and visuals, picture-narration sync), then `publish.md` and `thumbnail.png`.

## Layout

| Path | What |
|---|---|
| `theme/theme.py` | **Neon Pulse** theme: colour role tokens, fonts, helpers (`heading`, `math`, `glow`, `pulse_bar`, `tag`, `result_box`, ...) and `ThemedScene` with timeline sync. |
| `theme/THEME.md` | Theme spec and approval status (approved; change it only when the user asks). |
| `tts/srt_to_voice.py` | SRT → voice tool. It uses Kokoro-82M locally and writes per-segment clips, `narration.wav` and `voice_timing.json` (clip lengths and word times). |
| `tts/check_pronunciation.py` | Whisper round trip: transcribes the clips and diffs them against the script, with phonemes → `review/pronunciation.json`. |
| `tts/voice.json` | The fixed channel narrator (calm male voice `am_michael`, speed 0.9, loudness target, pronunciation rules). Changing it changes every future video. |
| `videos/NNN-<slug>/` | One video: `timeline.json` (source of truth), `research.md`, `script.md` (with the review log), `dialogue.*`, `chapters.txt`, `voice_timing.json`, `scene.py`, `publish.md`. Renders (`*.mp4`, `thumbnail.png`, `media/`, `audio/`, `review/`) are gitignored. |
| `channel/` | Channel plan from `/channel-planner`: `profile.md`, `research.md`, `strategy.md`, `ideas.md`, `calendar.md`, `briefs/`, `log.md`. |
| `.claude/skills/manim-video/` | Skill instructions; references (`style-guide.md`, `review-rubric.md`, formats, patterns); `scripts/timeline_tool.py` (`check`, `retime`, `export`, `fit`, `verify`, `frames`, `mux`) and `scripts/theme_lint.py`. |
| `.claude/workflows/` | `video-script-review.js` and `video-qa.js`: the independent review gates. |

## Commands

```bash
export PATH="/usr/local/texlive/2026/bin/universal-darwin:$PATH"     # LaTeX for MathTex
D=videos/001-example                                                # the video folder (NNN-slug)
T=.claude/skills/manim-video/scripts/timeline_tool.py
.venv/bin/python $T check  $D
.venv/bin/python $T export $D                                      # dialogue.* + chapters.txt
.venv/bin/python tts/srt_to_voice.py $D                            # clips + voice_timing.json
.venv/bin/python tts/check_pronunciation.py $D                     # ASR round trip
.venv/bin/python $T fit $D                                         # size segments to the real voice
.venv/bin/python .claude/skills/manim-video/scripts/theme_lint.py $D
.venv/bin/manim -ql --media_dir $D/media $D/scene.py VideoScene   # draft
.venv/bin/manim -qh --media_dir $D/media $D/scene.py VideoScene   # final 1080p, then copy to $D/<slug>.mp4
.venv/bin/python $T verify $D
.venv/bin/python $T frames $D                                      # review stills
.venv/bin/python $T mux $D                                         # audio/narration.wav + <slug>_narrated.mp4
```

## Setup

- Python 3.10 venv at `.venv`: `pip install -r requirements.txt`
- System: `brew install ffmpeg espeak-ng`, TeX Live 2026 (MacTeX)
- The Kokoro weights and the Whisper model (`small.en`) download from Hugging Face on first use.

## Rules

- Scene files never hard-code colours or fonts. Use the theme tokens and helpers; add new ones to `theme/theme.py` without renaming existing ones.
- `timeline.json` is the source of truth. When editing a video, change it first, then run `check` and `export`, re-voice and `fit`, update `scene.py`, re-render and `mux`.
- No `scene.py` before the script passes `video-script-review`; no video is reported done before it passes `video-qa`.
- Tone is calm and professional (`style-guide.md`): plain titles, no hype or cheeky wording, an honest hook.
- Narration is written for the ear: spoken maths ("R squared", "one half pi"), no symbols or LaTeX. Fix mispronunciations in `tts/voice.json` → `pronunciations`, not by misspelling the script.
- The voice is never sped up. If a clip overruns its segment, `timeline_tool.py fit` lengthens the segment.
- Time animations to the voice with `self.cue(id, "phrase")`, not with estimated offsets.
