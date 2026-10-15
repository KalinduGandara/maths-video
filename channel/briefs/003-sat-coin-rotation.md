# 003 · The SAT Question With No Right Answer

**Status:** brief ready · **Series:** Famous Puzzles, Properly Explained · **Pillar:** Puzzles and paradoxes · **Level:** 1
**Format:** long-form, 8–10 min (+ 3 Shorts) · **Audience:** general curious adults; US/UK/EU (the SAT gives strong US recognition)
**Upload slot:** Sat 14 Nov 2026, 11:00 EST / 16:00 GMT / 17:00 CET (21:30 Sri Lanka). Shorts on Tue 17, Thu 19 and Sun 22 Nov, 12:00 EST (22:30 Sri Lanka).

## Problem
In the figure, the radius of circle A is one third the radius of circle B. Starting from the position shown, circle A rolls around circle B. At the end of how many revolutions of circle A will the centre of circle A first reach its starting point?
(A) 3/2 (B) 3 (C) 6 (D) 9/2 (E) 9

**Source:** SAT, May 1982 (mathematics section). The College Board's keyed answer was (B) 3. After three students challenged it, the College Board accepted that the correct answer is 4, which was not among the options. Sources:
- [Education Week, June 1982](https://edweek.org/education/students-outsmart-s-a-t-again-300-000-tests-will-be-rescored/1982/06)
- [Scientific American](https://www.scientificamerican.com/article/the-sat-problem-that-everybody-got-wrong)
- [Veritasium page](https://www.veritasium.com/videos/2024/1/15/the-sat-question-everyone-got-wrong)

Confirm the exact wording against a facsimile during `/manim-video` research; quote it only as it appears in a reliable reproduction.

**Answer (pre-checked):** **4 revolutions** (none of the options).
- **Rolling outside:** turns = (R + r)/r = 3 + 1 = 4.
- **Rolling inside:** (R − r)/r = 2.
- **Check:** a Python simulation of rolling without slipping, run 2026-10-15, gave 4.0000 for R = 3r. For R = r it gave 2 outside and 0 inside.

## Why this video
- **The top-scored idea in `ideas.md` (4.90).** Veritasium's version has about 18M views and the topic is widely searched. A viral "everyone got it wrong" story invites argument (MindYourDecisions outliers).
- **Broadens the audience** beyond competition fans in week 3. This is the discovery role of pillar 3.

## Angle
Veritasium covered this in depth (about 25 minutes, with a history tangent). Ours is the calm, compact, visual proof:
- **Two motions:** the "extra turn" comes from two separate motions, rolling along the path and going round the circle. Show them split apart.
- **The general rule:** (R + r)/r outside and (R − r)/r inside, tested on real coins (R = r gives 2).
- **Check it at home:** "try it with two equal coins on a table".

Keep it to 8–10 minutes. Credit Veritasium in the description for the history.

## Hook (first 10 s)
- **Opening visual:** two circles, the small one with a marked arrow, the five answer choices fading in beside them.
- **Question:** how many times does the small circle turn on its way round?
- **Open loop:** the stake. In 1982 the test-setters' answer was wrong, and the right answer was not on the page.
- **Narration draft:** "A small circle, one third the size of a big one, rolls all the way around it. How many times does it turn? In 1982, three hundred thousand students were asked this on the SAT. The examiners' answer was wrong, and the correct one wasn't among the choices."

Verify the "300,000" figure against the Edweek headline before using it.

## Outline
1. **Hook** (≈0:00–0:20)
2. **The question and the obvious answer** (≈0:20–1:30): circumference ratio 3, so "3 turns" seems clear. Pause prompt: "Pause and pick an answer."
3. **Test it with equal coins** (≈1:30–2:45): the first early win. Two equal coins: the obvious answer says 1 turn, but the animation shows 2. Something is off.
4. **Unrolling the path** (≈2:45–4:15): on a straight line, a circle rolling its own circumference turns once. Bend the line into a circle and the coin also turns once more just by going round. Show the two motions separately.
5. **Where the extra turn comes from** (≈4:15–5:30): the centre travels a circle of radius R + r, so the turns are (R + r)/r = 4 for R = 3r. (HIGHLIGHT)
6. **Rolling inside** (≈5:30–6:45): the extra turn is subtracted, giving (R − r)/r = 2. A coin inside a ring of the same size doesn't turn at all.
7. **Sanity check** (≈6:45–7:45): special cases. R = r gives 2 outside and 0 inside. Large R makes the extra turn negligible (a car wheel going round a roundabout). Suggest the two-coin experiment.
8. **Why it matters** (≈7:45–8:30): the same "extra turn" is why a day measured against the stars is about 4 minutes shorter than a solar day. Mention it briefly and plainly; no deep tangent. Tie the experience back to good problem-solving: test a special case.
9. **Outro** (≈8:30–9:00):
   - Boxed: 4 turns, none of the options.
   - CTA: "There's a sharper version of this idea with gears and planets. If you'd like that, tell me in the comments."
   - End screen to 001.

- **Key insight:** the turns are the centre's path divided by the coin's circumference: (R + r)/r, not R/r.
- **Sanity check:** the equal-coins case (2 turns), which viewers can do at home.
- **Outro / CTA:** as above. End screen and playlist.

## Packaging
- **Upload titles:**
  1. The SAT Question With No Right Answer (1982)
  2. How Many Times Does the Coin Turn? The 1982 SAT Mistake
  3. The Coin Rotation Paradox, Explained Clearly
- **On-screen title:** The Rolling Coin Question
- **Thumbnail:**
  - Hero: a big circle in SECONDARY and a small circle in PRIMARY with a curved arrow trail and the arrow marker.
  - Text: "3 or 4?"
  - Tag pill: "SAT 1982". Two elements only.
- **Description draft:**
  > A circle one third the size rolls around a bigger one: how many turns? The 1982 SAT's answer was 3. The correct answer, 4, wasn't on the page. Here's why, with the general rule and a check you can do with two coins.
  > History: Education Week (June 1982); a longer telling by Veritasium (linked).
- **Tags:** SAT question everyone got wrong, coin rotation paradox, 1982 SAT question, rolling circle problem, how many rotations, SAT math mistake, coin paradox explained, circle rolling around circle, math puzzle, geometry paradox
- **Hashtags:** #maths #puzzle #SAT #paradox
- **Pinned comment:** "Try it: two identical coins, roll one round the other. Did you get 2 turns? What would you predict for a coin rolling round a square?" (Square check: the turns equal 1 + perimeter/(2πr). Verify before answering in replies.)
- **Playlists:** Famous Puzzles, Properly Explained · Start Here: Level 1 Problems

## Shorts cut
- **Short A (≈40 s):** the two equal coins rolling, opening on "this coin turns twice". The split of the two motions, then the end card linking to the full video.
- **Short B (≈45 s):** the 1982 question and its options, then "the right answer, 4, wasn't on the page", then the rule (R + r)/r → link.
- **Short C (≈35 s):** rolling inside gives 2, and a same-size coin inside a ring doesn't turn at all → link.

## Notes for production
- **Distinguish:** "turns as seen from the table" (4) from "turns relative to the contact point" (3). Name this clearly as the source of confusion; don't call the examiners foolish.
- **Visuals:** the arrow on the small coin must stay visible; the centre's path in a dashed GRID line; a split-screen of the straight line vs the circle.
- **Pronunciation:** "S A T" (letters), "R plus r over r" (read as "big R plus small r, over small r"; better to say "the big radius plus the small radius").
- **Tone:** the story is famous; no "everyone got it wrong" hype in the narration. The title may say "No Right Answer", which is literally true.
