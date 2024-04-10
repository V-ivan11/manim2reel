from manim import *
import math

class Ceercle(Scene):
    """
    Animaciones matemáticas.
    """
    def construct(self):
        # Introducción al círculo y su ecuación
        circulo = Circle().set_color_by_gradient("#0061ff","#60efff").set_height(10).move_to(ORIGIN)
        center = Dot(ORIGIN)
        radius = Line(ORIGIN, circulo.get_right()).set_color_by_gradient("#0061ff","#60efff")
        circulo_group = VGroup(circulo, center, radius)

        t1 = Text("¿Cómo pasamos de esto?").scale(1.5).next_to(circulo_group, 5*UP)
        t2 = Text("a esto:").scale(1.5).next_to(circulo_group, 5*UP)

        ecuacion = MathTex(r"x^2 + y^2 = r^2").move_to(ORIGIN).scale(4).set_color_by_gradient("#0061ff","#60efff")

        # Teorema de Pitágoras
        a = 3
        b = 4
        c = np.sqrt(a**2 + b**2)
        triangulo = Polygon([-b/2, -a/2, 0], [b/2, -a/2, 0], [-b/2, a/2, 0], stroke_width=2, fill_color=WHITE, fill_opacity=0.6)

        t3 = Text("Primero, recordemos al").next_to(triangulo, 25*UP)
        t4 = Text("Teorema de Pitágoras:").scale(2).next_to(t3, 2*DOWN)
        t_pitagoras = MathTex(r"a^2 + b^2 = c^2").set_color_by_gradient("#0061ff","#60efff").scale(3).next_to(triangulo, 20*DOWN)

        square_a = Square(side_length=a, color="#0061ff", fill_opacity=0.6)
        square_b = Square(side_length=b, color="#3082ff", fill_opacity=0.6)
        coords = self.get_other_coordinates([-b/2, a/2, 0], [b/2, -a/2, 0], c)
        square_c = Polygon(coords[0], coords[1], coords[3], coords[2], stroke_width=2, fill_color="#60efff", fill_opacity=0.6)

        square_a.move_to([-b/2 - a/2, 0, 0])
        square_b.move_to([0, -a/2 - b/2, 0])

        label_a = MathTex('a^2', color="#0061ff").next_to(square_a, DOWN)
        label_b = MathTex('b^2', color="#3082ff").next_to(square_b, RIGHT)
        label_c = MathTex('c^2', color="#60efff").next_to(square_c, RIGHT)

        cuadrados = VGroup(square_a, square_b, square_c, label_a, label_b, label_c)

        # Animaciones
        self.play(Write(t1), Create(circulo_group), run_time=2)
        self.wait(1)
        self.play(ReplacementTransform(t1, t2), ReplacementTransform(circulo_group, ecuacion))
        self.wait(1)
        self.play(Write(t3), ReplacementTransform(t2, t4), ReplacementTransform(ecuacion, triangulo), run_time=2)
        self.wait(1)
        self.play(Create(cuadrados), Write(t_pitagoras), run_time=4)
        self.wait(1)
        self.play(FadeOut(triangulo), FadeOut(t3), FadeOut(t4), FadeOut(t_pitagoras), FadeOut(cuadrados))
        self.wait(1)

    # Function given 2 coordinates of a rotated square (side) and lenght, returns all the coordinates of the square
    def get_other_coordinates(self, p1, p2, side):
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]
        # Get the angle of the line
        angle = np.arctan((y2 - y1)/(x2 - x1))
        # Get the other 2 points of the square
        x3 = x1 + side*np.cos(angle + np.pi/2)
        y3 = y1 + side*np.sin(angle + np.pi/2)
        x4 = x2 + side*np.cos(angle + np.pi/2)
        y4 = y2 + side*np.sin(angle + np.pi/2)
        return [[x1, y1, 0], [x2, y2, 0], [x3, y3, 0], [x4, y4, 0]]

