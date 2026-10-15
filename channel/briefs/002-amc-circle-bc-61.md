# 002 · The AMC Problem Where a Circle Finds BC

**Status:** brief ready · **Series:** Olympiad Problems, Explained (AMC week) · **Pillar:** Competition problems · **Level:** 2
**Format:** long-form, 8–10 min (+ 2 Shorts) · **Audience:** curious adults and teens, school geometry; US/UK/EU (plus AMC students right after the 5 Nov sitting)
**Upload slot:** Sat 7 Nov 2026, 11:00 EST / 16:00 GMT / 17:00 CET (21:30 Sri Lanka). Shorts on Tue 10 Nov and Thu 12 Nov, 12:00 EST (22:30 Sri Lanka).

## Problem
In triangle ABC, AB = 86 and AC = 97. A circle with center A and radius AB intersects BC at points B and X. Moreover, BX and CX have integer lengths. What is BC?
(A) 33 (B) 37 (C) 41 (D) 61 (E) 85

**Source:** 2013 AMC 12A Problem 19 (also 2013 AMC 10A Problem 23) ([AoPS wiki](https://artofproblemsolving.com/wiki/index.php/2013_AMC_12A_Problems/Problem_19), [Po-Shen Loh archive](https://live.poshenloh.com/past-contests/amc12/2013A/problem/19))

**Answer (pre-checked):** **(D) 61**, with CX = 33 and BX = 28.
- **Unique:** a Python search over all integers found 61 as the only solution.
- **Coordinate check:** B = (0, 0), C = (61, 0), A = (14, 84.85), X = (28, 0), and AX = 86 exactly.
- **The arithmetic:** 97² − 86² = 2013 = 3 × 11 × 61.

## Why this video
- **Timing:** AMC 10A/12A is sat on 5 Nov 2026 and 10B/12B on 13 Nov. Searches for AMC problems peak in that window (`research.md` §4).
- **Dual role:** a real AMC problem that looks impossible (two numbers, a circle, "integer lengths") yet reduces to factoring the year 2013, a memorable reveal.
- **Introduces power of a point,** a theorem candidate (idea "Power of a Point, Explained").

## Angle
Most solutions jump straight to "by power of a point". Ours earns it:
- **Pythagoras first:** drop the perpendicular from A to BC. The foot M is the midpoint of BX, because AB = AX.
- **Then the algebra:** Pythagoras twice gives CX · CB = AC² − AB², with only school geometry.
- **Then the name:** only after that do we name the rule (power of a point).
- **Then the integers:** the number 2013 is factored, and the triangle inequality picks the answer.

## Hook (first 10 s)
- **Opening visual:** the triangle with AB = 86 and AC = 97, the circle round A through B, and X appearing on BC.
- **Question:** how long is BC?
- **Open loop:** we only know two lengths and that two pieces are whole numbers. The answer hides inside the year the contest was held.
- **Narration draft:** "Two sides of a triangle, eighty-six and ninety-seven, and a circle centred at one corner. Two pieces of the base are whole numbers. That's enough to find the base exactly, and the answer is hiding inside the year this contest was written."

## Outline
1. **Hook** (≈0:00–0:20)
2. **Setting the scene** (≈0:20–1:15): label everything. AX = 86 too, since X is on the circle: name it once and keep it. Call BX = b and CX = c, so BC = b + c. Pause prompt.
3. **First win: a hidden isosceles triangle** (≈1:15–2:30): ABX is isosceles, so the perpendicular from A meets BX at its midpoint M. Write BM = MX = b/2.
4. **Pythagoras twice** (≈2:30–4:15): AM² = 86² − (b/2)² and AM² = 97² − (c + b/2)². Set them equal; the (b/2)² terms cancel. This leaves c(c + b) = 97² − 86². Signpost: "Everything now depends on one number."
5. **That number is 2013** (≈4:15–5:15): 97² − 86² = (97 − 86)(97 + 86) = 11 × 183 = 2013. And CX × CB = 2013. (HIGHLIGHT: the contest year.)
6. **Factoring** (≈5:15–6:45):
   - 2013 = 3 × 11 × 61, so CB is a factor: 1, 3, 11, 33, 61, 183, 671 or 2013.
   - The triangle inequality says 97 − 86 < BC < 97 + 86, so 11 < BC < 183. That leaves 33 or 61.
   - CX must be smaller than CB: CB = 33 would need CX = 61, which is impossible.
   - So BC = 61, CX = 33 and BX = 28.
7. **Sanity check** (≈6:45–7:45): draw the exact triangle to scale with BC = 61 and check that AX = 86 on the picture. Option (D) matches.
8. **Name the tool** (≈7:45–8:30): the product CX × CB is the same for every line from C through the circle. This is the "power of the point C", and it equals AC² − r².
9. **Outro** (≈8:30–9:00): boxed answer. Teaser: "That rule, the power of a point, shows up all over olympiad geometry. If you'd like a video on why it's true, tell me in the comments." Good luck to everyone sitting AMC 12B on 13 November.

- **Key insight:** CX · CB = 97² − 86² = 2013, and 2013 factors as 3 · 11 · 61.
- **Sanity check:** the scale drawing plus the triangle inequality.
- **Outro / CTA:** power-of-a-point teaser; end screen to 001.

## Packaging
- **Upload titles:**
  1. The AMC 12 Problem Hidden in the Number 2013
  2. Find BC: A Circle, a Triangle and Whole Numbers (AMC 12)
  3. 2013 AMC 12A Problem 19, Explained Step by Step
- **On-screen title:** A Circle That Finds BC
- **Thumbnail:**
  - Hero: the triangle with the circle glowing in PRIMARY and BC in SECONDARY, labelled "?".
  - Text: "BC = ?"
  - Tag pill: "AMC 12".
- **Description draft:**
  > Two sides, 86 and 97, a circle, and two whole-number lengths: how long is BC? The answer hides in the year 2013.
  > 2013 AMC 12A Problem 19 / AMC 10A Problem 23. Level 2: Pythagoras and factoring.
- **Tags:** AMC 12 2013 problem 19, AMC 10 2013 problem 23, AMC 12 geometry, power of a point, AMC 12 prep, math competition geometry, triangle circle problem, find BC, Pythagoras problem, AMC 2026 practice, olympiad geometry explained
- **Hashtags:** #maths #AMC12 #geometry #olympiad
- **Pinned comment:** "Which step would you have found first, the isosceles triangle or the factoring? And good luck to anyone sitting AMC 12B on 13 November."
- **Playlists:** Olympiad Problems, Explained · Competition Season · Power of a Point

## Shorts cut
- **Short A (≈45 s):**
  - Opens on the figure: "86, 97, a circle. Find BC."
  - Jump to "everything reduces to 97² − 86²", reveal 2013, then "and 2013 = 3 × 11 × 61".
  - End: "which factor is BC? Full video linked."
- **Short B (≈35 s):** the factoring and triangle-inequality step on its own, ending with BC = 61 in the result box. Related video: 002.

## Notes for production
- **Misconception:** X lies between B and C (show this). Don't assume the answer from the options.
- **Visuals:** the perpendicular AM, both right triangles shaded, the factor ladder filtered by the 11 < BC < 183 band, the final to-scale figure.
- **Pronunciation:** "A M C twelve", "ninety-seven squared minus eighty-six squared", "two thousand thirteen" vs "twenty thirteen" (choose "twenty thirteen" for the year and "two thousand and thirteen" for the number, or keep one form and check it), the point letters A/B/C/X/M (A-as-letter rules already exist in `tts/voice.json`).
- **Upload timing:** needs to be finished before 4 Nov (AMC 10A/12A is on 5 Nov).
