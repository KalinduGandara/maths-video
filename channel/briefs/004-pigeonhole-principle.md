# 004 · The Pigeonhole Principle, Explained Simply

**Status:** brief ready (conditional on how 001 is received; see `calendar.md`) · **Series:** The Theorem Behind It · **Pillar:** Theorems · **Level:** 1→2
**Format:** long-form, 9–11 min (+ 2 Shorts) · **Audience:** curious adults and teens; US/UK/EU; viewers arriving from 001
**Upload slot:** Sat 21 Nov 2026, 11:00 EST / 16:00 GMT / 17:00 CET (21:30 Sri Lanka). Shorts on Tue 24 Nov and Thu 26 Nov, 12:00 EST (22:30 Sri Lanka).

## Problem
**Principle:** if more than n objects go into n boxes, some box holds at least two. In its general form, if more than k·n objects go into n boxes, some box holds at least k + 1.

The video works through four applications, in rising difficulty:
1. **Socks:** a drawer with black and white socks. How many must you take, in the dark, to be sure of a matching pair? **Answer:** 3.
2. **Hair:** two people in London have exactly the same number of hairs on their heads. **Data:** London has about 9 million people, and a human head has far fewer than 1 million hairs.
3. **Five points:** any 5 points in a square of side 1 include two at distance at most √2/2.
4. **Lattice midpoints:** among any 5 points with whole-number coordinates, two have a midpoint with whole-number coordinates. Four points such as (0,0), (0,1), (1,0) and (1,1) show 5 is needed.

Callback: IMO 1972 Problem 1 (video 001).

**Sources:**
- The principle: Dirichlet, 1834, the "Schubfachprinzip". Confirm during research.
- The five-points and lattice problems: standard olympiad training problems. Cite a textbook such as Engel, *Problem-Solving Strategies*, ch. 4, during research.
- [Colorado Mesa Putnam notes on pigeonhole](https://org.coloradomesa.edu/~mapierce2/putnam/examples/pigeonhole.html)
- London's population and hair-count figures need sources during research (ONS; a dermatology source).

**Answers (pre-checked):** Python checks, run 2026-10-15:
- **Five points:** over 20,000 random 5-point sets, the largest minimum distance was 0.537, below √2/2 ≈ 0.707.
- **Lattice midpoints:** the claim held for 5,000 random lattice 5-sets, and the 4-point counterexample was confirmed.

## Why this video
- It is the theorem behind 001. The outro of 001 asks "would you like the full story?", and this pays it off and builds the problem → theorem loop.
- Theorem search alone is weak (`research.md` §4). So it is scheduled after 001 has had 3 weeks to accumulate interest, and it links 001 heavily.
- February is the low-CPM season, but this one is in November to complete the loop while 001 is fresh.

## Angle
Most pigeonhole videos stop at socks. Ours climbs a staircase:
- **Obvious:** socks.
- **Surprising:** hair.
- **Geometric:** five points, where the "boxes" are invented: cut the square into 4.
- **Clever:** lattice points, where the "boxes" are odd/even patterns.

It closes with the IMO problem from 001, now seen as one line. The lesson for viewers: the whole skill is choosing the boxes.

## Hook (first 10 s)
- **Opening visual:** a map outline of London; two figures; a tally "same number of hairs".
- **Question:** how can we be sure two Londoners have exactly the same number of hairs, without counting anyone's?
- **Open loop:** the shortcut. It follows from an idea simple enough for socks, and the same idea solved an olympiad problem.
- **Narration draft:** "Somewhere in London, two people have exactly the same number of hairs on their heads. We can be certain of it without counting a single hair. The reason is an idea simple enough to explain with socks, and strong enough to solve olympiad problems."

## Outline
1. **Hook** (≈0:00–0:20)
2. **Socks** (≈0:20–1:30): two colours means two boxes, so three socks force a pair. State the principle plainly. Early win.
3. **Hair** (≈1:30–3:00): the boxes are the hair counts 0 to 999,999 (a million boxes); the objects are about 9 million people, so some box holds at least two. General form: in fact at least 9 people share a count. Signpost: "Now the boxes won't be given to us."
4. **Five points in a square** (≈3:00–5:00): pause prompt. Cut the square into 4 small squares; 5 points in 4 boxes means two share a small square. The farthest apart two points in a small square can be is its diagonal, √2/2. (HIGHLIGHT: choosing the boxes.)
5. **Lattice points** (≈5:00–7:00): a midpoint is whole exactly when both coordinates have matching parity. There are 4 parity patterns (even/odd for x and for y), so 5 points means two share a pattern. Show the 4-point example where it fails, so 5 is exactly right.
6. **Back to IMO 1972** (≈7:00–8:30): the boxes are the totals 0 to 945; the objects are the 1,024 groups. The same idea in one line. Link card to 001.
7. **Sanity check and limits** (≈8:30–9:30): the principle says that something exists, not where. Contrast it with an exact answer. Note the bound is tight in each example (2 socks, 4 points).
8. **Outro** (≈9:30–10:00):
   - Summary: "choose the boxes".
   - Leave one problem for the comments: "Among any 6 people, either 3 all know each other or 3 are all strangers." This is R(3,3) = 6, a classic; verified 2026-10-15: every 2-colouring of the 6-person graph has a one-colour triangle, and a 5-person counterexample exists.
   - CTA: "If you'd like that one solved, tell me in the comments."

- **Key insight:** the skill is inventing the right boxes.
- **Sanity check:** each bound is tight (counterexamples with one fewer object).
- **Outro / CTA:** the Ramsey six-people question as a comment challenge and a possible future video.

## Packaging
- **Upload titles:**
  1. The Pigeonhole Principle, Explained Simply
  2. Why Two Londoners Have the Same Number of Hairs
  3. One Simple Idea That Solves Olympiad Problems
- **On-screen title:** The Pigeonhole Principle
- **Thumbnail:**
  - Hero: four glowing boxes (PRIMARY) with five dots, two of them in one box ringed in HIGHLIGHT.
  - Text: "5 IN 4"
  - Tag pill: "THEOREM".
- **Description draft:**
  > The pigeonhole principle, from socks to an olympiad problem: why two people in London must have the same number of hairs, why 5 points in a square have two close together, and how the same idea solves IMO 1972 Problem 1.
  > The Theorem Behind It, part of the series that explains the tools used in our olympiad problems.
- **Tags:** pigeonhole principle, pigeonhole principle explained, pigeonhole principle examples, Dirichlet box principle, pigeonhole principle olympiad, combinatorics explained, math olympiad techniques, discrete math basics, five points in a square, lattice point midpoint, IMO 1972 problem 1
- **Hashtags:** #maths #pigeonhole #olympiad #combinatorics
- **Pinned comment:** "Among any 6 people, are there always 3 mutual friends or 3 mutual strangers? Try it before I post a video on it."
- **Playlists:** The Theorem Behind It · The Pigeonhole Principle (with 001)

## Shorts cut
- **Short A (≈35 s):** socks then hair; open on "two Londoners have the same number of hairs" → link.
- **Short B (≈45 s):** five points in a square. Open on the square with 5 dots, "two of these are close; how close?"; cut into 4; the diagonal √2/2 in the result box → link.

## Notes for production
- **Data claims need citations:** the London population and the maximum hair count. Use "fewer than a million" (a safe upper bound with a source), not a precise average.
- **The 5-points bound** is "at most √2/2" (≤), including the boundary case. Be precise about points on the cut lines (assign them to either box).
- **Pronunciation:** "Dirichlet" (dee-ree-KLAY; add to `tts/voice.json` pronunciations if used), "root two over two".
- **Ramsey R(3,3) = 6:** verified with Python on 2026-10-15 (all 2-colourings of K6 contain a one-colour triangle; K5 has a counterexample).
