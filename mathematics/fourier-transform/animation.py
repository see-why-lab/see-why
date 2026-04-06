"""
See Why — Fourier Transform
============================
왜 모든 신호는 원운동의 합인가

Scene 구성:
  Scene 1: FourierIntuition    — 복잡한 신호 = 단순한 파동들의 합
  Scene 2: RotatingCircles     — 주파수 = 회전 속도, 원운동으로 신호 만들기
  Scene 3: TimeToFrequency     — 시간 도메인 ↔ 주파수 도메인
  Scene 4: FullFourierSeries   — 에피사이클로 임의 파형 근사

실행:
  manim -pql animation.py FourierIntuition
  manim -pql animation.py RotatingCircles
  manim -pql animation.py TimeToFrequency
  manim -pql animation.py FullFourierSeries
  manim -pqh animation.py FullFourierSeries   (고화질)
"""

from manim import *
import numpy as np


# ── 공통 색상 ──────────────────────────────────────────────────────────────
C_BASE    = "#CBD5E1"
C_MUTED   = "#4A5568"
C_BLUE    = "#3B82F6"
C_GREEN   = "#22C55E"
C_ORANGE  = "#F59E0B"
C_RED     = "#EF4444"
C_PURPLE  = "#8B5CF6"
C_BG      = "#07090f"


# ══════════════════════════════════════════════════════════════════════════════
# Scene 1: FourierIntuition
# "복잡한 신호는 단순한 파동들의 합이다"
# ══════════════════════════════════════════════════════════════════════════════
class FourierIntuition(Scene):
    def construct(self):
        self.camera.background_color = C_BG

        # ── 제목 ──────────────────────────────────────────────────────────
        title = Text("Fourier Transform", font="JetBrains Mono", color=C_BASE)\
            .scale(0.9).to_edge(UP, buff=0.3)
        subtitle = Text("왜 모든 신호는 원운동의 합인가",
                        font="Noto Sans KR", color=C_MUTED).scale(0.45)\
            .next_to(title, DOWN, buff=0.1)
        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(0.5)

        # ── 복잡한 신호 먼저 보여주기 ────────────────────────────────────
        ax = Axes(
            x_range=[0, TAU, PI/2],
            y_range=[-2.5, 2.5, 1],
            x_length=10, y_length=4,
            axis_config={"color": C_MUTED, "stroke_width": 1},
            tips=False,
        ).shift(DOWN * 0.5)

        def complex_signal(x):
            return (np.sin(x) + 0.5 * np.sin(2 * x) + 0.3 * np.sin(3 * x))

        complex_graph = ax.plot(complex_signal, color=C_BASE, stroke_width=2.5)
        label_complex = Text("복잡한 신호", font="Noto Sans KR",
                             color=C_BASE).scale(0.4)\
            .next_to(ax, RIGHT, buff=0.2).shift(UP * 0.5)

        question = Text("이게 뭐로 이루어져 있을까?",
                        font="Noto Sans KR", color=C_ORANGE).scale(0.5)\
            .next_to(ax, DOWN, buff=0.3)

        self.play(Create(ax), run_time=0.8)
        self.play(Create(complex_graph), run_time=2)
        self.play(FadeIn(label_complex), FadeIn(question))
        self.wait(1)

        # ── 분해: 3개의 단순한 파동 ──────────────────────────────────────
        self.play(FadeOut(question))

        axes_small = VGroup()
        graphs = VGroup()
        labels_info = [
            ("sin(x)", lambda x: np.sin(x), C_BLUE, "1번 주파수\n(기본파)"),
            ("0.5·sin(2x)", lambda x: 0.5 * np.sin(2 * x), C_GREEN, "2번 주파수\n(2배 빠름)"),
            ("0.3·sin(3x)", lambda x: 0.3 * np.sin(3 * x), C_ORANGE, "3번 주파수\n(3배 빠름)"),
        ]

        for i, (name, fn, col, info) in enumerate(labels_info):
            ax_s = Axes(
                x_range=[0, TAU, PI],
                y_range=[-1.2, 1.2, 1],
                x_length=3, y_length=1.2,
                axis_config={"color": C_MUTED, "stroke_width": 0.7},
                tips=False,
            ).shift(LEFT * 4 + RIGHT * i * 3.3 + DOWN * 0.5)
            g = ax_s.plot(fn, color=col, stroke_width=2)
            lbl = Text(name, font="JetBrains Mono", color=col).scale(0.3)\
                .next_to(ax_s, DOWN, buff=0.08)
            axes_small.add(ax_s)
            graphs.add(g)
            axes_small.add(lbl)

        # 복잡한 신호를 위로 올리고 분해 보여주기
        self.play(
            ax.animate.shift(UP * 1.2).scale(0.7),
            complex_graph.animate.shift(UP * 1.2).scale(0.7),
            label_complex.animate.shift(UP * 1.2),
            run_time=1,
        )

        decomp_text = Text("= 단순한 파동들의 합", font="Noto Sans KR",
                           color=C_MUTED).scale(0.45)\
            .next_to(ax, DOWN, buff=0.2)
        self.play(FadeIn(decomp_text))

        plus_signs = VGroup()
        for i in range(2):
            p = Text("+", color=C_MUTED).scale(0.6)\
                .shift(LEFT * 4 + RIGHT * (i * 3.3 + 1.65) + DOWN * 0.5)
            plus_signs.add(p)

        for i in range(len(labels_info)):
            ax_s = Axes(
                x_range=[0, TAU, PI],
                y_range=[-1.2, 1.2, 1],
                x_length=3, y_length=1.2,
                axis_config={"color": C_MUTED, "stroke_width": 0.7},
                tips=False,
            ).shift(LEFT * 4 + RIGHT * i * 3.3 + DOWN * 0.5)
            fn = labels_info[i][1]
            col = labels_info[i][2]
            name = labels_info[i][0]
            g = ax_s.plot(fn, color=col, stroke_width=2)
            lbl = Text(name, font="JetBrains Mono", color=col).scale(0.3)\
                .next_to(ax_s, DOWN, buff=0.08)
            self.play(
                Create(ax_s), Create(g), FadeIn(lbl),
                run_time=0.8
            )
            if i < 2:
                self.play(FadeIn(plus_signs[i]), run_time=0.3)

        self.wait(1)

        # ── 핵심 메시지 ───────────────────────────────────────────────────
        key_msg = VGroup(
            Text("Fourier의 통찰:", font="Noto Sans KR",
                 color=C_ORANGE).scale(0.5),
            Text("어떤 신호든 sin/cos 파동들의 합으로 표현할 수 있다",
                 font="Noto Sans KR", color=C_BASE).scale(0.45),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)

        self.play(FadeIn(key_msg), run_time=1)
        self.wait(2)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 2: RotatingCircles
# "주파수 = 원의 회전 속도 | 진폭 = 원의 반지름"
# ══════════════════════════════════════════════════════════════════════════════
class RotatingCircles(Scene):
    def construct(self):
        self.camera.background_color = C_BG

        # ── 레이아웃 ──────────────────────────────────────────────────────
        title = Text("sin = 원의 회전", font="Arial", color=C_BASE)\
            .scale(0.75).to_edge(UP, buff=0.25)
        self.play(FadeIn(title))

        # 왼쪽: 회전 원  /  오른쪽: 파형
        center = LEFT * 3.8 + DOWN * 0.3
        radius = 1.3

        circle = Circle(radius=radius, color=C_BLUE, stroke_width=1.5)\
            .move_to(center)
        self.play(Create(circle), run_time=0.7)

        # 진폭 라벨 — 원 왼쪽
        amp_label = Text("진폭 r", font="Arial", color=C_BLUE).scale(0.38)\
            .next_to(circle, LEFT, buff=0.15)
        self.play(FadeIn(amp_label))

        angle_tracker = ValueTracker(0)

        def get_tip():
            a = angle_tracker.get_value()
            return center + np.array([radius * np.cos(a), radius * np.sin(a), 0])

        radius_line = always_redraw(
            lambda: Line(center, get_tip(), color=C_BLUE, stroke_width=2.2)
        )
        tip_dot = always_redraw(
            lambda: Dot(get_tip(), color=C_ORANGE, radius=0.1)
        )
        self.play(Create(radius_line), FadeIn(tip_dot))

        # 오른쪽 축 — 원과 겹치지 않게
        axes_wave = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1.8, 1.8, 1],
            x_length=6.0,
            y_length=2.8,
            axis_config={"color": C_MUTED, "stroke_width": 1},
            tips=False,
        ).shift(RIGHT * 2.2 + DOWN * 0.3)

        x_label = MathTex(r"\theta", color=C_MUTED).scale(0.45)\
            .next_to(axes_wave, RIGHT, buff=0.1)
        y_label = MathTex(r"\sin\theta", color=C_ORANGE).scale(0.45)\
            .next_to(axes_wave, UP, buff=0.08)

        self.play(Create(axes_wave), FadeIn(x_label), FadeIn(y_label))

        # 수평 연결선 (원 끝 → 파형 현재 위치)
        connect_line = always_redraw(
            lambda: DashedLine(
                get_tip(),
                axes_wave.c2p(angle_tracker.get_value() % (2 * PI),
                              radius * np.sin(angle_tracker.get_value())),
                color=C_MUTED, stroke_width=0.8, dash_length=0.07
            )
        )
        self.add(connect_line)

        # 파형: updater로 점 직접 수정 (become 미사용 → 재귀 없음)
        wave_mob = VMobject(color=C_ORANGE, stroke_width=2.5)
        wave_mob.set_points_as_corners([
            axes_wave.c2p(0, 0), axes_wave.c2p(0.001, 0)
        ])

        def update_wave(mob):
            a = angle_tracker.get_value()
            if a < 0.05:
                return
            n = max(2, int(a / (2 * PI) * 150))
            pts = [
                axes_wave.c2p(a * i / n, radius * np.sin(a * i / n))
                for i in range(n + 1)
            ]
            mob.set_points_as_corners(pts)

        wave_mob.add_updater(update_wave)
        self.add(wave_mob)
        self.add(radius_line, tip_dot)

        # ── 회전 애니메이션 ───────────────────────────────────────────────
        self.play(
            angle_tracker.animate.set_value(2 * PI),
            run_time=5, rate_func=linear
        )
        wave_mob.remove_updater(update_wave)
        self.wait(0.4)

        # 주파수 설명 — 원 아래
        freq_label = Text("주파수 = 1초에 몇 바퀴",
                          font="Arial", color=C_GREEN).scale(0.38)\
            .next_to(circle, DOWN, buff=0.35)
        self.play(FadeIn(freq_label))
        self.wait(0.5)

        # ── 2배 주파수 비교 ───────────────────────────────────────────────
        compare_text = Text("2배 빠르면?", font="Arial", color=C_MUTED).scale(0.38)\
            .to_corner(UL, buff=0.6).shift(DOWN * 0.6)
        self.play(FadeIn(compare_text))

        # angle_tracker 리셋 후 2배 속도로 회전
        angle_tracker.set_value(0)
        wave2 = VMobject(color=C_GREEN, stroke_width=2.5)
        wave2.set_points_as_corners([
            axes_wave.c2p(0, 0), axes_wave.c2p(0.001, 0)
        ])

        def update_wave2(mob):
            a = angle_tracker.get_value()
            if a < 0.05:
                return
            n = max(2, int(a / (2 * PI) * 150))
            pts = [
                axes_wave.c2p(a * i / n, 0.8 * np.sin(2 * a * i / n))
                for i in range(n + 1)
            ]
            mob.set_points_as_corners(pts)

        wave2.add_updater(update_wave2)
        self.add(wave2)

        self.play(
            angle_tracker.animate.set_value(2 * PI),
            run_time=2.5, rate_func=linear
        )
        wave2.remove_updater(update_wave2)

        annot = Text("f=2: 2배 빠른 진동",
                     font="Arial", color=C_GREEN).scale(0.36)\
            .next_to(axes_wave, DOWN, buff=0.15)
        self.play(FadeIn(annot))
        self.wait(1.5)

        # ── 오일러 공식 ───────────────────────────────────────────────────
        euler = MathTex(
            r"e^{i\theta} = \cos\theta + i\sin\theta",
            color=C_BASE
        ).scale(0.65).to_edge(DOWN, buff=0.25)
        euler_explain = Text("원 위의 회전 = 복소수",
                             font="Arial", color=C_MUTED).scale(0.36)\
            .next_to(euler, UP, buff=0.12)
        self.play(FadeIn(euler_explain), FadeIn(euler))
        self.wait(2)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 3: TimeToFrequency
# "시간 도메인 → 주파수 도메인 변환"
# ══════════════════════════════════════════════════════════════════════════════
class TimeToFrequency(Scene):
    def construct(self):
        self.camera.background_color = C_BG

        title = Text("시간 → 주파수", font="Noto Sans KR", color=C_BASE)\
            .scale(0.75).to_edge(UP, buff=0.3)
        self.play(FadeIn(title))

        # ── 시간 도메인 ───────────────────────────────────────────────────
        ax_time = Axes(
            x_range=[0, TAU, PI / 2],
            y_range=[-2.2, 2.2, 1],
            x_length=6, y_length=2.8,
            axis_config={"color": C_MUTED, "stroke_width": 1},
            tips=False,
        ).shift(LEFT * 2.8 + UP * 1.2)

        ax_time_label = Text("시간 도메인", font="Noto Sans KR",
                             color=C_MUTED).scale(0.38)\
            .next_to(ax_time, UP, buff=0.1)
        x_t = Text("시간 (t)", font="Noto Sans KR",
                   color=C_MUTED).scale(0.32)\
            .next_to(ax_time, RIGHT, buff=0.1)

        freqs = [(1, 1.0, C_BLUE), (2, 0.6, C_GREEN), (3, 0.35, C_ORANGE)]

        def signal(x):
            return sum(a * np.sin(f * x) for f, a, _ in freqs)

        time_graph = ax_time.plot(signal, color=C_BASE, stroke_width=2)

        self.play(Create(ax_time), FadeIn(ax_time_label), FadeIn(x_t))
        self.play(Create(time_graph), run_time=2)
        self.wait(0.5)

        # ── 각 주파수 성분 강조 ───────────────────────────────────────────
        component_graphs = VGroup()
        for f, a, col in freqs:
            g = ax_time.plot(
                lambda x, f=f, a=a: a * np.sin(f * x),
                color=col, stroke_width=1.8, stroke_opacity=0.85
            )
            component_graphs.add(g)

        self.play(
            *[Create(g) for g in component_graphs],
            run_time=1.5
        )

        comp_labels = VGroup()
        for i, (f, a, col) in enumerate(freqs):
            lbl = MathTex(f"f={f}", color=col).scale(0.38)\
                .next_to(ax_time, DOWN, buff=0.1).shift(LEFT * 2 + RIGHT * i * 2)
            comp_labels.add(lbl)
        self.play(FadeIn(comp_labels))
        self.wait(0.8)

        # ── 변환 화살표 ───────────────────────────────────────────────────
        transform_arrow = Arrow(
            LEFT * 0.2, RIGHT * 0.8,
            color=C_ORANGE, stroke_width=3
        ).shift(DOWN * 1.2)

        dft_label = MathTex(
            r"\hat{f}(k) = \sum_{n=0}^{N-1} f(n) \cdot e^{-2\pi i k n / N}",
            color=C_ORANGE
        ).scale(0.45).next_to(transform_arrow, DOWN, buff=0.15)

        self.play(FadeOut(component_graphs), FadeOut(comp_labels))
        self.play(GrowArrow(transform_arrow), run_time=0.8)
        self.play(FadeIn(dft_label))
        self.wait(0.8)

        # ── 주파수 도메인 (스펙트럼) ──────────────────────────────────────
        ax_freq = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1.3, 0.5],
            x_length=5, y_length=2.8,
            axis_config={"color": C_MUTED, "stroke_width": 1},
            x_axis_config={"include_numbers": True,
                           "font_size": 18, "color": C_MUTED},
            tips=False,
        ).shift(RIGHT * 3.2 + UP * 1.2)

        ax_freq_label = Text("주파수 도메인", font="Noto Sans KR",
                             color=C_MUTED).scale(0.38)\
            .next_to(ax_freq, UP, buff=0.1)
        x_f = Text("주파수 (f)", font="Noto Sans KR",
                   color=C_MUTED).scale(0.32)\
            .next_to(ax_freq, RIGHT, buff=0.1)

        self.play(Create(ax_freq), FadeIn(ax_freq_label), FadeIn(x_f))

        # 스펙트럼 막대
        bars = VGroup()
        bar_labels = VGroup()
        for f, a, col in freqs:
            bar = ax_freq.get_lines_to_point(ax_freq.c2p(f, a))
            spike = ax_freq.plot(
                lambda x, f=f, a=a: a * np.exp(-50 * (x - f) ** 2),
                x_range=[f - 0.4, f + 0.4],
                color=col, stroke_width=3,
                fill_opacity=0.4
            )
            dot = Dot(ax_freq.c2p(f, a), color=col, radius=0.1)
            v_line = Line(
                ax_freq.c2p(f, 0), ax_freq.c2p(f, a),
                color=col, stroke_width=3
            )
            bars.add(v_line, dot)
            lbl = MathTex(f"a={a}", color=col).scale(0.32)\
                .next_to(dot, UP, buff=0.05)
            bar_labels.add(lbl)

        self.play(
            *[Create(b) for b in bars],
            run_time=1.5
        )
        self.play(FadeIn(bar_labels))
        self.wait(0.5)

        # ── 핵심 인사이트 ─────────────────────────────────────────────────
        insight = VGroup(
            Text("시간 도메인: 언제 어떤 값인가",
                 font="Noto Sans KR", color=C_BLUE).scale(0.4),
            Text("주파수 도메인: 어떤 주파수가 얼마나 있는가",
                 font="Noto Sans KR", color=C_GREEN).scale(0.4),
            Text("같은 신호의 두 가지 표현 — 정보 손실 없음",
                 font="Noto Sans KR", color=C_ORANGE).scale(0.4),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)\
            .to_edge(DOWN, buff=0.3)

        self.play(FadeIn(insight, shift=UP * 0.3), run_time=1.5)
        self.wait(2.5)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 4: FullFourierSeries (메인 장면)
# "에피사이클로 임의 파형 근사 — 원이 원을 도는 원"
# ══════════════════════════════════════════════════════════════════════════════
class FullFourierSeries(Scene):
    """
    여러 개의 회전 원(에피사이클)이 합쳐져서
    사각파(Square Wave)를 만들어내는 과정을 시각화.

    사각파의 푸리에 급수:
    f(x) = (4/π) * Σ sin((2k-1)x) / (2k-1)   k=1,2,3,...
    """

    N_TERMS = 7         # 사용할 항의 수 (홀수 주파수만)
    CENTER  = LEFT * 3  # 에피사이클 중심

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("에피사이클 — 원이 원을 도는 원",
                     font="Noto Sans KR", color=C_BASE).scale(0.7)\
            .to_edge(UP, buff=0.25)
        subtitle = Text("사각파를 sin파들의 합으로",
                        font="Noto Sans KR", color=C_MUTED).scale(0.4)\
            .next_to(title, DOWN, buff=0.08)
        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(0.5)

        # 푸리에 계수: 사각파 f(x) = Σ (4/π) * sin((2k-1)x)/(2k-1)
        colors = [C_BLUE, C_GREEN, C_ORANGE, C_RED, C_PURPLE,
                  YELLOW, PINK]
        coeffs = []
        for k in range(1, self.N_TERMS + 1):
            freq = 2 * k - 1       # 1, 3, 5, 7, ...
            amp  = 4 / (np.pi * freq)
            coeffs.append((freq, amp))

        # ── 에피사이클 (ValueTracker로 각도 제어) ─────────────────────────
        angle = ValueTracker(0)

        circles  = VGroup()
        radii    = VGroup()
        dots_tip = VGroup()

        SCALE = 1.3   # 전체 크기 스케일

        for i, (freq, amp) in enumerate(coeffs):
            r = amp * SCALE
            col = colors[i % len(colors)]
            c = Circle(radius=r, color=col, stroke_width=1.2,
                       stroke_opacity=0.55)
            circles.add(c)

            line = Line(ORIGIN, RIGHT * r, color=col, stroke_width=1.8)
            radii.add(line)

            dot = Dot(radius=0.06, color=col)
            dots_tip.add(dot)

        def get_tip_pos(idx):
            a = angle.get_value()
            pos = np.array(self.CENTER)
            for j in range(idx + 1):
                freq_j, amp_j = coeffs[j]
                r_j = amp_j * SCALE
                pos = pos + r_j * np.array([
                    np.cos(freq_j * a),
                    np.sin(freq_j * a),
                    0
                ])
            return pos

        def update_circles(mob):
            a = angle.get_value()
            current_center = np.array(self.CENTER)
            for i, (freq, amp) in enumerate(coeffs):
                r = amp * SCALE
                circles[i].move_to(current_center)
                tip = current_center + r * np.array([
                    np.cos(freq * a), np.sin(freq * a), 0])
                radii[i].put_start_and_end_on(current_center, tip)
                dots_tip[i].move_to(tip)
                current_center = tip

        circles.add_updater(lambda m: update_circles(m))

        self.add(circles, radii, dots_tip)

        # ── 파형 추적 ─────────────────────────────────────────────────────
        ax = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1.6, 1.6, 1],
            x_length=5.5, y_length=3.5,
            axis_config={"color": C_MUTED, "stroke_width": 0.8},
            tips=False,
        ).shift(RIGHT * 2.8)

        self.play(Create(ax), run_time=0.5)

        # 목표: 실제 사각파
        target = ax.plot(
            lambda x: sum(
                (4 / (np.pi * f)) * np.sin(f * x) for f, _ in coeffs
            ),
            color=C_BASE, stroke_width=1.2, stroke_opacity=0.4
        )
        target_label = Text("목표 파형", font="Noto Sans KR",
                            color=C_MUTED).scale(0.32)\
            .next_to(ax, UP, buff=0.05)
        self.play(Create(target), FadeIn(target_label), run_time=1)

        # 연결선 (에피사이클 끝 → 파형)
        trace_dot = Dot(radius=0.07, color=C_ORANGE)
        self.add(trace_dot)

        # 파형을 점진적으로 그리기
        drawn_wave = VMobject(color=C_ORANGE, stroke_width=2.5)
        drawn_wave.set_points_as_corners([ax.c2p(0, 0)])
        self.add(drawn_wave)

        MAX_POINTS = 300
        wave_points = []

        def update_trace(mob, dt):
            a = angle.get_value()
            # 에피사이클 끝점
            pos = np.array(self.CENTER)
            for freq, amp in coeffs:
                r = amp * SCALE
                pos = pos + r * np.array([
                    np.cos(freq * a), np.sin(freq * a), 0])
            y_val = pos[1]
            x_val = (a % (2 * PI)) / (2 * PI) * 5.5

            trace_dot.move_to(pos)

            wave_points.append(ax.c2p(a % (2 * PI), y_val))
            if len(wave_points) > 1:
                pts = wave_points[-MAX_POINTS:]
                mob.set_points_as_corners(pts)

        drawn_wave.add_updater(update_trace)

        # 연결선
        h_connect = always_redraw(
            lambda: DashedLine(
                trace_dot.get_center(),
                ax.c2p(angle.get_value() % (2 * PI),
                       trace_dot.get_center()[1]),
                color=C_MUTED, stroke_width=0.7, dash_length=0.06
            )
        )
        self.add(h_connect)

        # 텀 카운터
        term_label = always_redraw(
            lambda: Text(
                f"{self.N_TERMS}개 주파수",
                font="Noto Sans KR", color=C_ORANGE
            ).scale(0.38).to_corner(DR, buff=0.3)
        )
        self.add(term_label)

        # ── 회전 애니메이션 ───────────────────────────────────────────────
        self.play(
            angle.animate.set_value(4 * PI),
            run_time=12,
            rate_func=linear
        )

        drawn_wave.remove_updater(update_trace)
        self.wait(0.5)

        # ── 마무리 메시지 ─────────────────────────────────────────────────
        end_msg = VGroup(
            Text("원이 원을 돌면서 → 어떤 파형이든 만들 수 있다",
                 font="Noto Sans KR", color=C_ORANGE).scale(0.45),
            Text("이것이 푸리에 급수의 본질",
                 font="Noto Sans KR", color=C_BASE).scale(0.4),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)

        self.play(FadeIn(end_msg), run_time=1.2)
        self.wait(2.5)
