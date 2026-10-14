"""
Neon Pulse — shared visual theme for all maths videos.

Every videos/*/scene.py imports this module with:
    from theme.theme import *
Never hard-code colours/fonts in scene files; add a token or helper here instead.

Concept: a late-night arcade / synth stage -- ink-black backdrop lit by soft
cyan and magenta glows, electric neon strokes, bold condensed headlines.
"""

import json
import pathlib

from manim import *

# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------
THEME_NAME = "Neon Pulse"
CHANNEL_NAME = ""

# ---------------------------------------------------------------------------
# Palette (hex). Roles, not hues: scenes use roles so the theme can evolve.
# ---------------------------------------------------------------------------
BG = "#08080D"            # background
BG_ALT = "#14141F"        # panels / cards
GRID = "#26263A"          # axes grid, faint guides
TEXT = "#F7F7FB"          # primary text & maths
TEXT_MUTED = "#9C9CB4"    # secondary text, labels
PRIMARY = "#22E1FF"       # main accent: key objects, current step
SECONDARY = "#FF3D8B"     # second accent: contrasting object
TERTIARY = "#B98CFF"      # third accent: rarely, for a third series
HIGHLIGHT = "#FFD23F"     # emphasis: results, "aha" moments
POSITIVE = "#5CFF9D"      # correct / final answer
NEGATIVE = "#FF6B4A"      # mistakes, cancellations, warnings

# Ordered list for colouring multiple series/objects consistently.
SERIES = [PRIMARY, SECONDARY, TERTIARY, HIGHLIGHT, POSITIVE]

# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
FONT_HEADING = "DIN Alternate"
FONT_BODY = "Avenir Next"
FONT_MONO = "Menlo"

SIZE_TITLE = 76
SIZE_HEADING = 48
SIZE_BODY = 32
SIZE_CAPTION = 24
MATH_SCALE = 1.0               # multiply MathTex size

# LaTeX preamble for MathTex/Tex (font package optional, e.g. \usepackage{eulervm}).
TEX_TEMPLATE = TexTemplate()
TEX_TEMPLATE.add_to_preamble(r"\usepackage{amsmath}\usepackage{newtxmath}")

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
EASE = rate_functions.ease_out_cubic                 # default rate_func for theme helpers
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


def backdrop():
    """Signature background: two soft neon glows (cyan top-left, magenta
    bottom-right) plus a faint dot grid. Static, sits behind everything."""
    W, H = config.frame_width, config.frame_height

    def blob(color, center, rmax, op):
        return VGroup(*[
            Circle(radius=rmax * k, stroke_width=0, fill_color=color,
                   fill_opacity=op).move_to(center)
            for k in np.linspace(1.0, 0.05, 40)
        ])

    dots = VGroup(*[
        Dot([x, y, 0], radius=0.012, color=TEXT, fill_opacity=0.10)
        for x in np.arange(-W / 2 + 0.4, W / 2, 0.8)
        for y in np.arange(-H / 2 + 0.4, H / 2, 0.8)
    ])
    return VGroup(
        blob(PRIMARY, [-W / 2 - 0.5, H / 2 + 0.5, 0], 6.5, 0.0055),
        blob(SECONDARY, [W / 2 + 0.5, -H / 2 - 0.5, 0], 6.5, 0.0055),
        dots,
    )


def glow(mobject, color=None, layers=6, width=18, opacity=0.06):
    """Neon halo behind a stroked mobject. Returns VGroup(halo..., mobject)."""
    color = color or mobject.get_color()
    halo = VGroup(*[
        mobject.copy().set_fill(opacity=0).set_stroke(color, width=width * (i + 1) / layers,
                                                       opacity=opacity)
        for i in range(layers)
    ])
    return VGroup(halo, mobject)


def pulse_bar(width=3.0, height=0.08):
    """Signature underline: a cyan->magenta gradient bar with rounded ends."""
    bar = RoundedRectangle(corner_radius=height / 2, width=width, height=height,
                           stroke_width=0, fill_opacity=1)
    bar.set_fill(color=[PRIMARY, SECONDARY])
    bar.set_sheen_direction(RIGHT)
    return bar


def tag(text, color=SECONDARY):
    """Small pill badge, e.g. 'QUESTION 10' or 'KEY IDEA'."""
    t = Text(text, font=FONT_HEADING, font_size=SIZE_CAPTION + 2, color=BG)
    pill = RoundedRectangle(corner_radius=0.2, width=t.width + 0.45, height=t.height + 0.28,
                            fill_color=color, fill_opacity=1, stroke_width=0)
    t.move_to(pill)
    return VGroup(pill, t)


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

    def setup(self):
        self.backdrop = backdrop()
        self.add(self.backdrop)

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
        if t.width > SAFE_W:
            t.scale_to_fit_width(SAFE_W)
        line = pulse_bar(width=min(t.width * 0.7, SAFE_W))
        group = VGroup(t, line)
        if subtitle:
            group.add(caption(subtitle))
        group.arrange(DOWN, buff=0.35)
        self.play(FadeIn(t, shift=SHIFT_IN, scale=1.15), GrowFromEdge(line, LEFT),
                  run_time=run_time, rate_func=EASE)
        if subtitle:
            self.play(FadeIn(group[2], shift=SHIFT_IN), run_time=T_FAST)
        return group

    def clear_screen(self, run_time=T_FAST):
        keep = getattr(self, "backdrop", None)
        mobs = [m for m in self.mobjects if m is not keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)


# ---------------------------------------------------------------------------
# Preview scene — rendered for theme approval: manim -s theme/theme.py ThemePreview
# ---------------------------------------------------------------------------
class ThemePreview(ThemedScene):
    def construct(self):
        h = heading(THEME_NAME)
        h_rule = pulse_bar(width=h.width * 0.8).next_to(h, DOWN, buff=0.12)
        h = VGroup(h, h_rule)
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
        curve = glow(ax.plot(lambda x: np.sin(2 * x), color=PRIMARY, stroke_width=STROKE + 1))
        curve2 = ax.plot(lambda x: 0.5 * x, color=SECONDARY, stroke_width=STROKE)
        dot = Dot(ax.c2p(0, 0), color=HIGHLIGHT)
        graph = VGroup(ax, curve, curve2, dot)

        txt = VGroup(
            tag("KEY IDEA", HIGHLIGHT),
            step_label(1, "Factor the quadratic"),
            body("Body text looks like this."),
            caption("Captions and labels are muted."),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        right = VGroup(eq_group, txt).arrange(DOWN, buff=0.6)
        content = VGroup(graph, card(right)).arrange(RIGHT, buff=0.7)
        layout = VGroup(content, swatches).arrange(DOWN, buff=0.5).next_to(h, DOWN, buff=0.4)
        layout.scale_to_fit_width(min(layout.width, SAFE_W))
        avail = (h.get_bottom()[1] - 0.3) - (-SAFE_H / 2)
        if layout.height > avail:
            layout.scale_to_fit_height(avail)
        layout.next_to(h, DOWN, buff=0.3)

        self.add(h, layout, brand_mark())
