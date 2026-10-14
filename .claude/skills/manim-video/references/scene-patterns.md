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
- If you need to start an animation part-way into a segment (timed to a phrase), wait until a point measured from the segment start: `self.wait(max(0, self.seg("s05")["start"] + 3.0 - self.time))`.

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

## Layout discipline

- Keep at most about 3 equations on screen at once. Move older work up and fade it, or clear it.
- Check widths: `if m.width > SAFE_W: m.scale_to_fit_width(SAFE_W)`.
- Keep the heading at the top. Put the main work in the centre and captions or step labels near the bottom or left.
- Don't leave the screen static for more than about 8 s. Slowly emphasise or reveal something during long narration.

## Debugging

- To render a single still: `manim -ql -s --from_animation_number N ...`
- If an `overran` error comes from `sync`: either increase that segment's `end` (then run `retime` to shift the later segments, and `export` again), or shorten its run_times.
- If a LaTeX error appears: check that PATH includes `/usr/local/texlive/2026/bin/universal-darwin`, and look for unescaped `\` (use raw strings `r"..."`).
