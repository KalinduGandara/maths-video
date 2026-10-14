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
- `end - start` ≥ `words / words_per_second + 0.8`. Round to 0.5 s.
- `dialogue`: only the exact words the TTS voice will speak. Write maths the way it is spoken. An empty string `""` is allowed for a silent visual beat.
- `animation`: a concrete description of what the scene code does: objects, transforms, colours (as theme roles), and the order things happen.
- `on_screen` (optional): the text and maths that should be visible, used as a checklist when writing code.
- Optional per-segment `"pause_after": 1.0` is only documentation. Build the pause into `end` itself.

Commands:
- `timeline_tool.py check <dir>` validates the file.
- `timeline_tool.py retime <dir>` recomputes start/end contiguously, and extends any segment that is too short for its words. Use it after editing dialogue.

## script.md (human-readable)

```markdown
# <Title>

**Concept:** one-paragraph summary of what the viewer will learn.
**Audience:** <level> · **Duration:** m:ss · **Theme:** <Theme Name>

## Corrections to the rough script
- <what was wrong/unclear and how it was fixed, or "None">

## Timeline

| # | Time | Section | Narration (TTS) | Animation |
|---|------|---------|-----------------|-----------|
| 1 | 00:00–00:07 | Hook | What number, tripled... | Title card writes in; mystery box... |
| 2 | 00:07–00:13.5 | Setup | Let's write that... | Box morphs into 3x + 5 = 11... |

## Full narration
<all dialogue as continuous prose, for reading aloud / review>
```

## Writing good narration

- One idea per segment. Most segments are 4–15 s long.
- Say what's about to appear just before it appears, or while it appears. Never say it after.
- Use the same name for a thing throughout. If you call it "the discriminant" once, keep calling it that.
- Pronunciations for TTS: "x squared", "x to the fourth", "the square root of", "a over b", "sine", "cos", "tan", "pi", "theta", "plus or minus", "is approximately".
- Leave a silent beat (an empty-dialogue segment of 1–2 s) after the key insight and after the final answer.
