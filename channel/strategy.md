# Channel strategy

_Written 2026-10-15 from `profile.md` and `research.md`. Review after week 8 (`log.md`)._

## Positioning

**Real olympiad problems, explained so anyone can follow.** Calm, animated 8–12 minute walkthroughs of genuine competition problems (IMO, Putnam, AMC, UKMT), each with an honest source. The explanation gives the idea behind each step, not just the algebra. Then the theorem behind the solution gets its own video.

Why this channel and not the others:
- The clickbait "olympiad" channels make up their sources and grind algebra.
- 3Blue1Brown and Mathologer make 30-minute videos a few times a year.
- Andy Math is face-cam puzzles in 5 minutes.
- The calm voice, the Neon Pulse animation and the "nothing skipped" standard fill the gap between them.

## Audience persona

- **"The curious adult" (primary):** 18–45, US/UK/EU. Did maths up to high school and liked puzzles. Watches on a phone or TV in the evening and at weekends. Wants the aha moment, not homework. Struggles with notation that isn't explained and with skipped steps.
- **"The ambitious student" (secondary):** 14–18, preparing for AMC/UKMT. Watches around competition dates. Wants methods they can reuse.

Every video is written for the first persona. The second is served by the honest sources and the theorem videos.

## Content pillars and series

| Pillar | Series name | Share | What |
|---|---|---|---|
| 1. Competition problems | **Olympiad Problems, Explained** | ~55% | One real problem per video, from statement to answer. A difficulty level appears on screen and in the description: **Level 1** (anyone), **Level 2** (careful thinking), **Level 3** (famous and hard). |
| 2. Theorems | **The Theorem Behind It** | ~20% | The tool used in an earlier problem: where it comes from, why it's true, and 2–3 short uses. It is scheduled once a problem video's comments and retention show interest. |
| 3. Puzzles and paradoxes | **Famous Puzzles, Properly Explained** | ~25% | Broad-appeal puzzles (Monty Hall, the birthday problem, coin rotation, viral disputes) explained carefully. These are the discovery engine for a general audience. |

**Seasonal layer** (inside pillar 1): one real problem from an exam that has just been sat: AMC in November, Putnam in December, BMO in January, IMO in July (plus the yearly AI-at-the-IMO story).

**The link between pillars:** every problem video closes with one plain line: "The idea that made this work is called the pigeonhole principle. If you'd like the full story of why it's true and where else it shows up, tell me in the comments." The theorem video then links back to the problem in its description, end screen and pinned comment. Playlists pair them.

## Format mix (capacity: 1 long + 2–3 Shorts a week)

- **Long-form:** 1 a week, **8–12 minutes** by default. That clears the 8-minute mid-roll threshold without padding. Level 1 problems may run 6–8 minutes if that is all the content needs; never pad.
- **Shorts:** 2–3 a week, cut from that week's long video, 30–50 seconds. Types: (a) hook + problem + "the answer is in the full video"; (b) one self-contained aha step; (c) the final reveal with a check. Each links to the long video with **Related video**.
- **Ratio:** about 1 long to 2.5 Shorts. Shorts are for discovery, not revenue: they pay little and won't count toward YPP watch hours.
- **Build a two-video buffer before launch** (001 and 002 finished), so a hard week never breaks the schedule.

## Packaging system

**Titles** (≤ 60 characters, honest, search phrase early). Formulas:
1. `<Specific question>? (<Competition> <Year>)`, e.g. "Can 10 Numbers Always Be Split Into Equal Sums? (IMO 1972)"
2. `The <Competition> Problem <Hook fact>`, e.g. "The IMO Problem You Can Solve With Socks"
3. `<Theorem>, Explained Simply` / `Why <surprising fact> Is True`
4. `<Famous puzzle>: The Clear Explanation`

Never use "Harvard", "only 1% can solve", made-up countries, "insane" or "genius".

**Thumbnail** (rendered from the scene's `Thumbnail` class):
- Background is the Neon Pulse backdrop (BG), with one hero figure on the right in PRIMARY/SECONDARY with `glow`.
- At most 4 words in FONT_HEADING on the left in TEXT. One word may be in HIGHLIGHT gold.
- A small `tag` pill in the top-left gives the level ("LEVEL 2") or the source ("IMO 1972").
- The text never repeats the title. Test readability at 160 × 90 px.

**Description template**
```
<Line 1: the problem in plain words with the search phrase>
<Line 2: source (competition, year, problem number) and difficulty level>

Chapters
00:00 The problem
...

The theorem behind it: <link or "coming soon — tell me if you want it">
Related problem: <link>

Problem source: <official/AoPS link>
Animated with Manim. Narration voice is AI-generated; the research, script and animation are original and human-reviewed.
#maths #olympiad #<topic>
```

**Tags:** 8–15 search phrases: the problem name, the competition and year, the theorem, "math olympiad problem", "math puzzle", "<topic> explained".

**Playlists:** one per series; one per theorem (the problem videos plus the theorem video); "Start Here: Level 1 Problems".

## Idea scoring

Each criterion is scored 1–5 and weighted. The total is out of 5.

| Criterion | Weight | 5 means |
|---|---|---|
| Demand (search and viral evidence) | 0.25 | Proven searches or a viral topic |
| Outlier evidence | 0.20 | A comparable video at ≥5× its channel median |
| Visual potential | 0.20 | The key idea is a picture or a motion |
| Audience fit (average person) | 0.20 | Followable with school maths |
| Evergreen | 0.05 | No date dependence |
| Production cost (inverse) | 0.10 | Simple 2D, short research |

## Schedule

All slots are set in Studio in **US Eastern**.

| Slot | US Eastern | US Pacific | UK | CET | Sri Lanka |
|---|---|---|---|---|---|
| Long-form, **Saturday** | 11:00 | 08:00 | 16:00 (15:00 on 31 Oct) | 17:00 (16:00 on 31 Oct) | 20:30 until 31 Oct, **21:30 from 7 Nov** |
| Shorts, **Tuesday and Thursday** (optional Sunday) | 12:00 | 09:00 | 17:00 | 18:00 | 22:30 (21:30 before 1 Nov) |

Upload as a normal scheduled video, not a Premiere. Re-check after 8–12 weeks against Studio's "When your viewers are on YouTube" report.

**Seasonal plan:**
- **Nov:** AMC problem the weekend after the 5 Nov sitting.
- **Dec:** a Putnam problem in the week after 5 Dec; holiday puzzles (birthday problem) late December, when CPMs peak.
- **Jan–Feb:** BMO and AMC 8 problems. February has the lowest CPMs, so it suits theorem videos.
- **Jul:** the IMO and AI-at-the-IMO video.
- **Summer:** education viewing dips, so build the buffer then.

## Retention standards (passed to every brief)

- The problem is on screen within 2 seconds; one specific question and an honest open loop by 10 seconds.
- First real insight by 60 seconds; a signpost or chapter every 45–90 seconds.
- Something changes on screen every 6–8 seconds.
- **Before solving, invite a pause:** "Pause here if you'd like to try it." Viewers who try watch longer.
- Pay off the hook explicitly, then a sanity check, then the theorem teaser, then end.

## Growth and monetization roadmap (estimates)

**YPP arithmetic:**
- 8,000 hours is 480,000 minutes.
- A 10-minute video at 45% average view duration earns about 4.5 minutes per view.
- That means about **107,000 long-form views within 12 months**: an average of about 2,000 views per video across ~52 videos, or fewer views plus one or two outliers.

| When (target) | Milestone |
|---|---|
| 31 Oct 2026 | Launch with video 001 (002 already finished) |
| early Jan 2027 | 10 long-form videos and ~25 Shorts published; first `log.md` review (week 8) |
| Mar–Jun 2027 | 1,000 subscribers (estimate). Start a **free PDF problem sheet** per video with an email sign-up, to build an owned audience. |
| ~Q3–Q4 2027 | **YPP** at 8,000 hours (estimate; one outlier can halve this). Submit the W-8BEN with a Sri Lankan TIN on approval. |
| ~2,000 subscribers | Open **Patreon or Ko-fi** (YouTube memberships and Super Thanks are not available in Sri Lanka): early access and the problem sheets. |
| ~10,000 subscribers | First **paid product**: a "Level 1–3 Olympiad Problems" PDF workbook with full solutions, made from the channel's own videos. |
| 50,000+ subscribers (2028, estimate) | **Sponsorships** (Brilliant and other education brands) at about $20–35 per 1,000 views. Prepare a media kit. |

**Revenue order:** AdSense (on YPP approval) → Patreon/Ko-fi → products → sponsorships. Planning figure: at 100k long-form views a month, AdSense brings in about $500–1,200 a month (estimate).

## Policy safeguards (AI narrator, faceless)

- Every video is a different, researched problem with its own solution, script, animation and sanity check. There are no templated mass uploads; never more than 1 long video a week.
- The script passes `video-script-review`, and the video passes `video-qa` before publishing (human-directed).
- Sources are always credited; narration never reads someone else's solution text.
- The description line says the narration voice is AI-generated, and research, script and animation are original. The altered-content checkbox is not required (the voice is non-realistic and doesn't imitate a real person), but don't hide the AI voice.
- The same intro and outro are fine; the bulk of each video must differ.
- Before applying for YPP, make sure the 3 most recent and most-viewed videos show the strongest original work.

## KPIs and review cadence

| KPI | Target (first 3 months) | If it misses |
|---|---|---|
| Impressions CTR | ≥ 5% | Rework the thumbnail (bigger hero, fewer words) and the title (put the question first). A/B test titles with Studio "Test & compare". |
| Retention at 30 s | ≥ 70% | The hook is slow: show the problem sooner and cut the preamble. |
| Average view percentage (8–12 min) | ≥ 45% | Find the drop point: a missing step, a long algebra stretch or a static screen. Tighten that segment. |
| Subscribers per 1,000 views | ≥ 5 | Strengthen the series promise and the theorem teaser; add an end screen to the paired video. |
| Returning viewers | ≥ 20% of viewers | More series continuity: playlists, "last week we…" callbacks. |
| Shorts → long-form clicks | Track | Change the Short's ending to a clearer open question. |

**Cadence:** a quick check of each video's 48-hour numbers. A full `/channel-planner` review with analytics every 4 weeks, the first at week 8.
