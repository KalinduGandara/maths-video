# 001 · Can 10 Numbers Always Split Into Equal Sums? (IMO 1972)

**Status:** brief ready · **Series:** Olympiad Problems, Explained · **Pillar:** Competition problems · **Level:** 1–2
**Format:** long-form, 8–10 min (+ 2 Shorts) · **Audience:** curious adults and teens, school maths only; US/UK/EU
**Upload slot:** Sat 31 Oct 2026, 11:00 EDT / 15:00 GMT / 16:00 CET (20:30 Sri Lanka). Shorts on Tue 3 Nov and Thu 5 Nov, 12:00 EST (22:30 Sri Lanka).

## Problem
Prove that from a set of ten distinct two-digit numbers (in the decimal system), it is possible to select two disjoint subsets whose members have the same sum.

**Source:** 14th International Mathematical Olympiad, 1972 (Toruń, Poland), Problem 1 ([AoPS wiki](https://artofproblemsolving.com/wiki/index.php/1972_IMO_Problems/Problem_1), [Kalva solution](https://prase.cz/kalva/imo/isoln/isoln721.html))

**Answer (pre-checked):** always possible. Python checks, run 2026-10-15:
- **The count:** 2¹⁰ = 1,024 subsets, but sums can only be 0 to 945 (946 values).
- **Random sets:** an equal-sum disjoint pair was found in 2,000 random sets.
- **Demo set:** 17, 23, 38, 41, 56, 64, 72, 85, 91, 99 → {23, 56} and {38, 41}, both summing to 79.
- **Counterexample with 8:** 10, 11, 44, 68, 80, 88, 92, 96. All 256 subset sums are distinct, so the claim fails for 8 numbers.
- **9 numbers:** the search did not finish, so nothing is claimed.

## Why this video
- It is the channel's promise in one problem: a genuine IMO problem, solved by counting, that anyone can follow.
- Famous competition problems explained visually are durable outliers (3B1B Putnam 16.5M, Numberphile Question Six 3.9M; `research.md` §3).
- It sets up the theorem video 004 (pigeonhole principle), which this video's outro invites.

## Angle
Competing versions are text solutions (AoPS) or fast chalkboard walk-throughs. Ours does three things:
- **Lets the viewer play first:** "pick your own ten numbers".
- **Makes the counting a picture:** 946 labelled boxes, 1,024 groups falling into them.
- **Shows why "ten" matters:** a set of 8 numbers where it fails.

No formulas beyond 2¹⁰.

## Hook (first 10 s)
- **Opening visual:** ten number tiles appear in a row. Two groups light up, cyan {23, 56} and magenta {38, 41}, with "= 79" under each.
- **Question:** will this always happen, whichever ten two-digit numbers you choose?
- **Open loop:** the shortcut. It's an olympiad problem, and the proof needs no algebra, only counting.
- **Narration draft:** "Twenty-three plus fifty-six is seventy-nine. So is thirty-eight plus forty-one. Pick any ten two-digit numbers, and two separate groups with equal totals are always hiding inside. This was the first problem at the 1972 International Mathematical Olympiad, and the proof only needs counting."

## Outline
1. **Hook** (≈0:00–0:20)
2. **The question, precisely** (≈0:20–1:15): "two-digit" means 10 to 99; "distinct" means no repeats; "disjoint" means no number used twice. The groups can have different sizes. Pause prompt: "Pause here and try it with your own ten numbers."
3. **Why it isn't obvious** (≈1:15–2:15): searching by hand is slow, because there are lots of groups. First small win: each number is either in or out, so there are 2 × 2 × … = 2¹⁰ = 1,024 groups (including the empty group).
4. **How big can a total be?** (≈2:15–3:15): the largest possible total is 90 + 91 + … + 99 = 945. So every group's total is one of 0, 1, …, 945, which is 946 possible values. Signpost: "1,024 groups, but only 946 possible totals."
5. **Key insight** (≈3:15–4:30): the totals as 946 boxes; the groups drop in one by one. More groups than boxes, so some box gets two groups. Two different groups with the same total. (HIGHLIGHT)
6. **Making them separate** (≈4:30–6:00):
   - The two groups might share numbers. Remove the shared numbers from both: each total drops by the same amount, so they stay equal.
   - Neither group ends up empty: if one were empty, it would have been inside the other, and then the bigger group's total would be larger.
   - Animate it on a real overlapping pair from the demo set.
7. **Sanity check** (≈6:00–7:15):
   - For 8 numbers: 256 groups and plenty of possible totals, so the counting gives nothing. Indeed 10, 11, 44, 68, 80, 88, 92, 96 has all 256 totals different (show a few).
   - So "ten" is doing real work.
   - For 9 numbers: 512 groups against 856 possible totals, so the argument fails. Leave whether the claim still holds as an open question for the comments.
8. **Name the idea** (≈7:15–8:15): more pigeons than holes means two share a hole. The proof says the groups exist without telling us which. That is what makes it powerful and a little strange.
9. **Outro** (≈8:15–8:50): the result boxed in words.
   - Teaser: "This idea is called the pigeonhole principle. If you'd like the full story of why it is true and where else it shows up, tell me in the comments."
   - One CTA, no begging.

- **Key insight:** 1,024 groups but only 946 possible totals, so two groups must collide.
- **Sanity check:** the 8-number counterexample shows the count is essential; the demo set's equal pair confirms the result.
- **Outro / CTA:** pigeonhole teaser → video 004. End screen: subscribe + playlist "Olympiad Problems, Explained".

## Packaging
- **Upload titles:**
  1. Can 10 Numbers Always Split Into Equal Sums? (IMO 1972)
  2. The IMO Problem You Can Solve Just by Counting
  3. IMO 1972 Problem 1, Explained Simply
- **On-screen title:** Ten Numbers, Equal Sums
- **Thumbnail:**
  - Hero: ten glowing tiles, with two groups ringed in PRIMARY and SECONDARY and "79 = 79" between them.
  - Text: "ALWAYS?" in FONT_HEADING, with HIGHLIGHT on the question mark.
  - Layout: text left, tiles right. Tag pill "IMO 1972".
- **Description draft:**
  > Pick any ten two-digit numbers: two separate groups with equal sums are always hiding inside. Here is why, using only counting.
  > Problem 1 of the 1972 International Mathematical Olympiad (Poland). Level 1–2: no algebra needed.

  Then the template from `strategy.md`, with the source link to AoPS.
- **Tags:** IMO 1972 problem 1, math olympiad problem, pigeonhole principle, olympiad math explained, subset sum problem, equal sums puzzle, counting proof, competition math, math puzzle, IMO problem explained, combinatorics for beginners
- **Hashtags:** #maths #IMO #olympiad #puzzle
- **Pinned comment:** "Post your own ten two-digit numbers and two groups with equal totals. And an open question: does it still always work with nine numbers? The counting argument alone can't decide it."
- **Playlists:** Olympiad Problems, Explained · Start Here: Level 1 Problems · The Pigeonhole Principle

## Shorts cut
- **Short A (≈40 s), hook and challenge:**
  - First second: the ten tiles and "79 = 79".
  - Keep the hook, then "this is always true; why?", then the 1,024 vs 946 line.
  - End card: "Full proof in the video linked below." Related video: 001.
- **Short B (≈35 s), the one aha step:**
  - Opens on "1,024 groups. 946 possible totals."
  - The boxes animation shows two groups landing in one box.
  - End: "and that solves an olympiad problem" → link.

## Notes for production
- **Misconceptions to address:**
  - The groups need not be the same size.
  - The empty group is counted, then shown not to matter.
  - Removing the shared numbers keeps the totals equal.
- **Visuals that must appear:** the tile row, the 946-box shelf (it can be compressed with an ellipsis), the overlap-removal animation, the 8-number counterexample.
- **Pronunciation risks:** "two to the power ten", "nineteen seventy-two", "disjoint" (check with `check_pronunciation.py`), the numbers 945/946/1,024 (write them in words in the narration).
- **Avoid:** claiming anything about nine numbers. Don't call it "easy".
