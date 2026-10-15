# scene.py patterns

## Skeleton

```python
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))  # project root
from theme.theme import *


class VideoScene(ThemedScene):
    def construct(self):
        self.load_timeline(__file__)
        self.add(brand_mark())
        for s in self.timeline["segments"]:
            getattr(self, f"seg_{s['id']}")()

    # --- 00:00–00:07 Hook ---------------------------------------------
    def seg_s01_hook(self):
        self.title = self.title_card(self.timeline["title"])
        self.sync("s01_hook")

    # --- 00:07–00:13.5 Setup ------------------------------------------
    def seg_s02_setup(self):
        self.play(FadeOut(self.title, shift=UP), run_time=T_FAST)
        self.eq = math("3x", "+", "5", "=", "11", scale=1.4)
        self.eq[0].set_color(PRIMARY)
        self.play(Write(self.eq), run_time=T_NORMAL)
        self.sync("s02_setup")
```

- Store any object that later segments need on `self` (for example `self.eq`).
- Put a comment above each method with its time range, so the code is easy to match against the script.
- Use `self.slot("<id>")` to fit a slow animation into whatever time is left in a segment, for example `run_time=min(T_SLOW, self.slot("s05") - 0.5)`.
- **Lock visuals to the voice with `self.cue(id, "phrase")`.** It waits until the narrator starts saying that phrase, using the real word times in `voice_timing.json` (written by `tts/srt_to_voice.py`). Introduce every object on the phrase that names it: `self.cue("s05_triangle", "A C is")` then draw AC. Use `nth=2` for a repeated phrase. Without a voice file it estimates from the words-per-second rate, so draft renders still work.
- `self.at(id, seconds)` waits until a fixed offset into a segment, for a silent visual beat.
- Don't define your own `cue`/`at` or a speaking-rate constant in new scenes; the theme's versions use the real voice.

```python
    def seg_s05_triangle(self):
        sid = "s05_triangle"
        self.cue(sid, "A B is")
        self.play(Create(self.ab), run_time=T_NORMAL)
        self.cue(sid, "A C is")
        self.play(Create(self.ac), run_time=T_NORMAL)
        self.sync(sid)
```

## Useful techniques

| Need | Use |
|---|---|
| Algebra step morph | `TransformMatchingTex(old, new)` with substrings split identically; `key_map={...}` when a term changes form |
| Term moves across `=` | Animate the term's copy along an `ArcBetweenPoints` path, or use `TransformMatchingTex(..., path_arc=PI/2)` |
| Cancelling | `Cross(term, stroke_color=NEGATIVE)` then `FadeOut` |
| Highlight part of an equation | `eq[i].animate.set_color(HIGHLIGHT)`, `emphasis(eq[i])`, `Circumscribe(eq[i], color=HIGHLIGHT)` |
| Final answer | `self.play(Create(result_box(ans)))` |
| Graphs | `themed_axes()`, `ax.plot(f, color=PRIMARY)`, `ax.get_area`, `ax.get_riemann_rectangles`, `ax.get_graph_label` |
| Moving point / parameter | `ValueTracker` + `always_redraw` / `add_updater` |
| Geometry | `Polygon`, `Angle`, `RightAngle`, `Brace` + `BraceLabel`, `DashedLine` |
| Step list on the left | `VGroup(...).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)` and fade the old steps to `TEXT_MUTED` |
| Camera moves | Use `MovingCameraScene` behaviour: subclass `ThemedScene` and mix it in only when needed (`class VideoScene(ThemedScene, MovingCameraScene)`), with `self.camera.frame.animate` |
| 3D | `ThreeDScene` mixin. Keep it to a minimum, because it renders slowly |

## Thumbnail

Every `scene.py` also has a still-only thumbnail class, rendered with `manim -qh -s ... Thumbnail`:

```python
class Thumbnail(ThemedScene):
    def construct(self):
        fig = build_hero_figure().scale_to_fit_height(5.5).to_edge(RIGHT, buff=0.6)   # reuse scene geometry helpers
        words = Text("FIND r", font=FONT_HEADING, font_size=SIZE_TITLE * 1.6, color=TEXT, weight=BOLD)
        words.to_edge(LEFT, buff=0.7)
        self.add(glow(fig), words, pulse_bar(width=words.width).next_to(words, DOWN, buff=0.2))
```
Keep it to two or three large elements and at most 4 words, readable at 160 × 90 px (see style-guide.md).

## Layout discipline

- Keep at most about 3 equations on screen at once. Move older work up and fade it, or clear it.
- Check widths: `if m.width > SAFE_W: m.scale_to_fit_width(SAFE_W)`.
- Keep the heading at the top. Put the main work in the centre and captions or step labels near the bottom or left.
- Don't leave the screen static for more than about 8 s. Slowly emphasise or reveal something during long narration.

## Debugging

- To render a single still: `manim -ql -s --from_animation_number N ...`
- If an `overran` error comes from `sync`: shorten that segment's run_times first (the narration length is fixed). Only if the visual really needs more time, increase the segment's `end`, then run `retime`, `export` and `mux`.
- If a `[cue] ... not found` message appears: the phrase must match the spoken words of that segment (case and punctuation are ignored).
- If an `[at] ... late` message appears: the previous animations ran past the cue point, so shorten them or cue later.
- If a LaTeX error appears: check that PATH includes `/usr/local/texlive/2026/bin/universal-darwin`, and look for unescaped `\` (use raw strings `r"..."`).
