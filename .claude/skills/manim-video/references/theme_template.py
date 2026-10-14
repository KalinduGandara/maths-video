"""
<<THEME NAME>> — shared visual theme for all maths videos.

Every videos/*/scene.py imports this module with:
    from theme.theme import *
Never hard-code colours/fonts in scene files; add a token or helper here instead.

TEMPLATE NOTE (delete this note when filling in): every value marked <<...>> or
left as a placeholder MUST be replaced with an original choice. Keep all names
(tokens, helpers, ThemedScene API) unchanged so scene files stay compatible.
"""

import json
import pathlib

from manim import *

# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------
THEME_NAME = "<<Theme Name>>"
CHANNEL_NAME = "<<optional channel / series name, or ''>>"

# ---------------------------------------------------------------------------
# Palette (hex). Roles, not hues: scenes use roles so the theme can evolve.
# ---------------------------------------------------------------------------
BG = "#101418"            # background
BG_ALT = "#1A2027"        # panels / cards
GRID = "#2A323B"          # axes grid, faint guides
TEXT = "#ECEFF2"          # primary text & maths
TEXT_MUTED = "#8A96A3"    # secondary text, labels
PRIMARY = "#4FB3BF"       # main accent: key objects, current step
SECONDARY = "#E8A87C"     # second accent: contrasting object
TERTIARY = "#B39DDB"      # third accent: rarely, for a third series
HIGHLIGHT = "#F6D365"     # emphasis: results, "aha" moments
POSITIVE = "#7BC67E"      # correct / final answer
NEGATIVE = "#E57373"      # mistakes, cancellations, warnings

# Ordered list for colouring multiple series/objects consistently.
SERIES = [PRIMARY, SECONDARY, TERTIARY, HIGHLIGHT, POSITIVE]

# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
FONT_HEADING = "Avenir Next"   # must exist on this machine (check manimpango.list_fonts())
FONT_BODY = "Avenir Next"
FONT_MONO = "Menlo"

SIZE_TITLE = 64
SIZE_HEADING = 44
SIZE_BODY = 32
SIZE_CAPTION = 24
MATH_SCALE = 1.0               # multiply MathTex size

# LaTeX preamble for MathTex/Tex (font package optional, e.g. \usepackage{eulervm}).
TEX_TEMPLATE = TexTemplate()
TEX_TEMPLATE.add_to_preamble(r"\usepackage{amsmath,amssymb}")

# ---------------------------------------------------------------------------
# Layout & motion
# ---------------------------------------------------------------------------
SAFE_W = config.frame_width - 1.2     # keep content inside this box
SAFE_H = config.frame_height - 0.9
HEADING_EDGE_BUFF = 0.45
CORNER_RADIUS = 0.18
STROKE = 3

T_FAST = 0.5
T_NORMAL = 1.0
T_SLOW = 1.8
EASE = smooth                 # default rate_func for theme helpers
SHIFT_IN = 0.3 * UP           # direction/amount for FadeIn shifts

# ---------------------------------------------------------------------------
# Global defaults
# ---------------------------------------------------------------------------
config.background_color = BG
Text.set_default(font=FONT_BODY, color=TEXT, font_size=SIZE_BODY)
MathTex.set_default(color=TEXT, tex_template=TEX_TEMPLATE)
Tex.set_default(color=TEXT, tex_template=TEX_TEMPLATE)
Line.set_default(color=TEXT)
Arrow.set_default(color=TEXT_MUTED)


# ---------------------------------------------------------------------------
# Factory helpers — use these instead of raw constructors where they fit.
# ---------------------------------------------------------------------------
def heading(text, color=TEXT):
    """Section heading pinned to the top edge."""
    t = Text(text, font=FONT_HEADING, font_size=SIZE_HEADING, color=color, weight=BOLD)
    return t.to_edge(UP, buff=HEADING_EDGE_BUFF)


def body(text, color=TEXT, size=SIZE_BODY):
    return Text(text, font=FONT_BODY, font_size=size, color=color)


def caption(text, color=TEXT_MUTED):
    return Text(text, font=FONT_BODY, font_size=SIZE_CAPTION, color=color)


def math(*parts, color=TEXT, scale=1.0):
    """MathTex with theme sizing. Pass substrings separately for TransformMatchingTex."""
    m = MathTex(*parts, color=color)
    return m.scale(MATH_SCALE * scale)


def card(mobject, color=BG_ALT, buff=0.35, stroke_color=GRID):
    """Rounded panel behind a mobject. Returns VGroup(panel, mobject)."""
    panel = RoundedRectangle(
        corner_radius=CORNER_RADIUS,
        width=mobject.width + 2 * buff,
        height=mobject.height + 2 * buff,
        fill_color=color, fill_opacity=1,
        stroke_color=stroke_color, stroke_width=1.5,
    ).move_to(mobject)
    return VGroup(panel, mobject)


def result_box(mobject, color=POSITIVE, buff=0.25):
    """Box used for final answers."""
    return SurroundingRectangle(mobject, color=color, buff=buff,
                                corner_radius=CORNER_RADIUS, stroke_width=STROKE)


def emphasis(mobject, color=HIGHLIGHT):
    """Animation for drawing attention to a mobject."""
    return Indicate(mobject, color=color, scale_factor=1.12)


def step_label(n, text):
    """Small 'Step n — text' tag, typically placed top-left under the heading."""
    num = Text(str(n), font=FONT_HEADING, font_size=SIZE_CAPTION, color=BG, weight=BOLD)
    dot = Circle(radius=0.22, fill_color=PRIMARY, fill_opacity=1, stroke_width=0)
    num.move_to(dot)
    label = Text(text, font=FONT_BODY, font_size=SIZE_CAPTION, color=TEXT_MUTED)
    return VGroup(VGroup(dot, num), label).arrange(RIGHT, buff=0.2)


def themed_axes(x_range=(-5, 5, 1), y_range=(-3, 3, 1), x_length=9, y_length=5.5, **kw):
    return Axes(
        x_range=list(x_range), y_range=list(y_range),
        x_length=x_length, y_length=y_length,
        axis_config={"color": TEXT_MUTED, "stroke_width": 2, "include_tip": True,
                     "tip_length": 0.18, "tip_width": 0.12, "font_size": SIZE_CAPTION},
        **kw,
    )


def themed_plane(**kw):
    return NumberPlane(
        background_line_style={"stroke_color": GRID, "stroke_width": 1, "stroke_opacity": 0.8},
        axis_config={"stroke_color": TEXT_MUTED},
        **kw,
    )


def brand_mark():
    """Optional small corner watermark/series mark. Return VGroup() for none."""
    if not CHANNEL_NAME:
        return VGroup()
    return caption(CHANNEL_NAME).scale(0.8).to_corner(DR, buff=0.3).set_opacity(0.6)


# ---------------------------------------------------------------------------
# Scene base class with timeline sync
# ---------------------------------------------------------------------------
class ThemedScene(Scene):
    """Base for every video. Gives timeline-synced pacing and theme intros/outros."""

    timeline = None

    def load_timeline(self, scene_file):
        path = pathlib.Path(scene_file).resolve().parent / "timeline.json"
        self.timeline = json.loads(path.read_text())
        self._seg = {s["id"]: s for s in self.timeline["segments"]}
        return self.timeline

    def seg(self, seg_id):
        return self._seg[seg_id]

    def slot(self, seg_id):
        """Seconds left until the end of segment seg_id (for sizing run_times)."""
        return self._seg[seg_id]["end"] - self.time

    def sync(self, seg_id, tolerance=0.05):
        """Wait until the end timestamp of seg_id. Raises if animations overran."""
        end = self._seg[seg_id]["end"]
        remaining = end - self.time
        if remaining < -tolerance:
            raise RuntimeError(
                f"Segment '{seg_id}' overran by {-remaining:.2f}s "
                f"(ends {end:.2f}s, scene time {self.time:.2f}s). "
                f"Lengthen it in timeline.json or shorten its animations."
            )
        if remaining > 1e-3:
            self.wait(remaining)

    # --- signature intro / outro -----------------------------------------
    def title_card(self, title, subtitle=None, run_time=T_SLOW):
        """Signature opening. Returns the group so callers can fade it out."""
        t = Text(title, font=FONT_HEADING, font_size=SIZE_TITLE, color=TEXT, weight=BOLD)
        line = Line(LEFT, RIGHT, color=PRIMARY, stroke_width=4).set_width(t.width * 0.6)
        group = VGroup(t, line)
        if subtitle:
            group.add(caption(subtitle))
        group.arrange(DOWN, buff=0.35)
        self.play(Write(t), GrowFromCenter(line), run_time=run_time, rate_func=EASE)
        if subtitle:
            self.play(FadeIn(group[2], shift=SHIFT_IN), run_time=T_FAST)
        return group

    def clear_screen(self, run_time=T_FAST):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)


# ---------------------------------------------------------------------------
# Preview scene — rendered for theme approval: manim -s theme/theme.py ThemePreview
# ---------------------------------------------------------------------------
class ThemePreview(ThemedScene):
    def construct(self):
        h = heading(THEME_NAME)
        swatches = VGroup(*[
            VGroup(
                RoundedRectangle(corner_radius=0.1, width=1.1, height=0.7,
                                 fill_color=c, fill_opacity=1, stroke_width=0),
                Text(n, font=FONT_MONO, font_size=14, color=TEXT_MUTED),
            ).arrange(DOWN, buff=0.1)
            for n, c in [("PRIMARY", PRIMARY), ("SECONDARY", SECONDARY),
                         ("TERTIARY", TERTIARY), ("HIGHLIGHT", HIGHLIGHT),
                         ("POSITIVE", POSITIVE), ("NEGATIVE", NEGATIVE)]
        ]).arrange(RIGHT, buff=0.3)

        eq = math(r"x", r"=", r"{-b \pm \sqrt{b^2-4ac}", r"\over", r"2a}")
        eq[0].set_color(PRIMARY)
        box = result_box(eq)
        eq_group = VGroup(eq, box)

        ax = themed_axes(x_range=(-3, 3, 1), y_range=(-1.5, 1.5, 1), x_length=5, y_length=2.6)
        curve = ax.plot(lambda x: np.sin(2 * x), color=PRIMARY, stroke_width=STROKE + 1)
        curve2 = ax.plot(lambda x: 0.5 * x, color=SECONDARY, stroke_width=STROKE)
        dot = Dot(ax.c2p(0, 0), color=HIGHLIGHT)
        graph = VGroup(ax, curve, curve2, dot)

        txt = VGroup(
            step_label(1, "Factor the quadratic"),
            body("Body text looks like this."),
            caption("Captions and labels are muted."),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        right = VGroup(eq_group, txt).arrange(DOWN, buff=0.6)
        content = VGroup(graph, card(right)).arrange(RIGHT, buff=0.7)
        layout = VGroup(content, swatches).arrange(DOWN, buff=0.5).next_to(h, DOWN, buff=0.4)
        layout.scale_to_fit_width(min(layout.width, SAFE_W))

        self.add(h, layout, brand_mark())
