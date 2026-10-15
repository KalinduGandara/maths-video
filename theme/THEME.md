# Neon Pulse
status: approved
approved_on: 2026-10-14
version: 2
concept: A late-night arcade / synth stage: ink-black backdrop lit by soft cyan and magenta glows, electric neon strokes, bold DIN headlines.

## Palette
| Role | Hex | Use |
|---|---|---|
| BG | #08080D | background (cyan glow top-left, magenta glow bottom-right, faint dot grid) |
| BG_ALT | #14141F | panels / cards |
| GRID | #26263A | grids, faint guides |
| TEXT | #F7F7FB | primary text & maths |
| TEXT_MUTED | #9C9CB4 | labels, captions |
| PRIMARY | #22E1FF | electric cyan: key objects, current step |
| SECONDARY | #FF3D8B | hot magenta: contrasting object |
| TERTIARY | #B98CFF | violet: third series (rare) |
| HIGHLIGHT | #FFD23F | gold: "aha" moments only |
| POSITIVE | #5CFF9D | final answers |
| NEGATIVE | #FF6B4A | mistakes, removed parts, warnings |

## Typography
- Headings: DIN Alternate (bold), Body: Avenir Next, Mono: Menlo, Maths: newtxmath (Times-style italic)

## Motion & layout
- T_FAST 0.5 s, T_NORMAL 1.0 s, T_SLOW 1.8 s; easing ease-out-cubic; entrances rise up (SHIFT_IN = 0.3 up).
- Restrained, professional motion: no bouncing, popping, spinning or zoom-punch entrances. Titles fade up calmly (`title_card`); emphasis is a brief `emphasis()` or colour change, at most one per sentence.
- Timing: `self.cue(seg_id, "phrase")` starts an animation as the narrator says that phrase (from `voice_timing.json`); `self.sync(seg_id)` ends each segment.
- Signature: `backdrop()` (two soft neon glows + dot grid) on every scene as `self.backdrop`, never cleared by `clear_screen`.
- `pulse_bar()`: cyan→magenta gradient underline under titles/headings.
- `glow(mob)`: neon halo for key curves/shapes. `tag(text, color)`: pill badge ("QUESTION", "KEY IDEA").
- Keep content within SAFE_W × SAFE_H.

## Usage rules
- Final answers: result_box (POSITIVE)
- Current step / key object: PRIMARY; contrasting object: SECONDARY
- HIGHLIGHT only for the one key insight per section
- Removed / subtracted regions: NEGATIVE
- Use glow() sparingly: the one or two hero objects on screen.

## Changelog
- v2 (2026-10-15): title card no longer scales in (calmer, per user feedback); added `at()` / `cue()` word-timed sync to `ThemedScene`.
