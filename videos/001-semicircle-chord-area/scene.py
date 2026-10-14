import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))  # project root
from theme.theme import *

# Model lengths (problem units): big radius 10, small radius 6, half-chord 8.
S = 0.3                      # screen units per problem unit
R0, r0, HALF = 10, 6, 8
O_C = np.array([0.0, -2.1, 0.0])     # figure centre while it is alone on screen
O_L = np.array([-3.25, -1.7, 0.0])   # figure centre when sharing with the right column
RX = 3.45                            # x-centre of the right-hand column


def pt(O, x, y):
    return O + S * np.array([x, y, 0.0])


def label_out(tex, point, O, dist=0.32, color=TEXT):
    """Label placed radially outside the big arc."""
    d = point - O
    d = d / np.linalg.norm(d)
    return math(tex, color=color, scale=0.9).move_to(point + dist * d)


def build_figure(O, R=R0, r=r0, half=HALF, glow_arc=True):
    """Returns a dict of the semicircle-figure parts (all positioned around O)."""
    f = {}
    f["region"] = AnnularSector(inner_radius=S * r, outer_radius=S * R, angle=PI,
                                start_angle=0, arc_center=O, color=PRIMARY,
                                fill_opacity=0.22)
    outer = Arc(radius=S * R, start_angle=0, angle=PI, arc_center=O,
                color=PRIMARY, stroke_width=4)
    f["outer"] = glow(outer) if glow_arc else outer
    f["inner"] = Arc(radius=max(S * r, 1e-3), start_angle=0, angle=PI, arc_center=O,
                     color=NEGATIVE, stroke_width=3)
    f["base"] = VGroup(
        Line(pt(O, -R, 0), pt(O, -r, 0), color=PRIMARY, stroke_width=4),
        Line(pt(O, r, 0), pt(O, R, 0), color=PRIMARY, stroke_width=4),
    )
    f["gap"] = DashedLine(pt(O, -r, 0), pt(O, r, 0), color=TEXT_MUTED,
                          stroke_width=2, dash_length=0.08)
    f["chord"] = Line(pt(O, -half, r), pt(O, half, r), color=SECONDARY, stroke_width=4)
    f["len"] = math("16", color=SECONDARY, scale=0.85).next_to(f["chord"], UP, buff=0.1)
    A, B = pt(O, -R, 0), pt(O, R, 0)
    C, D = pt(O, -half, r), pt(O, half, r)
    f["dotsAB"] = VGroup(*[Dot(p, radius=0.06, color=TEXT) for p in (A, B)])
    f["dotsCD"] = VGroup(*[Dot(p, radius=0.06, color=TEXT) for p in (C, D)])
    f["labAB"] = VGroup(math("A", scale=0.9).next_to(A, DOWN, buff=0.18),
                        math("B", scale=0.9).next_to(B, DOWN, buff=0.18))
    f["labCD"] = VGroup(label_out("C", C, O), label_out("D", D, O))
    return f


def figure_group(f, keys=None):
    keys = keys or ["region", "gap", "base", "inner", "outer", "chord", "len",
                    "dotsAB", "dotsCD", "labAB", "labCD"]
    return VGroup(*[f[k] for k in keys])


class VideoScene(ThemedScene):
    def construct(self):
        self.load_timeline(__file__)
        self.add(brand_mark())
        for s in self.timeline["segments"]:
            getattr(self, f"seg_{s['id']}")()

    def at(self, seg_id, offset):
        """Wait until `offset` seconds into segment seg_id (to time to a phrase)."""
        dt = self.seg(seg_id)["start"] + offset - self.time
        if dt < -0.05:
            print(f"[at] {seg_id}+{offset}: late by {-dt:.2f}s")
        if dt > 1e-3:
            self.wait(dt)

    def swap_step(self, n, text):
        new = step_label(n, text).to_corner(UL, buff=0.5)
        old = getattr(self, "step", None)
        if old is not None:
            self.play(FadeOut(old, shift=UP * 0.2), FadeIn(new, shift=SHIFT_IN), run_time=T_FAST)
        else:
            self.play(FadeIn(new, shift=SHIFT_IN), run_time=T_FAST)
        self.step = new

    # --- 00:00–00:11 Hook ----------------------------------------------
    def seg_s01_hook(self):
        q = tag("QUESTION 10", SECONDARY).to_edge(UP, buff=0.55)
        title = Text(self.timeline["title"], font=FONT_HEADING, font_size=SIZE_TITLE,
                     color=TEXT, weight=BOLD).next_to(q, DOWN, buff=0.3)
        bar = pulse_bar(width=title.width * 0.7).next_to(title, DOWN, buff=0.15)
        f = build_figure(np.array([0.0, -2.9, 0.0]))
        fig = figure_group(f, ["region", "base", "inner", "outer", "chord", "len"])
        ang = 160 * DEGREES
        qmark = Text("?", font=FONT_HEADING, font_size=60, color=HIGHLIGHT, weight=BOLD).move_to(
            np.array([0.0, -2.9, 0.0]) + 2.4 * np.array([np.cos(ang), np.sin(ang), 0]))
        self.play(FadeIn(q, scale=0.6), run_time=T_FAST)
        self.play(FadeIn(title, shift=SHIFT_IN, scale=1.1), GrowFromEdge(bar, LEFT),
                  run_time=T_SLOW, rate_func=EASE)
        self.play(FadeIn(f["region"]), Create(f["outer"]), Create(f["base"]),
                  Create(f["inner"]), run_time=T_SLOW)
        self.at("s01_hook", 4.0)
        self.play(Create(f["chord"]), FadeIn(f["len"], shift=UP * 0.2), run_time=T_NORMAL)
        self.play(Indicate(f["len"], color=HIGHLIGHT, scale_factor=1.4), run_time=T_NORMAL)
        self.at("s01_hook", 7.5)
        self.play(FadeIn(qmark, scale=0.4), f["region"].animate.set_fill(opacity=0.4),
                  run_time=T_NORMAL)
        self.play(qmark.animate.scale(1.15), rate_func=there_and_back, run_time=T_NORMAL)
        self.hook = VGroup(q, title, bar, fig, qmark)
        self.sync("s01_hook")

    # --- 00:11–00:29 Setup ---------------------------------------------
    def seg_s02_setup(self):
        sid = "s02_setup"
        self.play(FadeOut(self.hook), run_time=T_FAST)
        h = heading("The setup")
        hb = pulse_bar(width=h.width * 0.8).next_to(h, DOWN, buff=0.1)
        self.play(FadeIn(h, shift=SHIFT_IN), GrowFromEdge(hb, LEFT), run_time=T_FAST)
        self.head = VGroup(h, hb)
        f = self.f = build_figure(O_C)
        # "A big semicircle sits on its diameter, A B."
        self.play(Create(f["outer"]), run_time=T_SLOW)
        self.play(Create(VGroup(f["base"][0], f["gap"], f["base"][1])),
                  FadeIn(f["dotsAB"]), FadeIn(f["labAB"], shift=UP * 0.15), run_time=T_NORMAL)
        # "A chord, C D, of length sixteen, runs parallel to A B."
        self.at(sid, 5.2)
        self.play(Create(f["chord"]), FadeIn(f["dotsCD"]), FadeIn(f["labCD"]), run_time=T_NORMAL)
        self.play(FadeIn(f["len"], shift=UP * 0.2), run_time=T_FAST)
        # parallel hint: ghost copy of AB slides up to CD
        ghost = Line(pt(O_C, -HALF, 0), pt(O_C, HALF, 0), color=SECONDARY,
                     stroke_width=3, stroke_opacity=0.6)
        self.play(ghost.animate.move_to(f["chord"]), run_time=T_NORMAL)
        self.play(FadeOut(ghost), run_time=T_FAST)
        # "A smaller semicircle, also standing on A B, just touches C D"
        self.at(sid, 10.5)
        tr = ValueTracker(0.3)
        grow = always_redraw(lambda: Arc(radius=S * tr.get_value(), start_angle=0, angle=PI,
                                         arc_center=O_C, color=NEGATIVE, stroke_width=3))
        self.add(grow)
        self.play(tr.animate.set_value(r0), run_time=T_SLOW + 0.7, rate_func=EASE)
        grow.clear_updaters()
        self.remove(grow)
        self.add(f["inner"])
        touch = Dot(pt(O_C, 0, r0), radius=0.08, color=HIGHLIGHT)
        self.play(Flash(touch, color=HIGHLIGHT, line_length=0.18), FadeIn(touch), run_time=T_NORMAL)
        # "and it is cut away."
        self.at(sid, 15.0)
        self.play(FadeIn(f["region"]), FadeOut(touch), run_time=T_NORMAL)
        self.play(f["region"].animate.set_fill(opacity=0.4), rate_func=there_and_back,
                  run_time=T_NORMAL)
        self.fig = figure_group(f)
        self.sync(sid)

    # --- 00:29–00:41.5 Question & choices -------------------------------
    def seg_s03_question(self):
        sid = "s03_question"
        h = heading("What is the shaded area?")
        hb = pulse_bar(width=h.width * 0.6).next_to(h, DOWN, buff=0.1)
        self.play(self.fig.animate.shift(O_L - O_C),
                  FadeOut(self.head[0], shift=UP * 0.2), FadeOut(self.head[1]),
                  run_time=T_NORMAL)
        self.play(FadeIn(h, shift=SHIFT_IN), GrowFromEdge(hb, LEFT), run_time=T_FAST)
        self.head = VGroup(h, hb)
        vals = ["16", "24", "32", "48", "64"]
        rows = VGroup()
        for letter, v in zip("ABCDE", vals):
            badge = tag(letter, TEXT_MUTED)
            badge[0].stretch_to_fit_width(0.6)
            badge[1].move_to(badge[0])
            val = math(v + r"\pi", scale=1.0)
            row = VGroup(badge, val).arrange(RIGHT, buff=0.35)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        cards = VGroup(*[card(r, buff=0.16) for r in rows])
        for c in cards:
            c[0].stretch_to_fit_width(2.4).align_to(c[1], LEFT).shift(LEFT * 0.16)
        cards.move_to([RX, -0.3, 0])
        self.options = cards
        self.at(sid, 4.0)
        self.play(LaggedStart(*[FadeIn(c, shift=SHIFT_IN) for c in cards], lag_ratio=0.35),
                  run_time=T_SLOW + 1.2)
        self.sync(sid)

    # --- 00:41.5–00:52 Step 1: name the radii -----------------------------
    def seg_s04_names(self):
        sid = "s04_names"
        self.play(FadeOut(self.options, shift=RIGHT * 0.3), FadeOut(self.head), run_time=T_FAST)
        self.swap_step(1, "Name the radii")
        O = O_L
        self.Odot = Dot(O, radius=0.07, color=TEXT)
        self.Olab = math("O", color=TEXT_MUTED, scale=0.8).next_to(O, DOWN, buff=0.18)
        self.play(FadeIn(self.Odot, scale=0.5), FadeIn(self.Olab), run_time=T_FAST)
        # "Call the big radius capital R"
        self.at(sid, 3.5)
        self.Rline = Line(O, pt(O, R0, 0), color=PRIMARY, stroke_width=6)
        self.Rlab = math("R", color=PRIMARY).next_to(self.Rline, UP, buff=0.12).shift(RIGHT * 0.9)
        self.play(Create(self.Rline), run_time=T_NORMAL)
        self.play(FadeIn(self.Rlab, shift=UP * 0.2), run_time=T_FAST)
        # "and the small radius little r."
        self.at(sid, 6.6)
        self.rline = Line(O, pt(O, -r0, 0), color=NEGATIVE, stroke_width=6)
        self.rlab = math("r", color=NEGATIVE).next_to(self.rline, UP, buff=0.12)
        self.play(Create(self.rline), run_time=T_NORMAL)
        self.play(FadeIn(self.rlab, shift=UP * 0.2), run_time=T_FAST)
        self.sync(sid)

    # --- 00:52–01:03.5 Step 2: area as a difference -----------------------
    def seg_s05_area(self):
        sid = "s05_area"
        self.swap_step(2, "Area = big half disc − small half disc")
        O = O_L
        big = AnnularSector(inner_radius=0, outer_radius=S * R0, angle=PI, arc_center=O,
                            color=PRIMARY, fill_opacity=0.45)
        small = AnnularSector(inner_radius=0, outer_radius=S * r0, angle=PI, arc_center=O,
                              color=NEGATIVE, fill_opacity=0.55)
        self.play(FadeIn(big), run_time=T_NORMAL)
        self.play(FadeIn(small), run_time=T_NORMAL)
        self.play(FadeOut(big), FadeOut(small), run_time=T_NORMAL)
        # "That is one half pi R squared, minus one half pi r squared."
        self.at(sid, 5.0)
        eq = math("A", "=", r"\tfrac{1}{2}\pi", "R^2", "-", r"\tfrac{1}{2}\pi", "r^2", scale=1.25)
        eq[3].set_color(PRIMARY)
        eq[6].set_color(NEGATIVE)
        eq.move_to([RX, 1.7, 0])
        self.play(Write(eq[0:4]), run_time=T_NORMAL + 0.5)
        self.play(Write(eq[4:]), run_time=T_NORMAL + 0.5)
        self.area = eq
        self.sync(sid)

    # --- 01:03.5–01:18.5 factor out ½π ---------------------------------
    def seg_s06_factor(self):
        sid = "s06_factor"
        self.play(Indicate(self.area[2], color=HIGHLIGHT), Indicate(self.area[5], color=HIGHLIGHT),
                  run_time=T_NORMAL)
        new = math("A", "=", r"\tfrac{1}{2}\pi", "(", "R^2", "-", "r^2", ")", scale=1.25)
        new[4].set_color(PRIMARY)
        new[6].set_color(NEGATIVE)
        new.move_to(self.area)
        self.at(sid, 3.0)
        self.play(TransformMatchingTex(self.area, new), run_time=T_SLOW)
        self.area = new
        # "So we only need that difference"
        self.at(sid, 8.5)
        box = SurroundingRectangle(new[3:8], color=HIGHLIGHT, buff=0.1, corner_radius=0.1)
        qm = Text("?", font=FONT_HEADING, font_size=48, color=HIGHLIGHT, weight=BOLD)
        qm.next_to(box, DOWN, buff=0.2)
        self.play(Create(box), run_time=T_NORMAL)
        self.play(FadeIn(qm, scale=0.5), run_time=T_FAST)
        self.diffbox, self.qm = box, qm
        self.sync(sid)

    # --- 01:18.5–01:33 Step 3: tangency gives height r --------------------
    def seg_s07_tangent(self):
        sid = "s07_tangent"
        O = O_L
        self.swap_step(3, "Use the tangent point")
        M = pt(O, 0, r0)
        # swing the small radius up to the tangent point
        self.play(FadeOut(self.rlab), FadeOut(self.f["len"]), run_time=T_FAST)
        self.play(Rotate(self.rline, angle=-PI / 2, about_point=O), run_time=T_SLOW, rate_func=EASE)
        self.Mdot = Dot(M, radius=0.07, color=HIGHLIGHT)
        self.Mlab = math("M", color=HIGHLIGHT, scale=0.8).next_to(M, UL, buff=0.08)
        self.play(FadeIn(self.Mdot, scale=0.4), Flash(M, color=HIGHLIGHT, line_length=0.15),
                  FadeIn(self.Mlab), run_time=T_NORMAL)
        # "So the distance from A B up to C D is exactly little r."
        self.at(sid, 7.0)
        el = 0.2
        self.elbow = VMobject(color=TEXT, stroke_width=2).set_points_as_corners(
            [M + RIGHT * el, M + RIGHT * el + DOWN * el, M + DOWN * el])
        self.rlab = math("r", color=NEGATIVE).next_to(self.rline, LEFT, buff=0.15)
        self.play(Create(self.elbow), FadeIn(self.rlab, shift=LEFT * 0.2), run_time=T_NORMAL)
        self.play(Indicate(self.rline, color=HIGHLIGHT, scale_factor=1.05),
                  Indicate(self.rlab, color=HIGHLIGHT), run_time=T_NORMAL)
        self.sync(sid)

    # --- 01:33–01:49.5 the right triangle ---------------------------------
    def seg_s08_triangle(self):
        sid = "s08_triangle"
        O = O_L
        M, D = pt(O, 0, r0), pt(O, HALF, r0)
        # "draw the big radius from the centre to D"
        self.play(FadeOut(self.Rlab), run_time=T_FAST)
        ang = np.arctan2(r0, HALF)
        self.play(Rotate(self.Rline, angle=ang, about_point=O), run_time=T_SLOW, rate_func=EASE)
        mid = O + 0.38 * (D - O)
        n = np.array([np.sin(ang), -np.cos(ang), 0])  # normal pointing down-right
        self.Rlab = math("R", color=PRIMARY).move_to(mid + 0.3 * n)
        self.play(FadeIn(self.Rlab, shift=n * 0.2), run_time=T_FAST)
        # "M splits the chord into two halves of eight."
        self.at(sid, 8.0)
        b_left = BraceBetweenPoints(self.f["chord"].get_start(), M, direction=UP, color=SECONDARY)
        b_right = BraceBetweenPoints(M, D, direction=UP, color=SECONDARY)
        eight_r = math("8", color=SECONDARY, scale=0.85).next_to(b_right, UP, buff=0.06)
        eight_l = math("8", color=SECONDARY, scale=0.85).next_to(b_left, UP, buff=0.06)
        self.play(GrowFromCenter(b_left), GrowFromCenter(b_right),
                  FadeIn(eight_l), FadeIn(eight_r), run_time=T_NORMAL)
        self.tri = Polygon(O, M, D, stroke_width=0, fill_color=HIGHLIGHT, fill_opacity=0.18)
        self.play(FadeIn(self.tri), FadeOut(b_left), FadeOut(eight_l), run_time=T_NORMAL)
        self.brace8 = VGroup(b_right, eight_r)
        self.sync(sid)

    # --- 01:49.5–02:00.5 Step 4: Pythagoras --------------------------------
    def seg_s09_pythag(self):
        sid = "s09_pythag"
        self.swap_step(4, "Pythagoras")
        self.play(self.tri.animate.set_fill(opacity=0.35), rate_func=there_and_back, run_time=T_NORMAL)
        py = math("r^2", "+", "8^2", "=", "R^2", scale=1.25)
        py[0].set_color(NEGATIVE)
        py[2].set_color(SECONDARY)
        py[4].set_color(PRIMARY)
        py.move_to([RX, -0.9, 0])
        self.at(sid, 2.0)
        self.play(Write(py), run_time=T_SLOW)
        # "Rearranging, R squared minus r squared equals sixty four."
        self.at(sid, 6.5)
        py2 = math("R^2", "-", "r^2", "=", "64", scale=1.25)
        py2[0].set_color(PRIMARY)
        py2[2].set_color(NEGATIVE)
        py2.move_to(py)
        self.play(TransformMatchingTex(py, py2, key_map={"8^2": "64", "+": "-"}, path_arc=PI / 3),
                  run_time=T_SLOW)
        self.py = py2
        self.sync(sid)

    # --- 02:00.5–02:13 Key insight --------------------------------------
    def seg_s10_insight(self):
        sid = "s10_insight"
        key = tag("KEY IDEA", HIGHLIGHT).next_to(self.py, DOWN, buff=0.55)
        self.play(FadeIn(key, scale=0.6), run_time=T_FAST)
        self.play(Circumscribe(self.py, color=HIGHLIGHT, fade_out=False), run_time=T_SLOW)
        # "and the chord hands it to us directly"  -> 64 flies up to replace "?"
        self.at(sid, 6.0)
        flying = self.py[4].copy()
        self.play(flying.animate.move_to(self.qm).set_color(HIGHLIGHT), FadeOut(self.qm),
                  run_time=T_SLOW, path_arc=-PI / 4)
        self.play(Indicate(flying, color=HIGHLIGHT, scale_factor=1.3), run_time=T_NORMAL)
        self.key, self.flying = key, flying
        self.sync(sid)

    # --- 02:13–02:20 Substitute ------------------------------------------
    def seg_s11_sub(self):
        sid = "s11_sub"
        s1 = math("A", "=", r"\tfrac{1}{2}\pi", r"\cdot", "64", scale=1.25).move_to(self.area)
        s1[4].set_color(HIGHLIGHT)
        self.play(FadeOut(self.diffbox), FadeOut(self.flying, target_position=self.area[3:8]),
                  TransformMatchingTex(self.area, s1, key_map={"(": r"\cdot"}), run_time=T_SLOW)
        self.at(sid, 3.8)
        s2 = math("A", "=", r"32\pi", scale=1.25).move_to(self.area)
        self.play(TransformMatchingTex(s1, s2, key_map={"64": r"32\pi", r"\tfrac{1}{2}\pi": r"32\pi"}),
                  run_time=T_SLOW)
        self.area = s2
        self.sync(sid)

    # --- 02:20–02:26.5 Answer --------------------------------------------
    def seg_s12_answer(self):
        sid = "s12_answer"
        big = self.area.copy().scale(1.3).move_to([RX, 1.6, 0])
        self.play(Transform(self.area, big), run_time=T_FAST)
        box = result_box(self.area)
        ans = tag("ANSWER  C", POSITIVE).next_to(box, DOWN, buff=0.3)
        self.play(Create(box), self.area.animate.set_color(POSITIVE), run_time=T_NORMAL)
        self.play(FadeIn(ans, scale=0.6), run_time=T_FAST)
        self.play(Flash(box.get_corner(UR), color=POSITIVE, line_length=0.25), run_time=T_NORMAL)
        self.ansgroup = VGroup(box, ans)
        self.sync(sid)

    # --- 02:26.5–02:45 Sanity check: slide r, area stays ------------------
    def seg_s13_check(self):
        sid = "s13_check"
        self.clear_screen()
        h = heading("Shrink the bite")
        hb = pulse_bar(width=h.width * 0.8).next_to(h, DOWN, buff=0.1)
        self.head = VGroup(h, hb)
        O = np.array([-2.9, -1.9, 0.0])
        rt = ValueTracker(r0)

        def Rv():
            return np.sqrt(rt.get_value() ** 2 + HALF ** 2)

        def make():
            rv = rt.get_value()
            f = build_figure(O, R=Rv(), r=rv, glow_arc=False)
            keys = ["region", "base", "outer", "chord", "len", "labCD", "dotsCD"]
            if rv > 0.15:
                keys += ["inner", "gap"]
            return figure_group(f, keys)

        fig = always_redraw(make)

        def row(sym, color, fn):
            lab = math(sym, "=", color=color, scale=1.1)
            num = DecimalNumber(fn(), num_decimal_places=1, color=color, font_size=46)
            num.add_updater(lambda m: m.set_value(fn()))
            return VGroup(lab, num)

        rR = row("R", PRIMARY, Rv)
        rr = row("r", NEGATIVE, lambda: rt.get_value())
        diff = math("R^2", "-", "r^2", "=", "64", scale=1.1)
        diff[0].set_color(PRIMARY)
        diff[2].set_color(NEGATIVE)
        area = math("A", "=", r"32\pi", scale=1.3, color=POSITIVE)
        panel = VGroup(rR, rr, diff, area).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        for g in (rR, rr):
            g[1].next_to(g[0], RIGHT, buff=0.2)
        panel.move_to([3.7, -0.4, 0])
        abox = result_box(area)
        self.play(FadeIn(h, shift=SHIFT_IN), GrowFromEdge(hb, LEFT), FadeIn(fig), run_time=T_NORMAL)
        self.play(LaggedStart(*[FadeIn(m, shift=SHIFT_IN) for m in (rR, rr, diff, VGroup(area, abox))],
                              lag_ratio=0.25), run_time=T_NORMAL + 0.4)
        # "shrink the small semicircle. The radii change, but the area never does."
        self.at(sid, 3.0)
        self.play(rt.animate.set_value(2.5), run_time=3.0, rate_func=smooth)
        self.play(Indicate(area, color=HIGHLIGHT), run_time=T_NORMAL)
        # "When the bite vanishes, C D becomes the diameter, R is eight"
        self.at(sid, 9.5)
        self.play(rt.animate.set_value(0.0), run_time=2.5, rate_func=smooth)
        self.play(Circumscribe(rR, color=HIGHLIGHT), run_time=T_NORMAL)
        self.at(sid, 14.0)
        self.play(Indicate(area, color=HIGHLIGHT, scale_factor=1.25), run_time=T_NORMAL)
        self.play(rt.animate.set_value(r0), run_time=2.5, rate_func=smooth)
        for g in (rR, rr):
            g[1].clear_updaters()
        fig.clear_updaters()
        self.sync(sid)

    # --- 02:45–03:03 Recap ----------------------------------------------
    def seg_s14_recap(self):
        sid = "s14_recap"
        self.clear_screen()
        h = heading("Recap")
        hb = pulse_bar(width=h.width * 1.2).next_to(h, DOWN, buff=0.1)
        self.play(FadeIn(h, shift=SHIFT_IN), GrowFromEdge(hb, LEFT), run_time=T_FAST)

        def item(n, text, formula):
            inner = VGroup(step_label(n, text), formula).arrange(RIGHT, buff=0.6)
            return card(inner, buff=0.25)

        f1 = math("A", "=", r"\tfrac{1}{2}\pi", "(", "R^2", "-", "r^2", ")")
        f1[4].set_color(PRIMARY)
        f1[6].set_color(NEGATIVE)
        f2 = math("r^2", "+", "8^2", "=", "R^2")
        f2[0].set_color(NEGATIVE)
        f2[2].set_color(SECONDARY)
        f2[4].set_color(PRIMARY)
        f3 = math(r"R^2 - r^2 = 64", r"\;\Rightarrow\;", r"A = 32\pi")
        f3[2].set_color(POSITIVE)
        cards = VGroup(
            item(1, "Write the area as a difference", f1),
            item(2, "Tangent point gives a right triangle", f2),
            item(3, "Pythagoras gives the difference", f3),
        ).arrange(DOWN, buff=0.35)
        w = max(c.width for c in cards)
        for c in cards:
            c[0].stretch_to_fit_width(w)
            c[1].align_to(c[0], LEFT).shift(RIGHT * 0.25)
            c[1][1].align_to(c[0], RIGHT).shift(LEFT * 0.25)
        cards.move_to(DOWN * 0.35)
        if cards.width > SAFE_W:
            cards.scale_to_fit_width(SAFE_W)
        self.play(FadeIn(cards[0], shift=SHIFT_IN), run_time=T_NORMAL)
        self.at(sid, 5.5)
        self.play(FadeIn(cards[1], shift=SHIFT_IN), run_time=T_NORMAL)
        self.at(sid, 10.5)
        self.play(FadeIn(cards[2], shift=SHIFT_IN), run_time=T_NORMAL)
        self.at(sid, 14.5)
        self.play(Create(result_box(f3[2], buff=0.12)), run_time=T_NORMAL)
        self.sync(sid)

    # --- 03:03–03:10 Outro ----------------------------------------------
    def seg_s15_outro(self):
        sid = "s15_outro"
        self.clear_screen()
        t1 = Text("Two radii?", font=FONT_HEADING, font_size=SIZE_HEADING, color=TEXT_MUTED, weight=BOLD)
        t2 = Text("Look for the right triangle.", font=FONT_HEADING, font_size=SIZE_TITLE,
                  color=TEXT, weight=BOLD)
        if t2.width > SAFE_W:
            t2.scale_to_fit_width(SAFE_W)
        bar = pulse_bar(width=t2.width * 0.7)
        O = np.array([0.0, -2.6, 0.0])
        tri = Polygon(O, pt(O, 0, r0) , pt(O, HALF, r0), stroke_width=0,
                      fill_color=HIGHLIGHT, fill_opacity=0.25)
        legs = VGroup(Line(O, pt(O, 0, r0), color=NEGATIVE, stroke_width=4),
                      Line(pt(O, 0, r0), pt(O, HALF, r0), color=SECONDARY, stroke_width=4),
                      glow(Line(O, pt(O, HALF, r0), color=PRIMARY, stroke_width=4)))
        icon = VGroup(tri, legs)
        grp = VGroup(t1, t2, bar).arrange(DOWN, buff=0.3).move_to(UP * 0.9)
        icon.next_to(grp, DOWN, buff=0.6)
        self.play(FadeIn(t1, shift=SHIFT_IN), run_time=T_FAST)
        self.play(FadeIn(t2, shift=SHIFT_IN, scale=1.1), GrowFromEdge(bar, LEFT),
                  run_time=T_NORMAL, rate_func=EASE)
        self.play(FadeIn(tri), Create(legs), run_time=T_NORMAL)
        self.sync(sid)
