# Review rubric

Used by the `video-script-review` workflow (before any code is written) and the `video-qa` workflow (after rendering). Each reviewer covers one lens and works independently.

## Severity

| Severity | Meaning | Examples |
|---|---|---|
| **blocker** | The video would be wrong or unusable. | Wrong answer or false claim; arithmetic error; a step that doesn't follow; a mispronounced key term; theme lint errors; picture and narration out of step; a check or verify failure |
| **major** | A typical viewer is lost, misled or likely to leave, or the video looks unprofessional. | A skipped step the audience can't do mentally; an unmotivated step; a weak or missing hook; a dramatic or cheeky title or tone; clipped or overlapping text; a colour role misused; a long static stretch |
| **minor** | Polish. | Wording, a slightly long segment, a nicer visual idea |

**Approval rule:** a lens approves only if it found no blocker or major issue and every issue from the previous round in its lens is fixed. The workflow approves only if every lens approves. Minor issues should be fixed when cheap, but they don't block.

## Script lenses (`video-script-review`)

### maths-solution
- Re-solve the problem independently (by a different method where possible) and check numerically.
- The final answer, every theorem used, and its conditions are correct. Extraneous roots and cases are handled and explained.
- The method is the clearest one for the audience. `research.md` justifies the choice.

### maths-steps
- Every equation, expansion, substitution and arithmetic line is correct. Check each with Python.
- No jump the audience can't follow; intermediate lines are shown in `on_screen`.
- Notation is consistent; dialogue, `on_screen` and `animation` agree.

### clarity
- Each step is motivated before it is done ("why now?").
- Terms and symbols are defined before use; one idea per segment.
- The visual plan shows the idea (geometry, colour links, transforms), not just the words.
- There is a sanity check after the result. The explanation suits the stated audience level.

### hook-and-tone (see `style-guide.md`)
- The real problem is on screen within 2 s. There is a specific question and an honest open loop within about 10 s.
- The title is plain and descriptive: no hype, puns or exclamation marks.
- Signposts every 45 to 90 s; an early win within 60 s; the hook's loop is paid off.
- Calm, professional voice; no hype words or filler; the outro is short with one plain CTA.

### narration
- Written for the ear: spoken maths, short sentences, unambiguous grouping ("all squared").
- Risky pronunciations are listed with a proposed `tts/voice.json` rule (point letters, names, Greek letters, heteronyms).
- Each visual is introduced just before or as it appears. `timeline_tool.py check` passes.

## Rendered-video lenses (`video-qa`)

### pronunciation
- Every mismatch in `review/pronunciation.json` is classified as a real mispronunciation or an ASR difference, using the phonemes.
- Risky words in `voice_timing.json` phonemes are checked even when the ASR matched.
- Every real problem comes with an exact `voice.json` rule.

### theme-visual
- `theme_lint.py` reports no errors.
- Colour roles follow `THEME.md`; the backdrop is present; everything is inside the safe area.
- No overlap, clipping or clutter; text is readable at phone size; calm, consistent layout.

### sync
- What is narrated in a segment is visible by the end of that segment, and nothing appears before it is narrated.
- Rendered maths matches the spoken maths (numbers, signs, labels).
- No long static stretches. `check` and `verify` pass.
