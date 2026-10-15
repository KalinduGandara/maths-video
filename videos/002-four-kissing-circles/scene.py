import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))  # project root
from theme.theme import *

# Problem geometry (problem units). Centres A, B, C of the radius-1, 2, 3 circles;
# O is the small circle's centre. r = 6/23, O = (21/23, 20/23).
RS = 6 / 23
OX, OY = 21 / 23, 20 / 23
CEN = {"A": (0, 0), "B": (3, 0), "C": (0, 4)}
RAD = {"A": 1, "B": 2, "C": 3}
COL = {"A": PRIMARY, "B": SECONDARY, "C": TERTIARY}
RX = 3.0                                  # x-centre of the right-hand column
SPEAK_WPS = 2.8                           # narrator's real speaking rate, for cue timing

# Algebra screen layout
EQS = 0.85                                # equation scale
EQX = 0.4                                 # x of the "=" sign in aligned rows
LABX = -5.3                               # x of the "(1)" style row labels
Y_TOP, Y_BOT, RULE_Y, DIFF_Y, STEP_Y, SOLVE_Y = 2.0, 1.1, 0.62, 0.05, -0.95, -2.15
NOTE_Y = [-0.5, -1.3]
XSLOT, YSLOT = np.array([3.4, 3.15, 0]), np.array([5.5, 3.15, 0])


class Frame:
    """Maps problem coordinates to the screen: A sits at `A`, `S` screen units per unit."""

    def __init__(self, A, S):
        self.A, self.S = np.array([*A, 0.0]), S

    def p(self, x, y):
        return self.A + self.S * np.array([x, y, 0.0])

    def c(self, k):
        return self.p(*CEN[k])

    def o(self):
        return self.p(OX, OY)


F_HOOK = Frame((2.52, -2.05), 0.68)
F_LEFT = Frame((-4.2, -1.9), 0.6)
F_ZOOM = Frame((-5.7, -3.0), 1.4)
F_CHECK = Frame((-3.3, -1.85), 0.62)


def big_circle(F, k):
    return Circle(radius=F.S * RAD[k], color=COL[k], stroke_width=4).move_to(F.c(k))


def small_circle(F, color=TEXT):
    return Circle(radius=F.S * RS, color=color, stroke_width=3).move_to(F.o())


def dot(p, color=TEXT, r=0.06):
    return Dot(p, radius=r, color=color)


def right_mark(F, size=0.24, color=HIGHLIGHT):
    a = F.c("A")
    return VMobject(color=color, stroke_width=3).set_points_as_corners(
        [a + size * RIGHT, a + size * (RIGHT + UP), a + size * UP])


def tri_sides(F, color=TEXT):
    return {
        "AB": Line(F.c("A"), F.c("B"), color=color, stroke_width=4),
        "AC": Line(F.c("A"), F.c("C"), color=color, stroke_width=4),
        "BC": Line(F.c("B"), F.c("C"), color=color, stroke_width=4),
    }


def eq_row(label, *parts, scale=0.85):
    """Numbered equation: muted '(n)' then the MathTex. Returns VGroup(label, eq)."""
    m = math(*parts, scale=scale)
    lab = math(label, color=TEXT_MUTED, scale=0.7)
    return VGroup(lab, m).arrange(RIGHT, buff=0.3)


def place(m, eq_index, y, x=EQX):
    """Put MathTex m at height y with its part eq_index (the '=') centred on x."""
    m.shift(RIGHT * (x - m[eq_index].get_center()[0]))
    m.set_y(y)
    return m


def strike(m, color=NEGATIVE):
    return Line(m.get_corner(DL), m.get_corner(UR), color=color, stroke_width=4)


class VideoScene(ThemedScene):
    def construct(self):
        self.load_timeline(__file__)
        self.add(brand_mark())
        self.step = None
        for s in self.timeline["segments"]:
            getattr(self, f"seg_{s['id']}")()

    # --- timing helpers ---------------------------------------------------
    def at(self, seg_id, offset):
        """Wait until `offset` seconds into segment seg_id."""
        dt = self.seg(seg_id)["start"] + offset - self.time
        if dt < -0.05:
            print(f"[at] {seg_id}+{offset:.1f}: late by {-dt:.2f}s")
        if dt > 1e-3:
            self.wait(dt)

    def cue(self, seg_id, phrase, lead=0.2):
        """Wait until the narrator reaches `phrase` in this segment's dialogue."""
        d = self.seg(seg_id)["dialogue"]
        n = len(d[:d.index(phrase)].split())
        self.at(seg_id, max(0.0, n / SPEAK_WPS - lead))

    def swap_step(self, n, text, corner=False):
        new = step_label(n, text)
        if corner:
            new.to_corner(UL, buff=0.5)
        else:
            new.move_to([RX, 3.3, 0])
        if self.step is not None:
            self.play(FadeOut(self.step, shift=UP * 0.2), FadeIn(new, shift=SHIFT_IN),
                      run_time=T_FAST)
        else:
            self.play(FadeIn(new, shift=SHIFT_IN), run_time=T_FAST)
        self.step = new

    def wipe(self, keep=()):
        """Fade everything except the backdrop, the step label and `keep`."""
        keep = set(keep) | {self.backdrop, self.step}
        mobs = [m for m in self.mobjects if m not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=T_FAST)

    def move_figure(self, F, keys=("A", "B", "C")):
        anims = [Transform(self.circ[k], big_circle(F, k)) for k in keys]
        anims.append(Transform(self.small, small_circle(F, self.small.get_color())))
        return anims

    # --- Hook ------------------------------------------------------------
    def seg_s01_hook(self):
        sid = "s01_hook"
        F = F_HOOK
        q = tag("QUESTION 22", SECONDARY)
        title = Text(self.timeline["title"], font=FONT_HEADING, font_size=SIZE_TITLE,
                     color=TEXT, weight=BOLD)
        title.scale_to_fit_width(5.6)
        bar = pulse_bar(width=title.width * 0.7)
        block = VGroup(q, title, bar).arrange(DOWN, buff=0.3).move_to([-3.3, 0.6, 0])
        q.align_to(title, LEFT)
        bar.align_to(title, LEFT)
        self.play(FadeIn(q, scale=0.6), run_time=T_FAST)
        self.play(FadeIn(title, shift=SHIFT_IN), GrowFromEdge(bar, LEFT),
                  run_time=T_NORMAL, rate_func=EASE)
        self.circ = {k: big_circle(F, k) for k in "ABC"}
        self.play(LaggedStart(*[Create(self.circ[k]) for k in "ABC"], lag_ratio=0.45),
                  run_time=2.5)
        self.cue(sid, "A smaller circle")
        tr = ValueTracker(0.01)
        grow = always_redraw(lambda: Circle(radius=F.S * RS * tr.get_value(), color=TEXT,
                                            stroke_width=3).move_to(F.o()))
        self.add(grow)
        self.play(tr.animate.set_value(1.0), run_time=T_SLOW, rate_func=EASE)
        grow.clear_updaters()
        self.remove(grow)
        self.small = small_circle(F)
        self.add(self.small)
        self.cue(sid, "Let's find")
        self.qmark = Text("?", font=FONT_HEADING, font_size=64, color=HIGHLIGHT,
                          weight=BOLD).move_to(F.p(-1.75, 0.45))
        self.qarrow = CurvedArrow(self.qmark.get_right() + RIGHT * 0.05,
                                  F.o() + LEFT * F.S * RS * 1.1, angle=-PI / 4,
                                  color=HIGHLIGHT, stroke_width=3, tip_length=0.15)
        self.play(FadeIn(self.qmark, scale=0.4), Create(self.qarrow), run_time=T_NORMAL)
        self.title_block = block
        self.sync(sid)

    # --- Setup -----------------------------------------------------------
    def seg_s02_setup(self):
        sid = "s02_setup"
        F = F_HOOK
        h = Text("Find r", font=FONT_HEADING, font_size=SIZE_HEADING, color=TEXT, weight=BOLD)
        hb = pulse_bar(width=h.width * 0.9)
        cap = caption("All four circles touch from the outside")
        head = VGroup(h, hb, cap).arrange(DOWN, buff=0.15)
        hb.align_to(h, LEFT)
        cap.align_to(h, LEFT)
        head.move_to([-3.3, 2.6, 0]).align_to([-6.2, 0, 0], LEFT)
        self.play(FadeOut(self.title_block, shift=UP * 0.3), run_time=T_FAST)
        self.play(FadeIn(h, shift=SHIFT_IN), GrowFromEdge(hb, LEFT), run_time=T_FAST)
        self.cue(sid, "A circle of radius r")
        rlab = math("r", color=HIGHLIGHT, scale=1.1).move_to(self.qmark)
        self.play(ReplacementTransform(self.qmark, rlab), run_time=T_NORMAL)
        self.rlab = rlab
        self.cue(sid, "three circles with")
        dirs = {"A": (-1, 0), "B": (np.cos(-0.7), np.sin(-0.7)), "C": (np.cos(2.2), np.sin(2.2))}
        radii = VGroup()
        for k in "ABC":
            cx, cy = CEN[k]
            dx, dy = dirs[k]
            ln = Line(F.c(k), F.p(cx + RAD[k] * dx, cy + RAD[k] * dy), color=COL[k], stroke_width=3)
            n = math(str(RAD[k]), color=COL[k], scale=0.85)
            n.next_to(ln.get_center(), rotate_vector(ln.get_unit_vector(), PI / 2), buff=0.14)
            radii.add(VGroup(dot(F.c(k), COL[k], 0.05), ln, n))
        self.play(LaggedStart(*[FadeIn(g, shift=SHIFT_IN * 0.5) for g in radii], lag_ratio=0.4),
                  run_time=2.0)
        self.radii = radii
        self.cue(sid, "Each of them")
        self.play(FadeIn(cap, shift=SHIFT_IN), run_time=T_FAST)
        o = np.array([OX, OY])
        small_pts = []
        for k in "ABC":
            c = np.array(CEN[k], dtype=float)
            u = (o - c) / np.linalg.norm(o - c)
            small_pts.append(F.p(*(c + RAD[k] * u)))
        pair_pts = [F.p(1, 0), F.p(0, 1), F.p(3 - 2 * 0.6, 0 + 2 * 0.8)]
        self.play(LaggedStart(*[Flash(p, color=HIGHLIGHT, line_length=0.12, flash_radius=0.12)
                                for p in small_pts], lag_ratio=0.3), run_time=T_SLOW)
        self.cue(sid, "and they also")
        self.play(LaggedStart(*[Flash(p, color=HIGHLIGHT, line_length=0.18, flash_radius=0.18)
                                for p in pair_pts], lag_ratio=0.3), run_time=T_SLOW)
        self.cue(sid, "What is r?")
        self.play(Indicate(rlab, color=HIGHLIGHT, scale_factor=1.5), run_time=T_NORMAL)
        opts = [("A", r"\frac{1}{4}"), ("B", r"\frac{6}{23}"), ("C", r"\frac{3}{11}"),
                ("D", r"\frac{5}{17}"), ("E", r"\frac{3}{10}")]
        cards = VGroup()
        for letter, v in opts:
            badge = tag(letter, TEXT_MUTED)
            row = VGroup(badge, math(v, scale=0.9)).arrange(RIGHT, buff=0.3)
            c = card(row, buff=0.18)
            c[0].stretch_to_fit_width(1.75)
            cards.add(c)
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.3)).move_to([-3.4, -0.9, 0])
        self.cue(sid, "The options")
        self.play(LaggedStart(*[FadeIn(c, shift=SHIFT_IN) for c in cards], lag_ratio=0.5),
                  run_time=4.5)
        self.options = cards
        self.head = VGroup(h, hb, cap)
        self.sync(sid)

    # --- Step 1: use the centres -----------------------------------------
    def seg_s03_centres(self):
        sid = "s03_centres"
        self.play(FadeOut(self.options, shift=LEFT * 0.3), FadeOut(self.head, shift=UP * 0.2),
                  FadeOut(self.radii), FadeOut(self.rlab), FadeOut(self.qarrow), run_time=T_FAST)
        self.play(*self.move_figure(F_LEFT), run_time=T_SLOW, rate_func=EASE)
        self.swap_step(1, "Join the centres")
        self.cue(sid, "For touching circles")
        txt = body("For touching circles, use the centres")
        self.rule_card = card(txt, buff=0.3).move_to([RX, 2.2, 0])
        self.play(FadeIn(self.rule_card, shift=SHIFT_IN), run_time=T_NORMAL)
        self.cue(sid, "So let's mark")
        self.cdots = {k: dot(F_LEFT.c(k), COL[k], 0.08) for k in "ABC"}
        self.play(LaggedStart(*[GrowFromCenter(self.cdots[k]) for k in "ABC"], lag_ratio=0.3),
                  run_time=T_NORMAL)
        self.play(LaggedStart(*[Flash(self.cdots[k], color=COL[k], line_length=0.2)
                                for k in "ABC"], lag_ratio=0.3), run_time=T_SLOW)
        self.sync(sid)

    # --- Why: distance = sum of radii ------------------------------------
    def seg_s04_rule(self):
        sid = "s04_rule"
        a, b = 1.0, 1.4
        c1 = np.array([RX - 1.2, -0.9, 0])
        tp = c1 + a * RIGHT
        c2 = tp + b * RIGHT
        C1 = Circle(radius=a, color=PRIMARY, stroke_width=4).move_to(c1)
        C2 = Circle(radius=b, color=SECONDARY, stroke_width=4).move_to(c2)
        d1, d2 = dot(c1, PRIMARY), dot(c2, SECONDARY)
        self.play(Create(C1), Create(C2), FadeIn(d1), FadeIn(d2), run_time=T_NORMAL)
        self.cue(sid, "the line joining")
        ln = Line(c1, c2, color=TEXT, stroke_width=4)
        touch = dot(tp, HIGHLIGHT, 0.09)
        self.play(Create(ln), run_time=T_NORMAL)
        self.play(FadeIn(touch, scale=0.3), Flash(touch, color=HIGHLIGHT, line_length=0.18),
                  run_time=T_NORMAL)
        self.cue(sid, "So the distance")
        br1 = Brace(Line(c1, tp), DOWN, color=PRIMARY, buff=0.08)
        br2 = Brace(Line(tp, c2), DOWN, color=SECONDARY, buff=0.08)
        la = math("a", color=PRIMARY, scale=0.9).next_to(br1, DOWN, buff=0.08)
        lb = math("b", color=SECONDARY, scale=0.9).next_to(br2, DOWN, buff=0.08)
        self.play(GrowFromCenter(br1), FadeIn(la), GrowFromCenter(br2), FadeIn(lb),
                  run_time=T_NORMAL)
        res = math(r"\text{distance}", "=", "a", "+", "b", scale=1.0)
        res[2].set_color(PRIMARY)
        res[4].set_color(SECONDARY)
        res.move_to([RX, -3.0, 0])
        self.play(Write(res), run_time=T_NORMAL)
        rbox = result_box(res, color=TEXT_MUTED, buff=0.15)
        self.play(Create(rbox), run_time=T_FAST)
        self.demo = VGroup(C1, C2, d1, d2, ln, touch, br1, br2, la, lb, res, rbox)
        self.sync(sid)

    # --- The triangle of centres -----------------------------------------
    def seg_s05_triangle(self):
        sid = "s05_triangle"
        F = F_LEFT
        self.play(FadeOut(self.demo), FadeOut(self.rule_card), run_time=T_FAST)
        offs = {"A": DL, "B": DR, "C": UL}
        self.clab = {k: math(k, color=COL[k], scale=0.85).next_to(F.c(k), offs[k], buff=0.08)
                     for k in "ABC"}
        self.play(LaggedStart(*[FadeIn(self.clab[k], shift=SHIFT_IN * 0.5) for k in "ABC"],
                              lag_ratio=0.3), run_time=T_NORMAL)
        self.sides = tri_sides(F)
        rows = [("AB", "1", "2", "3", F.p(1.5, 0) + DOWN * 0.28, "Then A B"),
                ("AC", "1", "3", "4", F.p(0, 2) + LEFT * 0.28, "A C is"),
                ("BC", "2", "3", "5", F.p(1.5, 2) + UR * 0.22, "And B C")]
        cols = {"1": PRIMARY, "2": SECONDARY, "3": TERTIARY}
        self.side_eqs = VGroup()
        self.side_nums = {}
        for name, p, q, s, lp, phrase in rows:
            self.cue(sid, phrase)
            eq = math(name, "=", p, "+", q, "=", s, scale=1.0)
            eq[2].set_color(cols[p])
            eq[4].set_color(cols[q])
            eq.move_to([RX, 2.0 - 1.0 * len(self.side_eqs), 0])
            n = math(s, color=TEXT, scale=0.9).move_to(lp)
            self.play(Create(self.sides[name]), Write(eq[:5]), run_time=T_NORMAL)
            self.play(Write(eq[5:]), FadeIn(n, scale=0.5), run_time=T_FAST)
            self.side_eqs.add(eq)
            self.side_nums[s] = n
        self.sync(sid)

    # --- 3-4-5 is a right triangle ---------------------------------------
    def seg_s06_right(self):
        sid = "s06_right"
        nums = [self.side_nums[s] for s in "345"]
        self.play(LaggedStart(*[n.animate.set_color(HIGHLIGHT).scale(1.25) for n in nums],
                              lag_ratio=0.3), run_time=T_NORMAL)
        self.cue(sid, "Three squared")
        pyth = math("3^2", "+", "4^2", "=", "9", "+", "16", "=", "25", "=", "5^2", scale=1.0)
        pyth.move_to([RX, -1.2, 0])
        self.play(Write(pyth[:4]), run_time=T_NORMAL)
        self.cue(sid, "is nine plus")
        self.play(Write(pyth[4:7]), run_time=T_NORMAL)
        self.cue(sid, "which is twenty five")
        self.play(Write(pyth[7:9]), run_time=T_FAST)
        self.cue(sid, "and that is five")
        self.play(Write(pyth[9:]), run_time=T_FAST)
        self.cue(sid, "So by the converse")
        cap = caption("converse of Pythagoras  ⇒  right angle at A").next_to(pyth, DOWN, buff=0.45)
        self.rmark = right_mark(F_LEFT)
        self.play(FadeIn(cap, shift=SHIFT_IN), run_time=T_FAST)
        self.play(Create(self.rmark), run_time=T_NORMAL)
        self.play(Flash(F_LEFT.c("A") + 0.12 * (RIGHT + UP), color=HIGHLIGHT, line_length=0.18),
                  run_time=T_NORMAL)
        self.key = VGroup(pyth, cap)
        self.sync(sid)

    # --- Step 2: coordinates ---------------------------------------------
    def seg_s07_coords(self):
        sid = "s07_coords"
        F = F_ZOOM
        self.play(FadeOut(self.key), FadeOut(self.side_eqs),
                  *[FadeOut(n) for n in self.side_nums.values()],
                  *[FadeOut(l) for l in self.clab.values()], run_time=T_FAST)
        self.swap_step(2, "Use coordinates")
        new_sides = tri_sides(F)
        self.play(*[FadeOut(self.circ[k]) for k in "ABC"],
                  *[Transform(self.sides[s], new_sides[s]) for s in self.sides],
                  *[Transform(self.cdots[k], dot(F.c(k), COL[k], 0.08)) for k in "ABC"],
                  Transform(self.small, small_circle(F)),
                  Transform(self.rmark, right_mark(F, 0.3)),
                  run_time=T_SLOW, rate_func=EASE)
        xax = Arrow(F.p(0, 0), F.p(3.5, 0), buff=0, color=TEXT_MUTED, stroke_width=2,
                    tip_length=0.18, max_tip_length_to_length_ratio=0.1)
        yax = Arrow(F.p(0, 0), F.p(0, 4.35), buff=0, color=TEXT_MUTED, stroke_width=2,
                    tip_length=0.18, max_tip_length_to_length_ratio=0.1)
        xl = math("x", color=TEXT_MUTED, scale=0.8).next_to(xax.get_end(), DOWN, buff=0.12)
        yl = math("y", color=TEXT_MUTED, scale=0.8).next_to(yax.get_end(), RIGHT, buff=0.12)
        self.coord = {
            "A": math("A", "(0,0)", scale=0.8).next_to(F.c("A"), DOWN, buff=0.15),
            "B": math("B", "(3,0)", scale=0.8).next_to(F.c("B"), DOWN, buff=0.15),
            "C": math("C", "(0,4)", scale=0.8).next_to(F.c("C"), RIGHT, buff=0.2),
        }
        for k in "ABC":
            self.coord[k][0].set_color(COL[k])
        self.cue(sid, "Put point A")
        self.play(FadeIn(self.coord["A"], shift=SHIFT_IN * 0.5), run_time=T_FAST)
        self.cue(sid, "B at three")
        self.play(GrowArrow(xax), FadeIn(xl), FadeIn(self.coord["B"], shift=SHIFT_IN * 0.5),
                  run_time=T_NORMAL)
        self.cue(sid, "and C at")
        self.play(GrowArrow(yax), FadeIn(yl), FadeIn(self.coord["C"], shift=SHIFT_IN * 0.5),
                  run_time=T_NORMAL)
        self.axes = VGroup(xax, yax, xl, yl)
        self.bring_to_front(*self.sides.values(), *self.cdots.values())
        self.sync(sid)

    # --- The unknown centre O --------------------------------------------
    def seg_s08_unknown(self):
        sid = "s08_unknown"
        F = F_ZOOM
        o = F.o()
        self.play(Indicate(self.small, color=HIGHLIGHT, scale_factor=1.3), run_time=T_NORMAL)
        self.cue(sid, "Let its centre")
        self.odot = dot(o, TEXT, 0.06)
        self.olab = math("O", "(x,y)", scale=0.75).next_to(o, UR, buff=0.32)
        self.olab[0].set_color(HIGHLIGHT)
        self.play(FadeIn(self.odot, scale=0.3), FadeIn(self.olab, shift=SHIFT_IN * 0.5),
                  run_time=T_NORMAL)
        px = DashedLine(o, F.p(OX, 0), color=TEXT_MUTED, stroke_width=2, dash_length=0.06)
        py = DashedLine(o, F.p(0, OY), color=TEXT_MUTED, stroke_width=2, dash_length=0.06)
        lx = math("x", color=TEXT_MUTED, scale=0.7).next_to(F.p(OX, 0), DOWN, buff=0.12)
        ly = math("y", color=TEXT_MUTED, scale=0.7).next_to(F.p(0, OY), LEFT, buff=0.12)
        self.play(Create(px), Create(py), FadeIn(lx), FadeIn(ly), run_time=T_NORMAL)
        specs = [("A", "1", -1, "O A is", 0.36), ("B", "2", 1, "O B is", 0.32),
                 ("C", "3", -1, "and O C", 0.38)]
        self.olines, self.olabs = {}, {}
        for k, n, side, phrase, d in specs:
            self.cue(sid, phrase)
            ln = Line(o, F.c(k), color=COL[k], stroke_width=4)
            nrm = side * rotate_vector(ln.get_unit_vector(), PI / 2)
            lab = math("r", "+", n, color=COL[k], scale=0.7).move_to(ln.get_center() + d * nrm)
            self.play(Create(ln), FadeIn(lab, scale=0.6), run_time=T_NORMAL)
            self.olines[k], self.olabs[k] = ln, lab
        self.bring_to_front(self.odot)
        self.sync(sid)

    # --- Step 3: three distance equations --------------------------------
    def seg_s09_equations(self):
        sid = "s09_equations"
        self.swap_step(3, "Distance equations")
        e1 = eq_row("(1)", "x^2", "+", "y^2", "=", "(1+r)^2")
        e2 = eq_row("(2)", "(x-3)^2", "+", "y^2", "=", "(2+r)^2")
        e3 = eq_row("(3)", "x^2", "+", "(y-4)^2", "=", "(3+r)^2")
        rows = VGroup(e1, e2, e3).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rows.move_to([RX, 1.6, 0])
        self.eqs = rows
        for k, e, phrase in zip("ABC", rows, ["x squared plus y", "x minus three", "And x squared"]):
            self.cue(sid, phrase)
            e[1][4].set_color(COL[k])
            self.play(FadeIn(e[0]), Write(e[1]), self.olines[k].animate.set_stroke(width=8),
                      Indicate(self.olabs[k], color=COL[k], scale_factor=1.3), run_time=T_SLOW)
            self.play(self.olines[k].animate.set_stroke(width=4), run_time=T_FAST)
        self.sync(sid)

    # --- Plan: subtracting cancels the squares ---------------------------
    def seg_s10_plan(self):
        sid = "s10_plan"
        cap = body("3 equations, 3 unknowns:  x, y, r", color=TEXT_MUTED, size=SIZE_CAPTION)
        cap.move_to([RX, -0.4, 0])
        self.play(FadeIn(cap, shift=SHIFT_IN), run_time=T_FAST)
        self.cue(sid, "When we expand")
        sq = math(r"x^2", ",", r"\;y^2", ",", r"\;r^2", r"\;\text{in every equation}", scale=0.9)
        for i in (0, 2, 4):
            sq[i].set_color(HIGHLIGHT)
        sq.move_to([RX, -1.4, 0])
        self.play(Write(sq), run_time=T_SLOW)
        self.cue(sid, "So if we subtract")
        res = math(r"\text{subtract}", r"\;\Rightarrow\;", r"\text{the squared terms cancel}",
                   scale=0.9)
        res.move_to([RX, -2.4, 0])
        self.play(FadeIn(res, shift=SHIFT_IN), run_time=T_NORMAL)
        cross = VGroup(*[strike(sq[i]) for i in (0, 2, 4)])
        self.play(LaggedStart(*[Create(c) for c in cross], lag_ratio=0.3), run_time=T_NORMAL)
        self.sync(sid)

    # --- algebra building blocks -----------------------------------------
    def expand_row(self, sid, label, orig, exp, eo, ee, y, notes, phrases, hl):
        """Write an equation, show each bracket's expansion as a note, then expand it."""
        lab = math(label, color=TEXT_MUTED, scale=0.75).move_to([LABX, y, 0])
        o = place(math(*orig, scale=EQS), eo, y)
        e = place(math(*exp, scale=EQS), ee, y)
        self.play(FadeIn(lab), Write(o), run_time=T_NORMAL)
        ns = VGroup()
        for i, (n, ph, h) in enumerate(zip(notes, phrases, hl)):
            self.cue(sid, ph)
            m = math(n, color=TEXT_MUTED, scale=0.75).move_to([EQX, NOTE_Y[i], 0])
            self.play(FadeIn(m, shift=SHIFT_IN), Indicate(o[h], color=HIGHLIGHT, scale_factor=1.1),
                      run_time=T_NORMAL)
            ns.add(m)
        self.wait(0.6)
        self.play(FadeTransform(VGroup(*o[:eo]), VGroup(*e[:ee])),
                  ReplacementTransform(o[eo], e[ee]),
                  FadeTransform(VGroup(*o[eo + 1:]), VGroup(*e[ee + 1:])), run_time=T_NORMAL)
        self.play(FadeOut(ns), run_time=T_FAST)
        return VGroup(lab, e)

    def subtract_rows(self, sid, top, bot, ct, cb, diff, de, phrases):
        """top - bot: rule line, strike the cancelling squares, write the difference."""
        self.cue(sid, phrases[0])
        minus = math("-", color=NEGATIVE, scale=1.0).next_to(bot[0], LEFT, buff=0.15)
        rule = Line([LABX - 0.6, RULE_Y, 0], [5.0, RULE_Y, 0], color=TEXT_MUTED, stroke_width=2)
        self.play(FadeIn(minus), Create(rule), run_time=T_NORMAL)
        self.cue(sid, phrases[1])
        parts = [top[1][i] for i in ct] + [bot[1][i] for i in cb]
        marks = VGroup(*[strike(p) for p in parts])
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.15),
                  *[p.animate.set_opacity(0.45) for p in parts], run_time=T_SLOW)
        self.cue(sid, phrases[2])
        d = place(math(*diff, scale=EQS), de, DIFF_Y)
        self.play(Write(d), run_time=T_NORMAL)
        return VGroup(minus, rule, marks), d

    def solve_linear(self, sid, diff, step, se, sol, sole, var, color, slot, phrases):
        """diff -> step -> var = fraction = simplified; copy the boxed result into `slot`."""
        self.cue(sid, phrases[0])
        s1 = place(math(*step, scale=EQS), se, STEP_Y)
        self.play(FadeTransform(diff.copy(), s1), run_time=T_NORMAL)
        self.cue(sid, phrases[1])
        s2 = place(math(*sol, scale=EQS), sole, SOLVE_Y)
        s2[0].set_color(color)
        self.play(Write(s2[:3]), run_time=T_NORMAL)
        self.cue(sid, phrases[2])
        self.play(Write(s2[3:]), run_time=T_NORMAL)
        res = math(var, "=", sol[-1], scale=0.75)
        res[0].set_color(color)
        res.move_to(slot)
        box = result_box(res, color=color, buff=0.14)
        self.play(Create(result_box(s2[-1], color=color, buff=0.1)), run_time=T_FAST)
        self.play(TransformFromCopy(VGroup(s2[0], s2[1], s2[4]), res), Create(box),
                  run_time=T_NORMAL)
        return s1, s2, VGroup(res, box)

    # --- Step 4: find x ---------------------------------------------------
    def seg_s11_expand2(self):
        sid = "s11_expand2"
        self.wipe()
        self.swap_step(4, "Find x", corner=True)
        self.e2 = self.expand_row(
            sid, "(2)", ["(x-3)^2", "+", "y^2", "=", "(2+r)^2"],
            ["x^2", "-6x", "+9", "+y^2", "=", "4", "+4r", "+r^2"], 3, 4, Y_TOP,
            [r"(x-3)^2 = x^2-6x+9", r"(2+r)^2 = 4+4r+r^2"],
            ["x minus three", "And two plus r"], [0, 4])
        self.sync(sid)

    def seg_s12_expand1(self):
        sid = "s12_expand1"
        self.e1 = self.expand_row(
            sid, "(1)", ["x^2", "+", "y^2", "=", "(1+r)^2"],
            ["x^2", "+y^2", "=", "1", "+2r", "+r^2"], 3, 2, Y_BOT,
            [r"(1+r)^2 = 1+2r+r^2"], ["One plus r"], [4])
        self.sync(sid)

    def seg_s13_sub21(self):
        sid = "s13_sub21"
        self.sub_marks, self.diff = self.subtract_rows(
            sid, self.e2, self.e1, [0, 3, 7], [0, 1, 5],
            ["-6x", "+9", "=", "3", "+2r"], 2,
            ["Now subtract", "The x squared", "leaving"])
        self.sync(sid)

    def seg_s14_x(self):
        sid = "s14_x"
        work = self.solve_linear(
            sid, self.diff, ["-6x", "=", "-6", "+2r"], 1,
            ["x", "=", r"\frac{-6+2r}{-6}", "=", r"1-\frac{r}{3}"], 1,
            "x", PRIMARY, XSLOT, ["Subtract nine", "Then divide", "That gives"])
        self.xres = work[2]
        self.sync(sid)

    # --- Step 5: find y ---------------------------------------------------
    def seg_s15_expand3(self):
        sid = "s15_expand3"
        self.wipe(keep=[self.xres])
        self.swap_step(5, "Find y", corner=True)
        self.e3 = self.expand_row(
            sid, "(3)", ["x^2", "+", "(y-4)^2", "=", "(3+r)^2"],
            ["x^2", "+y^2", "-8y", "+16", "=", "9", "+6r", "+r^2"], 3, 4, Y_TOP,
            [r"(y-4)^2 = y^2-8y+16", r"(3+r)^2 = 9+6r+r^2"],
            ["y minus four", "And three plus r"], [2, 4])
        lab = math("(1)", color=TEXT_MUTED, scale=0.75).move_to([LABX, Y_BOT, 0])
        e = place(math("x^2", "+y^2", "=", "1", "+2r", "+r^2", scale=EQS), 2, Y_BOT)
        self.play(FadeIn(lab), FadeIn(e, shift=SHIFT_IN), run_time=T_NORMAL)
        self.e1 = VGroup(lab, e)
        self.sync(sid)

    def seg_s16_sub31(self):
        sid = "s16_sub31"
        self.sub_marks, self.diff = self.subtract_rows(
            sid, self.e3, self.e1, [0, 1, 7], [0, 1, 5],
            ["-8y", "+16", "=", "8", "+4r"], 2,
            ["Subtract the", "The squared terms", "and we get"])
        self.sync(sid)

    def seg_s17_y(self):
        sid = "s17_y"
        work = self.solve_linear(
            sid, self.diff, ["-8y", "=", "-8", "+4r"], 1,
            ["y", "=", r"\frac{-8+4r}{-8}", "=", r"1-\frac{r}{2}"], 1,
            "y", SECONDARY, YSLOT, ["Subtract sixteen", "Divide by", "and y equals"])
        self.yres = work[2]
        self.sync(sid)

    # --- Step 6: substitute and simplify ----------------------------------
    def seg_s18_substitute(self):
        sid = "s18_substitute"
        self.wipe(keep=[self.xres, self.yres])
        self.swap_step(6, "Substitute into (1)", corner=True)
        self.play(Indicate(self.xres, color=PRIMARY), Indicate(self.yres, color=SECONDARY),
                  run_time=T_NORMAL)
        self.cue(sid, "Substitute them")
        e1 = place(math("x^2", "+", "y^2", "=", "(1+r)^2", scale=EQS), 3, Y_TOP)
        self.play(Write(e1), run_time=T_NORMAL)
        self.cue(sid, "This gives")
        sub = place(math(r"\left(1-\frac{r}{3}\right)^2", "+", r"\left(1-\frac{r}{2}\right)^2",
                         "=", "(1+r)^2", scale=EQS), 3, Y_TOP)
        self.play(TransformFromCopy(self.xres[0][2], sub[0]), FadeOut(e1[0]),
                  TransformFromCopy(self.yres[0][2], sub[2]), FadeOut(e1[2]),
                  ReplacementTransform(e1[1], sub[1]), ReplacementTransform(e1[3], sub[3]),
                  ReplacementTransform(e1[4], sub[4]), run_time=T_SLOW)
        self.sub = sub
        self.sync(sid)

    def seg_s19_brackets(self):
        sid = "s19_brackets"
        b = place(math("1", r"-\frac{2r}{3}", r"+\frac{r^2}{9}", "+1", "-r", r"+\frac{r^2}{4}",
                       "=", "1", "+2r", "+r^2", scale=EQS), 6, 0.85)
        notes = [r"\left(1-\frac{r}{3}\right)^2 = 1-\frac{2r}{3}+\frac{r^2}{9}",
                 r"\left(1-\frac{r}{2}\right)^2 = 1-r+\frac{r^2}{4}",
                 r"(1+r)^2 = 1+2r+r^2"]
        phrases = ["One minus r over three", "One minus r over two", "And one plus r"]
        groups = [b[0:3], b[3:6], b[6:]]
        ns = VGroup()
        for i, (n, ph, g, h) in enumerate(zip(notes, phrases, groups, [0, 2, 4])):
            self.cue(sid, ph)
            m = math(n, color=TEXT_MUTED, scale=0.72).move_to([EQX, -0.55 - 1.0 * i, 0])
            self.play(FadeIn(m, shift=SHIFT_IN), Indicate(self.sub[h], color=HIGHLIGHT,
                                                          scale_factor=1.08), run_time=T_NORMAL)
            self.play(Write(g), run_time=T_NORMAL)
            ns.add(m)
        self.brackets_notes = ns
        self.rb = b
        self.sync(sid)

    def seg_s20_times36(self):
        sid = "s20_times36"
        self.play(FadeOut(self.brackets_notes), run_time=T_FAST)
        c = place(math("36", "-24r", "+4r^2", "+36", "-36r", "+9r^2", "=", "36", "+72r",
                       "+36r^2", scale=EQS), 6, -1.7, x=1.0)
        badge = tag("x 36", TERTIARY)
        badge[1].become(math(r"\times 36", color=BG, scale=0.7).move_to(badge[0]))
        badge.next_to(c, LEFT, buff=0.3)
        self.cue(sid, "multiply every term")
        self.play(FadeIn(badge, scale=0.6), run_time=T_FAST)
        self.cue(sid, "since both nine")
        self.play(Write(VGroup(*[c[i] for i in (0, 3, 4, 6, 7, 8, 9)])), run_time=T_SLOW)
        notes = math(r"36\cdot\frac{2r}{3}=24r", r"\qquad 36\cdot\frac{r^2}{9}=4r^2",
                     r"\qquad 36\cdot\frac{r^2}{4}=9r^2", color=TEXT_MUTED, scale=0.72)
        notes.move_to([0.4, -0.45, 0])
        for i, (ph, k) in enumerate(zip(["Thirty six times two r",
                                         "Thirty six times r squared over nine",
                                         "and thirty six times"], [1, 2, 5])):
            self.cue(sid, ph)
            self.play(FadeIn(notes[i], shift=SHIFT_IN),
                      Indicate(self.rb[k], color=HIGHLIGHT, scale_factor=1.12), run_time=T_NORMAL)
            self.play(Write(c[k]), run_time=T_FAST)
        self.rc, self.badge, self.mnotes = c, badge, notes
        self.sync(sid)

    def seg_s21_collect(self):
        sid = "s21_collect"
        c = self.rc
        self.play(FadeOut(self.sub), FadeOut(self.mnotes), FadeOut(self.badge),
                  self.rb.animate.set_y(Y_TOP), c.animate.set_y(0.75), run_time=T_NORMAL)
        d = place(math("72", "-60r", "+13r^2", "=", "36", "+72r", "+36r^2", scale=EQS), 3,
                  -0.4, x=c[6].get_center()[0])
        self.play(TransformFromCopy(c[6:], d[3:]), run_time=T_NORMAL)
        for (i, j), k, color, ph in [((0, 3), 0, PRIMARY, "Thirty six plus"),
                                     ((1, 4), 1, SECONDARY, "Minus twenty four"),
                                     ((2, 5), 2, TERTIARY, "And four r squared")]:
            self.cue(sid, ph)
            self.play(c[i].animate.set_color(color), c[j].animate.set_color(color), run_time=T_FAST)
            d[k].set_color(color)
            self.play(TransformFromCopy(VGroup(c[i], c[j]), d[k]), run_time=T_NORMAL)
        self.rd = d
        self.sync(sid)

    def seg_s22_move(self):
        sid = "s22_move"
        d = self.rd
        e = math("0", "=", r"(36-13)r^2", r"+(72+60)r", r"+(36-72)", scale=EQS)
        e.move_to([0.4, -1.55, 0])
        self.cue(sid, "Move everything")
        self.play(Write(e[:2]), run_time=T_FAST)
        for k, src, ph in [(2, (2, 6), "Thirty six minus thirteen"),
                           (3, (1, 5), "seventy two plus sixty"),
                           (4, (0, 4), "and thirty six minus seventy")]:
            self.cue(sid, ph)
            self.play(Indicate(d[src[0]], scale_factor=1.15), Indicate(d[src[1]], scale_factor=1.15),
                      Write(e[k]), run_time=T_NORMAL)
        self.cue(sid, "So twenty three")
        f = math("23r^2", "+132r", "-36", "=", "0", scale=EQS).move_to([0.4, -2.65, 0])
        self.play(Write(f), run_time=T_NORMAL)
        self.play(Create(result_box(f, color=HIGHLIGHT, buff=0.12)), run_time=T_FAST)
        self.quad = f
        self.sync(sid)

    # --- Step 7: quadratic formula ----------------------------------------
    def seg_s23_formula(self):
        sid = "s23_formula"
        self.wipe(keep=[self.quad])
        self.swap_step(7, "Quadratic formula", corner=True)
        self.play(self.quad.animate.scale(1.1).move_to([0, 2.5, 0]), run_time=T_NORMAL)
        self.cue(sid, "so use the quadratic")
        gen = math("r", "=", r"\frac{-b\pm\sqrt{b^2-4ac}}{2a}", scale=0.95).move_to([0, 0.25, 0])
        self.play(Write(gen), run_time=T_NORMAL)
        abc = math("a=23", r",\qquad", "b=132", r",\qquad", "c=-36", scale=0.85).move_to([0, 1.5, 0])
        for k, col, q in zip((0, 2, 4), (PRIMARY, SECONDARY, TERTIARY), (0, 1, 2)):
            abc[k].set_color(col)
        for k, q, col, ph in zip((0, 2, 4), (0, 1, 2), (PRIMARY, SECONDARY, TERTIARY),
                                 ["with a equals", "b equals", "and c equals"]):
            self.cue(sid, ph)
            parts = [abc[k]] + ([abc[k + 1]] if k < 4 else [])
            self.play(*[FadeIn(p, shift=SHIFT_IN) for p in parts],
                      self.quad[q].animate.set_color(col), run_time=T_FAST)
        sub = math("r", "=", r"\frac{-132\pm\sqrt{132^2-4(23)(-36)}}{2(23)}", scale=0.95)
        sub.move_to([0, -1.6, 0])
        self.play(FadeTransform(gen.copy(), sub), run_time=T_NORMAL)
        self.gen, self.abc, self.qsub = gen, abc, sub
        self.sync(sid)

    def seg_s24_disc(self):
        sid = "s24_disc"
        self.play(FadeOut(self.gen), FadeOut(self.abc), self.qsub.animate.move_to([0, 1.0, 0]),
                  run_time=T_NORMAL)
        disc = math(r"132^2-4(23)(-36)", "=", "17424", "+3312", "=", "20736", "=", "144^2",
                    scale=0.9).move_to([0, -0.7, 0])
        self.cue(sid, "the part under")
        self.play(Circumscribe(self.qsub, color=HIGHLIGHT), Write(disc[0]), run_time=T_SLOW)
        for ks, ph in [((1, 2), "One hundred and thirty two squared"), ((3,), "Minus four times"),
                       ((4, 5), "Together"), ((6, 7), "which is one hundred")]:
            self.cue(sid, ph)
            self.play(Write(VGroup(*[disc[k] for k in ks])), run_time=T_NORMAL)
        disc[7].set_color(HIGHLIGHT)
        self.play(Indicate(disc[7], color=HIGHLIGHT, scale_factor=1.2), run_time=T_NORMAL)
        self.disc = disc
        self.sync(sid)

    def seg_s25_roots(self):
        sid = "s25_roots"
        self.play(FadeOut(self.quad),
                  self.qsub.animate.move_to([0, 2.3, 0]),
                  self.disc.animate.move_to([0, 1.0, 0]), run_time=T_NORMAL)
        rf = math("r", "=", r"\frac{-132\pm144}{46}", scale=1.0).move_to([0, -0.4, 0])
        self.play(Write(rf), run_time=T_NORMAL)
        b1 = math("r", "=", r"\frac{12}{46}", "=", r"\frac{6}{23}", scale=1.0)
        b2 = math("r", "=", r"\frac{-276}{46}", "=", "-6", scale=1.0)
        lab1 = caption("with +")
        lab2 = caption("with −")
        g1 = VGroup(lab1, b1).arrange(DOWN, buff=0.2)
        g2 = VGroup(lab2, b2).arrange(DOWN, buff=0.2)
        VGroup(g1, g2).arrange(RIGHT, buff=1.6).move_to([0, -2.3, 0])
        self.cue(sid, "With the plus sign")
        self.play(FadeIn(lab1), Write(b1[:3]), run_time=T_NORMAL)
        self.cue(sid, "which simplifies")
        self.play(Write(b1[3:]), run_time=T_NORMAL)
        self.cue(sid, "With the minus sign")
        self.play(FadeIn(lab2), Write(b2[:3]), run_time=T_NORMAL)
        self.cue(sid, "which is minus six")
        self.play(Write(b2[3:]), run_time=T_NORMAL)
        self.b1, self.b2 = b1, b2
        self.sync(sid)

    # --- Answer -----------------------------------------------------------
    def seg_s26_answer(self):
        sid = "s26_answer"
        b1, b2 = self.b1, self.b2
        x = Cross(b2, stroke_color=NEGATIVE, stroke_width=5, scale_factor=0.9)
        self.play(Create(x), b2.animate.set_color(NEGATIVE), run_time=T_NORMAL)
        final = math("r", "=", r"\frac{6}{23}", scale=1.6).move_to([0, 0.6, 0])
        final[2].set_color(POSITIVE)
        self.cue(sid, "so r is")
        keep = {self.backdrop, self.step, b1}
        others = [m for m in self.mobjects if m not in keep]
        self.play(*[FadeOut(m) for m in others], FadeOut(b1[2]), FadeOut(b1[3]),
                  ReplacementTransform(VGroup(b1[0], b1[1], b1[4]), final), run_time=T_NORMAL)
        box = result_box(final)
        self.play(Create(box), run_time=T_FAST)
        self.cue(sid, "The answer is B")
        ans = tag("ANSWER  B", POSITIVE).next_to(box, DOWN, buff=0.5)
        self.play(FadeIn(ans, scale=0.6), run_time=T_NORMAL)
        self.answer = VGroup(final, box, ans)
        self.sync(sid)

    def seg_s27_breath(self):
        self.play(self.answer.animate.scale(1.05), rate_func=there_and_back, run_time=T_NORMAL)
        self.sync("s27_breath")

    # --- Check ------------------------------------------------------------
    def seg_s28_check(self):
        sid = "s28_check"
        F = F_CHECK
        self.clear_screen()
        self.step = None
        h = heading("Check")
        hb = pulse_bar(width=h.width * 0.8).next_to(h, DOWN, buff=0.1)
        circ = {k: big_circle(F, k) for k in "ABC"}
        sm = small_circle(F, POSITIVE)
        self.play(FadeIn(h, shift=SHIFT_IN), GrowFromEdge(hb, LEFT),
                  *[Create(circ[k]) for k in "ABC"], FadeIn(sm), run_time=T_NORMAL)
        self.cue(sid, "six over twenty three")
        approx = math(r"r", "=", r"\frac{6}{23}", r"\approx", "0.26", scale=1.1)
        approx[2].set_color(POSITIVE)
        approx.move_to([RX + 0.3, 1.0, 0])
        self.play(Write(approx), run_time=T_NORMAL)
        self.cue(sid, "That's roughly")
        ghost = circ["A"].copy().set_stroke(PRIMARY, width=3, opacity=0.9)
        self.play(ghost.animate.scale(RS).move_to(sm), run_time=T_SLOW, rate_func=EASE)
        self.play(FadeOut(ghost), run_time=T_FAST)
        ratio = math(r"\approx \tfrac{1}{4}", r"\times", r"\text{radius of circle } A", scale=0.85)
        ratio[2].set_color(PRIMARY)
        ratio.next_to(approx, DOWN, buff=0.5)
        self.play(FadeIn(ratio, shift=SHIFT_IN), run_time=T_NORMAL)
        self.cue(sid, "which matches")
        self.play(Circumscribe(sm, shape=Circle, color=POSITIVE, buff=0.12), run_time=T_SLOW)
        self.sync(sid)

    # --- Outro: Descartes' circle theorem ---------------------------------
    def seg_s29_outro(self):
        sid = "s29_outro"
        self.clear_screen()
        h = heading("Descartes' circle theorem")
        hb = pulse_bar(width=h.width * 0.7).next_to(h, DOWN, buff=0.1)
        self.play(FadeIn(h, shift=SHIFT_IN), GrowFromEdge(hb, LEFT), run_time=T_NORMAL)
        self.cue(sid, "which links")
        kdef = math("k", "=", r"\frac{1}{\text{radius}}", scale=0.85).move_to([0, 1.7, 0])
        f1 = math(r"k_4", "=", r"k_1+k_2+k_3", "+", r"2\sqrt{k_1k_2+k_2k_3+k_3k_1}", scale=0.9)
        f1.move_to([0, 0.5, 0])
        self.play(FadeIn(kdef, shift=SHIFT_IN), Write(f1), run_time=T_SLOW)
        self.cue(sid, "It gives the same")
        f2 = math(r"k_4", "=", r"\frac{23}{6}", r"\;\Rightarrow\;", "r", "=", r"\frac{6}{23}",
                  scale=0.9).move_to([0, -0.8, 0])
        f2[6].set_color(POSITIVE)
        self.play(Write(f2), run_time=T_NORMAL)
        self.cue(sid, "If you'd like")
        q = VGroup(body("Want a video on how this theorem works?"),
                   caption("Let me know in the comments")).arrange(DOWN, buff=0.2)
        qc = card(q, buff=0.3, stroke_color=TERTIARY).move_to([0, -2.4, 0])
        self.play(FadeIn(qc, shift=SHIFT_IN), run_time=T_NORMAL)
        self.sync(sid)
