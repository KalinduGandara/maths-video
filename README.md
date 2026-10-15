# Maths Explainer Video Studio

A [Claude Code](https://claude.com/claude-code) project for running a maths explainer channel. It plans the channel, then produces each video: animated with [Manim Community](https://www.manim.community/) and narrated by a local text-to-speech voice. Every video shares one visual theme (**Neon Pulse**) and one calm narrator, so the channel looks and sounds consistent.

## How it works

Two Claude Code skills:

| Skill | Role |
|---|---|
| `/channel-planner` | Strategist and content manager. Asks for the target audience, region and goals, researches competitors, demand and monetization rules, and writes a strategy, an idea backlog, an upload calendar and per-video briefs in `channel/`. Reviews analytics and updates the plan. |
| `/manim-video` | Producer. Turns a brief or a maths question into a finished video: research → script → **independent script review** → narration → Manim scene → render → **independent QA** → publish kit. |

The two review gates are Claude Code workflows in `.claude/workflows/`:
- **`video-script-review`**: five independent reviewers (maths solution, step-by-step rigour, clarity, hook and tone, narration). No animation code is written until they approve.
- **`video-qa`**: three reviewers check pronunciation (a Whisper round trip), theme compliance and visual quality, and picture-narration sync.

The narration is generated first, and its real word timings drive the animation (`self.cue(segment, "phrase")`), so the picture stays locked to the voice.

## Output per video

`videos/NNN-<slug>/` contains:

| File | What |
|---|---|
| `timeline.json` | Source of truth: segments, narration, animation plan, timings, chapters |
| `research.md`, `script.md` | Sources and chosen method; the script, timeline table and review log |
| `scene.py` | Themed Manim code (`VideoScene` + `Thumbnail`) |
| `<slug>.mp4` | Video only |
| `audio/narration.wav`, `audio/<segment>.wav`, `dialogue.srt` | Audio only, aligned to the video, plus subtitles |
| `<slug>_narrated.mp4` | Video and narration combined |
| `thumbnail.png`, `publish.md`, `chapters.txt` | Upload kit: titles, description, chapters, tags |

Rendered media is gitignored; everything can be rebuilt from the committed sources.

## Setup (macOS)

```bash
brew install ffmpeg espeak-ng          # plus MacTeX / TeX Live for LaTeX maths
python3.10 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

The Kokoro-82M voice model and the Whisper `small.en` model download from Hugging Face on first use.

## Usage

Open the project in Claude Code, then:

```
/channel-planner                                  # plan the channel and write briefs
/manim-video channel/briefs/001-<slug>.md         # produce a video from a brief
/manim-video <a maths question or concept>        # or straight from a question
```

`CLAUDE.md` has the full command reference and the project rules.

## Layout

```
theme/          Neon Pulse theme (theme.py tokens and helpers, THEME.md spec, preview.png)
tts/            srt_to_voice.py (Kokoro narrator), check_pronunciation.py, voice.json (channel voice)
.claude/        skills (manim-video, channel-planner) and review workflows
channel/        channel plan and briefs (created by /channel-planner)
videos/         one folder per video
```
