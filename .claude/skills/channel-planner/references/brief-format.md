# Video brief format

A brief is the hand-off from `/channel-planner` to `/manim-video`. It holds everything needed to produce and publish one video. `/manim-video` reads it in Step 1, uses the audience, hook and outline for the script, the thumbnail concept for `Thumbnail`, and the packaging fields for `publish.md`.

File: `channel/briefs/NNN-<slug>.md` (NNN and slug match the future `videos/NNN-<slug>/` folder).

```markdown
# NNN · <working title>

**Status:** brief ready · **Series:** <series name> · **Pillar:** <pillar>
**Format:** long-form, <target length, e.g. 5–7 min> (+ Short) · **Audience:** <level, region>
**Upload slot:** <weekday date, time + timezone of the audience> (<user's local time>)

## Problem
<exact statement, including answer options if any>
**Source:** <competition/book/exam, year, question number> (URL)
**Answer (pre-checked):** <answer>, verified by <method / Python check>

## Why this video
<evidence: outlier videos, search demand, comments asking for it, exam timing; links>

## Angle
<what this video does that others don't; the method chosen and why it suits this audience>

## Hook (first 10 s)
- **Opening visual:** <what's on screen in the first 2 s>
- **Question:** <the one specific question>
- **Open loop:** <the honest surprise, tension or stake>
- **Narration draft:** "<15–30 words>"

## Outline
1. <beat> (≈ time)
2. <beat>
...
- **Key insight:** <the aha moment>
- **Sanity check:** <estimate, special case, picture>
- **Outro / CTA:** <follow-up question or teaser, one plain call to action>

## Packaging
- **Upload titles:** 1) <primary> 2) <alt> 3) <alt>. Honest, ≤ 60 characters, with the search phrase early.
- **On-screen title:** <plain, 2 to 6 words, title case>
- **Thumbnail:** <hero visual> + text "<≤ 4 words>"; layout <left text / right figure>; colours <theme roles>
- **Description draft:** <first 2 lines with the search phrase; credit the source>
- **Tags:** <8 to 15 search phrases>
- **Hashtags:** <3 to 5>
- **Pinned comment:** <a genuine question to start discussion>
- **Playlist:** <name>

## Shorts cut
<a 30 to 50 s version: its own first-second hook, which beats to keep, and the end card pointing to the full video>

## Notes for production
<misconceptions to address, visuals that must appear, pronunciation risks (names, letters), anything to avoid>
```
