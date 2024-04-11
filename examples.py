from manim import *
import math
import colorsys

def Color(hue: float, saturation: float, luminance: float) -> ManimColor:
    return ManimColor(colorsys.hls_to_rgb(hue, luminance, saturation))

class OpeningManim(Scene):
    def construct(self):
        title = Tex(r"This is some \LaTeX")
        basel = MathTex(r"\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}")
        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeIn(basel, shift=DOWN),
        )
        self.wait()

        transform_title = Tex("That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*(FadeOut(obj, shift=DOWN) for obj in basel)),
        )
        self.wait()

        grid = NumberPlane()
        grid_title = Tex("This is a grid", font_size=72)
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeOut(title),
            FadeIn(grid_title, shift=UP),
            Create(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid_transform_title = Tex(
            r"That was a non-linear function \\ applied to the grid",
        )
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.animate.apply_function(
                lambda p: p
                + np.array(
                    [
                        np.sin(p[1]),
                        np.sin(p[0]),
                        0,
                    ],
                ),
            ),
            run_time=3,
        )
        self.wait()
    
class SimpleScene(Scene):
    def construct(self):
        plane = NumberPlane(x_range=(-8, 8), y_range=(-15, 15))
        t = Triangle(color=DARK_BLUE, fill_opacity=0.9).scale(2)
        self.add(plane, t)

class BasicAnimations(Scene):
    def construct(self):
        polys = VGroup(
            *[RegularPolygon(5, radius=1, color=Color(hue=j/5, saturation=1, luminance=0.5), fill_opacity=0.5)
              for j in range(5)]
        ).arrange(RIGHT)
        self.play(DrawBorderThenFill(polys), run_time=2)
        self.play(
            Rotate(polys[0], PI, rate_func=lambda t: t), # rate_func=linear
            Rotate(polys[1], PI, rate_func=smooth),  # default behavior for most animations
            Rotate(polys[2], PI, rate_func=lambda t: np.sin(t*PI)),
            Rotate(polys[3], PI, rate_func=there_and_back),
            Rotate(polys[4], PI, rate_func=lambda t: 1 - abs(1-2*t)),
            run_time=2
        )
        self.wait()

class LaggingGroup(Scene):
    def construct(self):
        squares = VGroup(*[Square(color=Color(hue=j/20, saturation=1, luminance=0.5), fill_opacity=0.8) for j in range(20)])
        squares.arrange_in_grid(4, 5).scale(0.75)
        self.play(AnimationGroup(*[FadeIn(s) for s in squares], lag_ratio=0.15))

class ValueTrackerPlot(Scene):
    def construct(self):
        a = ValueTracker(1)
        ax = Axes(x_range=[-2, 2, 1], y_range=[-8.5, 8.5, 1], x_length=4, y_length=6)
        parabola = ax.plot(lambda x: a.get_value() * x**2, color=RED)
        parabola.add_updater(
            lambda mob: mob.become(ax.plot(lambda x: a.get_value() * x**2, color=RED))
        )
        a_number = DecimalNumber(
            a.get_value(),
            color=RED,
            num_decimal_places=3,
            show_ellipsis=True
        )
        a_number.add_updater(
            lambda mob: mob.set_value(a.get_value()).next_to(parabola, RIGHT)
        )
        self.add(ax, parabola, a_number)
        self.play(a.animate.set_value(2))
        self.play(a.animate.set_value(-2))
        self.play(a.animate.set_value(1))

class OptimizationProblem(Scene):
    def construct(self):
        opt_obj = MathTex(r"\max_{p_1, p_2,...,p_M} R_{sum}")
        opt_obj_details = MathTex(r"\max_{p_1, p_2,...,p_M} \sum_{k=1}^{M}\log_2\left( 1 + \frac{p_k\left|{\hat{h}_k}\right|^2}{\left|{\hat{h}_k}\right|^2\sum_{j=1}^{k-1}p_j+P\sigma^2_{\epsilon} + \sigma^2} \right)")

        subject_to = MathTex(r"\text{s.t.}")
        first_constraint = MathTex(r"C1:\quad \sum_{k=1}^{M}p_k \leq P.").next_to(subject_to, RIGHT)
        second_constraint = MathTex(r"C2:\quad p_k\geq (w_k -1)\left( \sum_{j=1}^{k-1} p_j + \frac{P\sigma_{\epsilon}^2+\sigma^2}{\left|{\hat{h}_k}\right|^2} \right ) \quad \forall k = 1,2,...,M.").next_to(first_constraint, DOWN).align_to(first_constraint, LEFT)

        constraints_group = VGroup(subject_to, first_constraint, second_constraint).scale(0.6).move_to((0,0,0))

        opt_obj_details.scale(0.65).next_to(constraints_group, UP)
        opt_obj.scale(0.65).next_to(opt_obj_details, UP)

        opt_problem = VGroup(opt_obj, opt_obj_details, constraints_group).move_to((0,0,0)).arrange(DOWN, buff= 0.5)

        self.play(AnimationGroup(*[Write(t) for t in opt_problem], lag_ratio=0.75))
        self.wait(3)

        self.play(Indicate(opt_obj_details, scale_factor= 1.15, color=ORANGE))
        self.wait(1)

        self.play(FadeOut(opt_obj, constraints_group), rate_func=smooth)
        self.play(opt_obj_details.animate.scale(1.15).move_to((0,0,0)), rate_func= smooth)
        self.wait(2)

# Pythagorean theorem using 3 squares on the sides of a triangle
class PythagoreanTheorem(Scene):
    def construct(self):
        # Create the triangle as polygon where c is the hypotenuse and a is the base
        a = 3
        b = 4
        c = math.sqrt(a**2 + b**2)
        triangle = Polygon(
            ORIGIN, RIGHT * a, RIGHT * a + UP * b,
            stroke_width=2, fill_color=BLUE, fill_opacity=0.6
        )
        self.play(Create(triangle))

        # Create the squares on the sides of the triangle
        square_a = Square(side_length=a, color=RED, fill_opacity=0.6)
        square_b = Square(side_length=b, color=GREEN, fill_opacity=0.6)
        square_c = Square(side_length=c, color=YELLOW, fill_opacity=0.6)
        
        # Position the squares
        square_a.move_to(triangle.get_left() + square_a.get_center())
        square_b.move_to(triangle.get_bottom() + square_b.get_center())
        square_c.move_to(triangle.get_right() + square_c.get_center())
        # Rotate the squares
        square_c.rotate(PI / 2, about_point=square_c.get_bottom())

        # Create the labels for the squares
        label_a = MathTex('a^2', color=RED).next_to(square_a, DOWN)
        label_b = MathTex('b^2', color=GREEN).next_to(square_b, RIGHT)
        label_c = MathTex('c^2', color=YELLOW).next_to(square_c, UP)

        self.play(Create(square_a), Create(square_b), Create(square_c))
        self.play(Write(label_a), Write(label_b), Write(label_c))
        self.wait()

class MovingPointAndArc(Scene): 
    def construct(self): 
        dot = Dot(color=RED).move_to(ORIGIN)
        arc = Arc(radius=1, angle=0, color=BLUE)

        def update_func(mob: Arc):
            mob.angle = dot.get_x()
            mob.generate_points()

        self.add(dot, arc)
        self.wait()
        self.play(dot.animate.shift(TAU * RIGHT), UpdateFromFunc(arc, update_func))


class Compass(Scene):
    def construct(self):
        # Definir la línea inicial desde el origen hasta un punto determinado
        line = Line(np.array([0, 0, 0]), np.array([3, 2, 0]), color=BLUE)

        # Definir el círculo que simula el compás
        circle = Circle(radius=line.get_length(), color=RED)

        # Añadir una punta en la línea
        arrow = Arrow(ORIGIN, UP, color=BLUE).scale(0.2).next_to(line.get_end(), direction=UP)

        # Animar la rotación de la línea y dibujar el círculo
        self.play(Create(line), Create(circle), run_time=2)
        self.play(Rotate(line, angle=PI/2, about_point=ORIGIN), Rotate(circle, angle=PI/2, about_point=ORIGIN))
        self.play(Rotate(line, angle=PI/2, about_point=ORIGIN), Rotate(circle, angle=PI/2, about_point=ORIGIN))
        self.play(Rotate(line, angle=PI/2, about_point=ORIGIN), Rotate(circle, angle=PI/2, about_point=ORIGIN))
        self.play(Rotate(line, angle=PI/2, about_point=ORIGIN), Rotate(circle, angle=PI/2, about_point=ORIGIN))
        self.play(FadeOut(line), FadeOut(circle), FadeOut(arrow))

        self.wait()


