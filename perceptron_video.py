from manim import *
import random
from utils.points import obtener_coords_manim, lista2coords
from utils.data import cargar_csv
from utils.perceptron import Perceptron

class PerceptronReel(Scene):
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

        puntos_l = VGroup(*label_dots)

        # Play
        self.play(DrawBorderThenFill(plano))
        self.play(ShowIncreasingSubsets(puntos_l, rate_func=linear))
        self.wait()

        etiquetas = [1 if etiqueta == "Rainy" else 0 for etiqueta in etiquetas]

        label_eq = Tex("p = hardlim(Wp+b)", color=DARK_BLUE, font_size=20).move_to(5*LEFT + 3*UP)
        #label_w = Tex("w_{\text{new}} = w_{\text{old}} +(t-a)p", color=BLUE, font_size=20).move_to(5*LEFT + 2*UP)

        # Entrenamiento
        self.animation_train(plano, puntos, etiquetas, puntos_l ,iteraciones=80)
        plano.get_lines_to_point(puntos_l[0].get_center())

        self.wait()


    def puntos_clasificar(self):
        path = "datos/clima.csv"
        datos = cargar_csv(path)
        etiquetas = datos["Weather Condition"].values
        puntos = obtener_coords_manim(datos[["Humidity", "Temperature"]], 2)
        dataset = list(zip(puntos, etiquetas))
        random.seed(0)
        random.shuffle(dataset)
        puntos, etiquetas = zip(*dataset)
        return puntos, etiquetas
    
    def animation_train(self, plano, puntos, etiquetas, puntos_l, iteraciones=100):
        # Entrenamiento
        perceptron = Perceptron(2, puntos, etiquetas, 0.01)

        f_x, f_y = perceptron.frontera_decision()
        print(f_x, f_y)
        linea = Line(plano.c2p(f_x[0], f_x[1], 0), plano.c2p(f_y[0], f_y[1], 0), color=RED, stroke_width=5)     
        lineas = VGroup(linea)

        self.wait()

        texto = Text("Valores aleatorios", font_size=30).move_to(8*UP)
        textos = VGroup(texto)

        peso_inicial = Tex(f"W = [{perceptron.weights[0]}, {perceptron.weights[1]}], b = {perceptron.bias[0]}", font_size=30).move_to(8*DOWN)
        pesos_tex = VGroup(peso_inicial)

        predeccion = Text("Predicción", font_size=30).move_to(12*DOWN)
        predicciones = VGroup(predeccion)
        
        self.play(Write(texto), Write(peso_inicial))
        iters = 0

        for i in range(iteraciones):
            if iteraciones > len(puntos) - 1:
                i = i % len(puntos)
            dot = puntos_l[i]
            #lines = plano.get_lines_to_point(dot.get_center())

            x = puntos[i]
            y = etiquetas[i]
            print(x, y)
            if len(x) > 2:
                x.pop(2)

            if perceptron.predict(x) != y:
                self.play(Flash(dot))
                pred = Text(f"a: {perceptron.predict(x)}, t: {y}", font_size=30).move_to(12*DOWN)
                predicciones.add(pred)

                self.play(Unwrite(predicciones[-2]), Write(predicciones[-1]))

                perceptron.train(x, y)

                texto = Text(f"{iters+1}: Error: {str(perceptron.error())}", font_size=30).move_to(8*UP)
                textos.add(texto)

                f_x, f_y = perceptron.frontera_decision()
                linea = Line(plano.c2p(f_x[0], f_x[1], 0), plano.c2p(f_y[0], f_y[1], 0), color=RED, stroke_width=5)
                #print(linea.get_start(), linea.get_end())
                lineas.add(linea)
                #linea.move_to(ORIGIN)

                pesos = [float(perceptron.weights[0]), float(perceptron.weights[1]), 0]

                peso = Tex(
                    f"W = [{round(perceptron.weights[0], 4)}, {round(perceptron.weights[1], 4)}], b = {round(perceptron.bias[0], 4)}", font_size=30
                ).move_to(8*DOWN)
                pesos_tex.add(peso)

                
                self.play(
                    ReplacementTransform(textos[-2], textos[-1]), 
                    ReplacementTransform(lineas[-2], lineas[-1]),
                    ReplacementTransform(pesos_tex[-2], pesos_tex[-1]),
                    #ReplacementTransform(predicciones[-2], predicciones[-1]),
                    run_time=0.5
                )
                iters += 1
