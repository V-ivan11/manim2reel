from manim import *
import math
import random
from utils.points import obtener_coords_manim
from utils.data import cargar_csv

class Perceptron(Scene):
    """
    Explicación sencilla del perceptrón.
    """
    def construct(self):

        # Plano cartesiano
        plano = Axes(x_range=(40, 75, 5), y_range=(17, 24, 1),
                    axis_config={
                        "stroke_color": TEAL,
                        "stroke_width": 4,
                        "stroke_opacity": 0.7,
                        'tip_shape': StealthTip
                        },
                        x_length=10, y_length=10,
                    x_axis_config={
                         "decimal_number_config": {
                            "unit": "\%", 
                            "num_decimal_places": 0,
                            "color": BLUE_A
                            },
                         "font_size": 30,
                     },
                    y_axis_config={
                            "decimal_number_config": {
                                "unit": "^\\circ", 
                                "num_decimal_places": 1,
                                "color": RED_A
                            },
                            "font_size": 30
                        }
                ).add_coordinates()

        # Puntos
        puntos, etiquetas = self.puntos_clasificar()
        label_dots = []
        for i, punto in enumerate(puntos):
            dot = LabeledDot(
                Text("L" if etiquetas[i] == "Rainy" else "S", font_size=20), 
                color = DARK_BLUE if etiquetas[i] == "Rainy" else GOLD_E,
                radius= 0.2
            )
            dot.move_to(plano.c2p(punto[0], punto[1]))
            label_dots.append(dot)
        
        random.shuffle(label_dots)

        puntos_l = VGroup(*label_dots)

        # Play
        self.play(DrawBorderThenFill(plano))
        self.play(ShowIncreasingSubsets(puntos_l, rate_func=linear))
        self.wait()


    def puntos_clasificar(self):
        path = "datos/clima.csv"
        datos = cargar_csv(path)
        etiquetas = datos["Weather Condition"].values
        puntos = obtener_coords_manim(datos[["Humidity", "Temperature"]], 2)
        return puntos, etiquetas
