# Creating the theme (first run only)

The theme is the channel's visual identity. Every video uses it, so it must be distinctive, readable, and calm enough for long explanations.

## Design it

Choose one clear concept and derive everything from it. Example concepts (don't copy these, invent your own): "chalk on slate", "blueprint drafting", "ink on warm paper", "neon night grid", "museum placard", "botanical sketchbook".

Decide:
1. **Name**: short and memorable.
2. **Palette** (fill in every role in the template):
   - BG: dark or light. Dark is easier on the eyes for maths. If you pick a light background, make TEXT dark and check that the accents still have enough contrast.
   - TEXT must reach a contrast ratio of at least 7:1 against BG. Accents need at least 4.5:1.
   - PRIMARY / SECONDARY should be clearly different hues (at least 90° apart on the hue wheel) and both readable by colour-blind viewers. Avoid relying on a red/green pair alone to carry meaning.
   - HIGHLIGHT is used sparingly, for "aha" moments only.
3. **Fonts**: choose fonts that are installed on this Mac. Verify them with:
   `.venv/bin/python -c "import manimpango; print([f for f in manimpango.list_fonts() if 'Avenir' in f])"`
   Good built-in macOS options: Avenir Next, Futura, Gill Sans, Optima, Didot, Baskerville, Georgia, Helvetica Neue, Menlo, Courier New, American Typewriter, Chalkboard SE, Noteworthy, Marker Felt.
   You may add a LaTeX maths font package in `TEX_TEMPLATE` (for example `eulervm`, `mathpazo`, `newtxmath`, `fourier`). Check that it compiles by rendering the preview.
4. **Motion**: set default timings (T_FAST/T_NORMAL/T_SLOW), EASE (`smooth`, `rate_functions.ease_out_cubic`, `there_and_back`...), and the SHIFT_IN direction.
5. **Signature elements**: customise `title_card()` (the opening) and `brand_mark()`. You may add extra helpers, such as a textured background, a custom underline, or a recurring transition. Keep every existing helper name and signature so older scene files still work.

## Files to write

`theme/theme.py`: copy `theme_template.py`, replace every placeholder, delete the TEMPLATE NOTE, and keep the `ThemePreview` scene.

`theme/__init__.py`: an empty file, so that `from theme.theme import *` works.

`theme/THEME.md`:
```markdown
# <Theme Name>
status: pending            # → approved after user OK
approved_on: —             # YYYY-MM-DD
concept: <one sentence>

## Palette
| Role | Hex | Use |
|---|---|---|
| BG | #...... | background |
...

## Typography
- Headings: <font>, Body: <font>, Mono: <font>, Maths: <LaTeX font or Computer Modern>

## Motion & layout
- <timings, easing, layout rules, signature intro/outro>

## Usage rules
- Final answers: result_box (POSITIVE)
- Current step / key object: PRIMARY; contrasting object: SECONDARY
- HIGHLIGHT only for the one key insight per section
- <any rule specific to this theme>
```

## Preview and approval

```bash
export PATH="/usr/local/texlive/2026/bin/universal-darwin:$PATH"
.venv/bin/manim -qm -s --media_dir theme/media theme/theme.py ThemePreview -o preview
cp "$(find theme/media/images -name 'preview*.png' | head -1)" theme/preview.png
```
Look at `theme/preview.png` with Read before showing it. Check that nothing overlaps or is cut off, that the text is readable, and that the colours look harmonious. Fix any problems and render again.

Then show the user: the preview path, the palette table, the fonts, and the theme concept. Ask them to choose: **Approve**, **Tweak** (they describe what to change), or **Completely new theme**. Repeat until they approve. When they do, set `status: approved` and `approved_on`.

Changing the theme later is allowed only when the user asks. Bump a `version:` line in THEME.md. Old videos keep rendering, because helper names stay the same.
