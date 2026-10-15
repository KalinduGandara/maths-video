# Channel style guide

The channel sounds like a calm, expert teacher who respects the viewer's time. Quality and clarity keep people watching, not hype. The script reviewers grade against this file.

## Tone

- Plain, confident and warm. Short declarative sentences. Explain, don't perform.
- Never use hype words: "insane", "mind-blowing", "crazy", "genius", "you won't believe", "secret trick", "destroy", "epic", "satisfying". Avoid exclamation marks.
- No jokes, memes, sound-effect words or rhetorical theatre ("Wait for it...", "Boom!"). One dry, understated remark per video is the limit.
- Don't talk down to the viewer: no "this is easy", "obviously" or "simply". Say why a step works.
- Use "we" for the shared working ("now we subtract") and "you" for the viewer's own thinking ("you might expect...").

## Titles

On-screen title (`timeline.json` → `title`):
- Plain and descriptive. Name the problem or concept, in 2 to 6 words, in title case. Examples: "Four Touching Circles", "Area of a Semicircle with a Chord", "Why 0.999... Equals 1".
- No puns, wordplay, emoji, question-bait or exclamation marks.
- It fades in calmly with the theme's `title_card` and is gone within about 3 seconds. The problem itself is the opening visual, not the title.

Upload titles (in `publish.md`, from the brief) may be more search- and curiosity-driven. They must still be honest: the video has to deliver exactly what the title promises.

## The hook (first 5 to 15 seconds)

The hook earns the next minute. A good hook does three things, quickly:
1. **Shows the actual problem** on screen within the first 2 seconds. Don't open with a logo, an intro or "In this video...".
2. **Asks one specific question** the viewer now wants answered ("What is the radius of the small circle?").
3. **Opens a loop** that the video promises to close: a surprising fact, a tension or a stake. Make it true and specific:
   - Surprise: "We only know one number, sixteen, and that turns out to be enough."
   - Tension: "Three equations, three unknowns, and every one of them has a square in it."
   - Stake: "This is question 22 of a national olympiad; most students left it blank."
   - Shortcut: "There is a one-line formula for this. But first, let's see why it has to be true."

Avoid: questions with an obvious answer, fake difficulty ("only geniuses can solve this"), and promises the video does not keep.

## Keeping viewers to the end

- **Signpost every 45 to 90 seconds**: say where we are and what's next ("We have x. Now the same trick gives us y."). Each signpost is also a chapter (`chapter` field).
- **Give early small wins**: the first real insight comes within the first 60 seconds.
- **One idea per segment.** Each step is motivated before it is executed ("To get rid of the squares, we subtract").
- **Something changes on screen at least every 6 to 8 seconds**: a reveal, a highlight or a transform, never a static slide.
- **Pay off the hook's loop explicitly** at the result, then a short sanity check (estimate, special case, picture), so the viewer trusts the answer.
- **End promptly.** After the result and check, at most one short outro: a genuine follow-up question or a teaser for a related video, and one plain call to action ("If you'd like the proof of that theorem, tell me in the comments"). Never beg for likes or subscriptions.

## Explanation standard

- Aim at the average viewer of the target audience, not the strongest one. Show every algebra step that this viewer can't do in their head in two seconds.
- Define every term and symbol before using it. Name each object once, then keep that name.
- Prefer the method that is clearest to understand over the shortest one. Mention the slicker method as a teaser if it adds value.
- Give the reason behind each rule ("the line joining the centres passes through the touching point, so...").
- State the final answer in words and in symbols, boxed.

## Pacing

- 2.5 words per second is the planning rate. The real clip lengths from the voice set the final timing.
- Leave a 1 to 2 second silent beat after the key insight and after the final answer.
- Long-form videos run 4 to 10 minutes; Shorts are under 60 seconds, with the hook in the first 2 seconds and one idea.

## Visual tone

- Follow `theme/THEME.md`. Motion is calm: fades, writes, transforms and gentle highlights. No spins, wiggles, bounces, zoom punches or flashing.
- `HIGHLIGHT` gold is used once per section, for the insight. Final answers use `result_box` (POSITIVE).
- Text on screen is short (labels and equations, not sentences), and readable on a phone.

## Thumbnail (rendered from the scene's `Thumbnail` class)

- One hero visual (the figure or the key equation), large, using the theme palette on the theme backdrop.
- At most 4 words of text in `FONT_HEADING`, high contrast. The text must not repeat the upload title.
- It must be readable at 160 × 90 px: two or three elements at most, nothing small.
- Honest: show the real problem, without fake arrows, shocked faces or invented numbers.
