# Script & timeline formats

## timeline.json (source of truth)

```json
{
  "title": "Solving 3x + 5 = 11",
  "slug": "linear-equation-basics",
  "words_per_second": 2.5,
  "segments": [
    {
      "id": "s01_hook",
      "section": "Hook",
      "chapter": "The problem",
      "start": 0.0,
      "end": 7.0,
      "dialogue": "What number, tripled and then increased by five, gives you eleven?",
      "animation": "Title card writes in. A mystery box labelled x appears, multiplied by 3, plus 5, arrow to 11.",
      "on_screen": ["Title: Solving 3x + 5 = 11", "box(x) × 3 + 5 → 11"]
    },
    {
      "id": "s02_setup",
      "section": "Setup",
      "start": 7.0,
      "end": 13.5,
      "dialogue": "Let's write that as an equation. Three x plus five equals eleven.",
      "animation": "Box morphs into MathTex 3x + 5 = 11; 'x' coloured PRIMARY.",
      "on_screen": ["3x + 5 = 11"]
    }
  ]
}
```

Rules:
- `id`: `sNN_short_name`, unique, in order. The scene method is named `seg_<id>`.
- `start` of each segment == `end` of the previous one. The first segment starts at 0.0.
- `end - start` ≥ `words / words_per_second + 0.8`. Round to 0.5 s. This is only the planning rate: once the voice exists (`voice_timing.json`), each slot must hold the real clip plus 0.6 s, and `timeline_tool.py fit` enforces that.
- `chapter` (optional): starts a YouTube chapter at this segment's start, with this name. Put one on the first segment, then one at each signpost, 45 to 90 s apart. Use plain names: "The problem", "Join the centres", "Solve for x", "Check".
- `dialogue`: only the exact words the TTS voice will speak. Write maths the way it is spoken. An empty string `""` is allowed for a silent visual beat.
- `animation`: a concrete description of what the scene code does: objects, transforms, colours (as theme roles), and the order things happen.
- `on_screen` (optional): the text and maths that should be visible, used as a checklist when writing code.
- Optional per-segment `"pause_after": 1.0` is only documentation. Build the pause into `end` itself.

Commands:
- `timeline_tool.py check <dir>` validates the file.
- `timeline_tool.py retime <dir>` recomputes start/end contiguously, and extends any segment that is too short for its words. Use it after editing dialogue.
- `timeline_tool.py fit <dir>` (after the voice is generated) grows segments to the real clip lengths and re-exports.

## script.md (human-readable)

```markdown
# <Title>

**Concept:** one-paragraph summary of what the viewer will learn.
**Audience:** <level> · **Duration:** m:ss · **Theme:** <Theme Name>

**Hook:** the one-sentence open loop · **Brief:** channel/briefs/NNN-slug.md (or "none")

## Corrections to the rough script
- <what was wrong/unclear and how it was fixed, or "None">

## Timeline

| # | Time | Section | Narration (TTS) | Animation |
|---|------|---------|-----------------|-----------|
| 1 | 00:00–00:07 | Hook | What number, tripled... | Title card writes in; mystery box... |
| 2 | 00:07–00:13.5 | Setup | Let's write that... | Box morphs into 3x + 5 = 11... |

## Full narration
<all dialogue as continuous prose, for reading aloud / review>

## Review log
- Script review round 1: <scores per lens>; <what was changed>; approved yes/no
- QA round 1: <result>; <what was fixed>
```

## research.md

```markdown
# Research: <problem>

## Source
<competition / book / exam, year, question number, exact statement, options, official answer> (URL)

## Methods compared
| Method | Steps | Visual? | Audience fit | Notes |
|---|---|---|---|---|
| Coordinates + distance equations | 7 | yes | high school | all algebra is routine |
| Descartes' circle theorem | 1 | no | needs the theorem | good teaser |

**Chosen:** <method> because <reason>. **Teaser/alternative:** <method>.

## Misconceptions to address
- <common mistake> → addressed in segment <id>

## Existing videos and gap
- <channel, title, views, URL>: <angle, weaknesses, what commenters ask>
- **Our angle:** <what this video does better or differently>

## Sources
- <title> (URL)
```

## publish.md

```markdown
# Publish: <slug>

**Upload title:** <from the brief; honest, searchable, ≤ 60 characters>
**Alternatives:** <title 2> / <title 3>
**Upload slot:** <day, local time, timezone> · **Playlist/series:** <name>
**Thumbnail:** thumbnail.png, text "<≤ 4 words>"

## Description
<2-line summary with the main search phrase in the first sentence>

Chapters:
<contents of chapters.txt>

<credit to the problem source> · <related video links>
<3 to 5 hashtags>

## Tags
<comma-separated search phrases>

## Pinned comment
<a genuine question that invites answers, e.g. which method viewers used>

## Shorts cut
<segment ids or a 30 to 50 s hook-to-answer idea, with its own first-second hook>
```

## Writing good narration

- One idea per segment. Most segments are 4–15 s long.
- Say what's about to appear just before it appears, or while it appears. Never say it after.
- Use the same name for a thing throughout. If you call it "the discriminant" once, keep calling it that.
- Pronunciations for TTS: "x squared", "x to the fourth", "the square root of", "a over b", "sine", "cos", "tan", "pi", "theta", "plus or minus", "is approximately".
- Leave a silent beat (an empty-dialogue segment of 1–2 s) after the key insight and after the final answer.
