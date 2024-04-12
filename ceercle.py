from manim import *
import math

class Ceercle(Scene):
    """
    Animaciones matemáticas.
    """
    def construct(self):
        # Introducción al círculo y su ecuación
        circulo = Circle(radius=5).set_color_by_gradient("#0061ff","#60efff").move_to(ORIGIN)
        circulo.set_fill(color="#60efff", opacity=0.6)

        t1 = Text("¿Cómo pasamos de esto?").scale(1.5).next_to(circulo, 5*UP)
        t2 = Text("¿a esto?").scale(1.5).next_to(circulo, 5*UP)

        ecuacion = MathTex(r"x^2 + y^2 = r^2").move_to(ORIGIN).scale(4).set_color_by_gradient("#0061ff","#60efff")

        # Teorema de Pitágoras
        a = 3
        b = 4
        c = np.sqrt(a**2 + b**2)
        triangulo = Polygon([-b/2, -a/2, 0], [b/2, -a/2, 0], [-b/2, a/2, 0], stroke_width=4, fill_color=WHITE, fill_opacity=0.6)

        t3 = Text("Primero, recordemos al").next_to(triangulo, 25*UP)
        t4 = Text("Teorema de Pitágoras:").scale(2).next_to(t3, 2*DOWN)
        t_pitagoras = MathTex(r"a^2 + b^2 = c^2").set_color_by_gradient("#0061ff","#60efff").scale(3).next_to(triangulo, 20*DOWN)

        square_a = Square(side_length=a, color="#0061ff", fill_opacity=0.6)
        square_b = Square(side_length=b, color="#3082ff", fill_opacity=0.6)
        coords = self.get_other_coordinates([-b/2, a/2, 0], [b/2, -a/2, 0], c)
        square_c = Polygon(coords[0], coords[1], coords[3], coords[2], stroke_width=2, fill_color="#60efff", fill_opacity=0.6)

        square_a.move_to([-b/2 - a/2, 0, 0])
        square_b.move_to([0, -a/2 - b/2, 0])

        label_a2 = MathTex(
            'a^2', color="#ffffff").move_to(
                square_a.get_center()
        ).scale(1.5)
        label_b2 = MathTex(
            'b^2', color="#ffffff").move_to(
                square_b.get_center()
        ).scale(1.5)
        label_c2 = MathTex(
            'c^2', color="#ffffff").move_to(
                square_c.get_center()
        ).scale(1.5)

        cuadrados = VGroup(square_a, square_b, square_c, label_a2, label_b2, label_c2)

        # Plano cartesiano
        plano = (
            NumberPlane(x_range=(-6, 6, 1), y_range=(-7, 7, 1),
                        background_line_style={
                            "stroke_color": TEAL,
                            "stroke_width": 4,
                            "stroke_opacity": 0.3,
                            },
                        )
        )
        labels_plano = plano.get_axis_labels(
            x_label="x", y_label="y"
        )

        # Animaciones
        self.add(circulo)
        self.play(Write(t1), run_time=1)
        self.wait(1)
        self.play(ReplacementTransform(t1, t2), ReplacementTransform(circulo, ecuacion))
        self.wait(1)
        self.play(Write(t3), ReplacementTransform(t2, t4), ReplacementTransform(ecuacion, triangulo), run_time=2)
        self.wait(1)
        self.play(Create(cuadrados), Write(t_pitagoras), Circumscribe(t4), run_time=4)
        self.wait(2)
        self.play( 
            FadeOut(t3), FadeOut(t4),
            t_pitagoras.animate.shift(16*UP).scale(0.8),
            FadeOut(cuadrados))
        self.play(
            triangulo.animate.shift((a/2)*UP + (b/2)*RIGHT),
            DrawBorderThenFill(plano), 
            Create(labels_plano), 
            )
        self.play(
            triangulo.animate.rotate(PI, axis = Y_AXIS)
            
        )
        label_a = always_redraw(
            lambda: MathTex('a', color="#0061ff").next_to(
                triangulo, RIGHT).scale(1.5)
        )
        label_b = always_redraw(
            lambda: MathTex('b', color="#3082ff").next_to(
                triangulo, DOWN).scale(1.5)
        )
        label_c = always_redraw(
            lambda: MathTex('c', color="#60efff").move_to(
                self.get_center_of_hypotenuse(triangulo.get_vertices())).scale(1.5)
        )
        labels_t = VGroup(label_a, label_b)
        self.play(
            triangulo.animate.set_fill(opacity=0),
            Write(labels_t),
            Write(label_c),
            run_time = 2
        )
        self.wait(1)

        # Circulo y radio
        radio_line = Line(ORIGIN, triangulo.get_vertices()[2]).set_color_by_gradient("#0061ff","#60efff")
        radio_t = always_redraw(
            lambda: MathTex('r', color="#60efff").move_to(
                self.get_location_radio(radio_line.get_start_and_end())
                )
                )
        circulo_f = Circle(radius=c, color="#60efff").move_to(ORIGIN)
        ecuacion_t = Text("Ecuación del círculo").scale(1.5).next_to(plano, 2*DOWN)
        pasos = [
                 MathTex(r"c^2 = r^2"),
                 MathTex(r"x^2 + y^2 = r^2")]
        pasos[0].set_color_by_gradient("#0061ff","#60efff").scale(1.8).move_to(t_pitagoras.get_center())
        pasos[1].set_color_by_gradient("#0061ff","#60efff").scale(2).move_to(t_pitagoras.get_center())
        # Si c es igual al radio
        texto_aux1 = Text(
            "Si c es constante con el origen", t2w={'[3:4]':BOLD}, t2c={'[3:4]':YELLOW}
        ).scale(1.5).next_to(plano, 2*DOWN)
        texto_aux2 = Text(
            "tenemos el radio", t2w={'radio':BOLD}, t2c={'radio':YELLOW}
        ).scale(1.5).next_to(texto_aux1, 2*DOWN)
        texto_aux = VGroup(texto_aux1, texto_aux2)

        self.play(
            FadeOut(labels_t),
            ReplacementTransform(label_c, radio_t),
            Create(radio_line),
            FadeOut(triangulo),
            Write(texto_aux),
            run_time = 2
        )
        self.play(ReplacementTransform(t_pitagoras, pasos[0]))
        self.wait(1)

        self.play(Rotate(radio_line, angle=-0.643501, about_point=ORIGIN), run_time=2)
        self.play(
            ReplacementTransform(pasos[0], pasos[1]),
            ReplacementTransform(texto_aux, ecuacion_t),
            AnimationGroup(
                Create(circulo_f),
                Rotate(radio_line, angle=2*PI, about_point=ORIGIN)
            ),
            run_time = 2
        )
        self.play(Circumscribe(pasos[1]))

        self.play(FadeOut(radio_t), FadeOut(radio_line), run_time=1)
        self.play(circulo_f.animate.set_fill(color="#60efff", opacity=0.6), FadeOut(plano), FadeOut(labels_plano), FadeOut(ecuacion_t))
        self.play(FadeOut(pasos[1]))


    def get_other_coordinates(self, p1, p2, side):
        """
        Retorna todas las coordenadas 3D de un cuadrado, dado dos puntos y un lado.
        """
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]

        angle = np.arctan((y2 - y1)/(x2 - x1))

        x3 = x1 + side*np.cos(angle + np.pi/2)
        y3 = y1 + side*np.sin(angle + np.pi/2)
        x4 = x2 + side*np.cos(angle + np.pi/2)
        y4 = y2 + side*np.sin(angle + np.pi/2)
        return [[x1, y1, 0], [x2, y2, 0], [x3, y3, 0], [x4, y4, 0]]
    
    def get_center_of_hypotenuse(self, vertices, extra_space=0.5):
        """
        Retorna el centro de la hipotenusa de un triángulo.
        """
        max_length = 0
        index_of_vertices = []
        for i in range(len(vertices)):
            for j in range(i+1, len(vertices)):
                length = np.linalg.norm(vertices[i] - vertices[j])
                if length > max_length:
                    max_length = length
                    index_of_vertices = [i, j]

        center = (vertices[index_of_vertices[0]] + vertices[index_of_vertices[1]])/2

        center[1] += extra_space
        return center
    
    def get_location_radio(self, vertices, extra_space=0.5):
        """
        Retorna la ubicación del centro entre 2 vertices.
        """
        center = (vertices[0] + vertices[1])/2
        center[1] += extra_space
        return center
        

