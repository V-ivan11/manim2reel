from manim import *

# Manim configuration
config.background_color = "#ffffff"
config.pixel_height = 1080
config.pixel_width = 1920

# Imagen Perceptrón multicapa
class MLPerceptronImage(Scene):
    def construct(self):
        colors = [BLUE_E, TEAL_E, RED_E]
        input_neurons = [Circle(radius=0.5, color=colors[0]) for _ in range(3)]
        hidden_neurons_1 = [Circle(radius=0.5, color=colors[1]) for _ in range(4)]
        hidden_neurons_2 = [Circle(radius=0.5, color=colors[1]) for _ in range(5)]
        hidden_neurons_3 = [Circle(radius=0.5, color=colors[1]) for _ in range(4)]
        output_neuron = Circle(radius=0.5, color=colors[2])

        input_layer = VGroup(*input_neurons).arrange(DOWN, buff=0.5)
        hidden_layer_1 = VGroup(*hidden_neurons_1).arrange(DOWN, buff=0.5)
        hidden_layer_2 = VGroup(*hidden_neurons_2).arrange(DOWN, buff=0.5)
        hidden_layer_3 = VGroup(*hidden_neurons_3).arrange(DOWN, buff=0.5)
        output_layer = VGroup(output_neuron)

        hidden_layers = VGroup(
            hidden_layer_1, 
            hidden_layer_2,
            hidden_layer_3
        ).arrange(RIGHT, buff=2)

        layers = VGroup(
            input_layer, 
            hidden_layers,
            output_layer
        ).arrange(RIGHT, buff=2)


        input_layers = SurroundingRectangle(input_layer, color=colors[0], buff=MED_SMALL_BUFF)
        hidden_layers = SurroundingRectangle(hidden_layers, color=colors[1])
        output_layers = SurroundingRectangle(output_layer, color=colors[2], buff=MED_SMALL_BUFF)

        label_input = MathTex("p", color=BLACK, font_size=24).next_to(input_layer, DOWN)

        label_output = MathTex("m=5", color=BLACK, font_size=24).next_to(output_layer, DOWN)

        self.add(label_input, label_output)

        connections_1 = VGroup()
        connections_2 = VGroup()
        connections_3 = VGroup()
        connections_4 = VGroup()
        # Capa de entrada a capa oculta 1
        for input_neuron in input_neurons:
            for hidden_neuron in hidden_neurons_1:
                connections_1.add(Line(input_neuron.get_center(), hidden_neuron.get_center(), color=colors[0]))
        # Capa oculta 1 a capa oculta 2
        for hidden_neuron in hidden_neurons_1:
            for hidden_neuron_2 in hidden_neurons_2:
                connections_2.add(Line(hidden_neuron.get_center(), hidden_neuron_2.get_center(), color=colors[1]))
        # Capa oculta 2 a capa oculta 3
        for hidden_neuron in hidden_neurons_2:
            for hidden_neuron_3 in hidden_neurons_3:
                connections_3.add(Line(hidden_neuron.get_center(), hidden_neuron_3.get_center(), color=colors[1]))
        # Capa oculta 3 a capa de salida
        for hidden_neuron in hidden_neurons_3:
            connections_4.add(Line(hidden_neuron.get_center(), output_neuron.get_center(), color=colors[1]))


        self.add(layers)
        #self.add(input_layers, hidden_layers, output_layers)
        self.add(connections_1, connections_2, connections_3, connections_4)

        input_text = Text("Capa de entrada", color=BLACK, font_size=24).next_to(input_layer, 2*UP)
        hidden_text = Text("Capas ocultas", color=BLACK, font_size=24).next_to(hidden_layers, UP)
        output_text = Text("Capa de salida", color=BLACK, font_size=24).next_to(output_layer, 2*UP)

        self.add(input_text, hidden_text, output_text)

        eq_entrada = MathTex("a^1  = f^1(W^1p+b^1)", color = BLACK, font_size=30
            ).next_to(connections_1, 6*DOWN)
        eq_oculta = MathTex("a^{m+1}  = f^2(W^{m+1}a^m+b^{m+1})", color = BLACK, font_size=30
            ).next_to(hidden_layers, DOWN)
        eq_salida = MathTex("a^{5}  = f^3(W^{5}a^{4}+b^{5})", color = BLACK, font_size=30
            ).next_to(connections_4, 6*DOWN)
        
        buff_line = (0, 0.5, 0)
        line_connections_input = Arrow(connections_1.get_bottom() + buff_line, eq_entrada.get_top(), color= BLACK)
        line_connections_hidden_1 = Arrow(connections_2.get_bottom()+ buff_line, eq_oculta.get_top(), color=BLACK)
        line_connections_hidden_2 = Arrow(connections_3.get_bottom()+ buff_line, eq_oculta.get_top(), color=BLACK)
        line_connections_output = Arrow(connections_4.get_bottom()+ buff_line, eq_salida.get_top(), color=BLACK)

        self.add(line_connections_input, line_connections_hidden_1, line_connections_hidden_2, line_connections_output)

        self.add(eq_entrada, eq_oculta, eq_salida)

# Imagen Matriz de confusión
class ConfusionMatrix(Scene):
    def construct(self):
        t1 = MobjectTable(
            [[Text("TP", color=BLACK), Text("FP", color=BLACK)],
            [Text("FN", color=BLACK), Text("TN", color=BLACK)]],
            row_labels=[Text("Positivo", color=BLACK), Text("Negativo", color=BLACK)],
            col_labels=[Text("Positivo", color=BLACK), Text("Negativo", color=BLACK)],
            line_config={"stroke_width": 1, "color": BLACK},
            v_buff=1.5,
            )

        t1.add_highlighted_cell((2,2), color=GREEN_A)
        t1.add_highlighted_cell((3,3), color=GREEN_A)

        self.add(t1)

# Curva del aprendizaje error prueba y entrenamiento
class CurvaAprendizaje(Scene):
    def construct(self):
        # Datos
        ax = Axes(
            x_range=[0, 7],
            y_range=[0, 6],
            tips=False,
            axis_config={
                "color": BLACK,
                "stroke_color": BLACK,
                "stroke_width": 4,
                "stroke_opacity": 0.7,
                'tip_shape': StealthTip,
                "include_ticks": False,
            },
            # x label configuration
            x_axis_config={

                "unit_size": 0.5,

                "font_size": 24,
            },
            
            x_length=6, y_length=6,
        )
        # 1/x
        train_error = ax.plot(lambda x: 2/x, x_range=[0.35, 7], color=RED)
        test_error = ax.plot(lambda x: 2/x +2*x-1.7*x, x_range=[0.35, 7], color=BLUE)

        label_train =MathTex(
            "E_{train}", color=RED_E
        ).scale(0.6).next_to(train_error, RIGHT).shift(2.7*DOWN)
        label_test = MathTex(
            "E_{test}", color=BLUE_E
        ).scale(0.6).next_to(test_error, RIGHT).shift(1.2*DOWN)
        
        x_label=Tex(
            "Iteraciones", color=GRAY_E
        ).scale(0.6).next_to(ax, 4*DOWN)
        y_label=Tex(
            "Error", color=GRAY_E
        ).scale(0.6).next_to(ax, 2*LEFT)

        label_underfittings = Tex("Subajuste", color=BLACK).scale(0.6).move_to(ax.get_corner(DL)+0.3*DOWN)
        label_bestfitting = Tex("Mejor ajuste", color=BLACK).scale(0.6).move_to(ax.get_center()+3.3*DOWN).shift(0.8*LEFT)
        label_overfittings = Tex("Sobreajuste", color=BLACK).scale(0.6).move_to(ax.get_corner(DR)+0.3*DOWN).shift(0.8*LEFT)

        # sQUARE for the best fitting
        square = Square(color=GREEN_D, fill_color=WHITE, fill_opacity=0.5).scale(0.9).move_to(label_bestfitting.get_center()).shift(1.6*UP)
        self.add(square)

        self.add(label_underfittings, label_bestfitting, label_overfittings)
        self.add(label_train, label_test)
        self.add(ax, train_error, test_error, x_label, y_label)

# Ilustracion del conjunto de validación
class ConjuntoValidacion(Scene):
    def construct(self):
        label_Dataset = MathTex("D", color=BLACK).scale(0.8)
        label_Train = MathTex("D_{train}", color=BLACK).scale(0.7)
        label_val = MathTex("D_{val}", color=BLACK).scale(0.7)
        
        label_puntos = MathTex("\ldots", color=BLACK).scale(0.6)

        label_H1 = MathTex("H_1", color=BLACK).scale(0.6)
        label_H2 = MathTex("H_2", color=BLACK).scale(0.6)
        label_HM = MathTex("H_M", color=BLACK).scale(0.6)

        label_E1 = MathTex("E_1", color=BLACK).scale(0.6)
        label_E2 = MathTex("E_2", color=BLACK).scale(0.6)
        label_EM = MathTex("E_M", color=BLACK).scale(0.6)
        
        label_g1 = MathTex("g_1", color=BLACK).scale(0.6)
        label_g2 = MathTex("g_2", color=BLACK).scale(0.6)
        label_gM = MathTex("g_M", color=BLACK).scale(0.6)

        label_mejor = Tex("Tomar el mejor", color=BLACK).scale(0.45)
        label_modelo = MathTex("(H_m^*, E_m^*)", color=BLACK).scale(0.65)

        label_g_mejor = MathTex("g_{m^*}", color=BLACK).scale(0.7)

        label_tam_D = MathTex("(N)", color=BLACK).scale(0.4)
        label_tam_train = MathTex("(N-K)", color=BLACK).scale(0.4)
        label_tam_val = MathTex("(K)", color=BLACK).scale(0.4)

        # Datasets
        label_Dataset.move_to(2.5*LEFT+1.35*DOWN)
        label_Train.move_to(2.5*LEFT+1.7*UP)
        label_val.move_to(0.8*LEFT+0.7*UP)

        label_tam_D.next_to(label_Dataset, DOWN).shift(0.1*UP)
        label_tam_train.next_to(label_Train, DOWN).shift(0.1*UP)
        label_tam_val.next_to(label_val, DOWN).shift(0.1*UP)

        label_Dataset = VGroup(label_Dataset, label_tam_D)
        label_Train = VGroup(label_Train, label_tam_train)
        label_val = VGroup(label_val, label_tam_val)

        bg_Dataset = BackgroundRectangle(label_Dataset, color=GREEN_A).scale(1.5)
        bg_Train = BackgroundRectangle(label_Train, color=TEAL_A).scale(1.4)
        bg_val = BackgroundRectangle(label_val, color=BLUE_A).scale(1.4)

        self.add(bg_Dataset, bg_Train, bg_val)

        self.add(label_Dataset, label_Train, label_val)

        # Hipótesis
        hipotesis = VGroup(
            label_H1, label_H2, label_puntos.copy(), label_HM
        ).arrange(RIGHT, buff=0.7).move_to(2.5*RIGHT+2*UP)

        gs = VGroup(
            label_g1, label_g2, label_puntos.copy(), label_gM
        ).arrange(RIGHT, buff=0.75).move_to(2.5*RIGHT+1*UP)

        errores = VGroup(
            label_E1, label_E2, label_puntos.copy(), label_EM
        ).arrange(RIGHT, buff=0.7).move_to(2.5*RIGHT)

        rec_errores = SurroundingRectangle(errores, color=GREEN_E)
        label_mejor.next_to(rec_errores, DOWN).shift(0.11*UP)
        label_modelo.next_to(label_mejor, DOWN).shift(0.2*UP)

        label_g_mejor.next_to(label_modelo, DOWN).shift(0.8*DOWN)

        arrow_modelo_g = Arrow(
            label_modelo.get_bottom(), label_g_mejor.get_top(),
            color=BLACK, max_tip_length_to_length_ratio=0.3)
        arrow_D_g = Arrow(
            label_Dataset.get_right(), arrow_modelo_g.get_center(),
            color=BLACK, max_tip_length_to_length_ratio=0.04,
            max_stroke_width_to_length_ratio=0.6).scale(1.05)
        
        arrow_D_Dtrain = Arrow(
            label_Dataset.get_top(), label_Train.get_bottom(), 
            color=BLACK, max_tip_length_to_length_ratio=0.09,
            max_stroke_width_to_length_ratio=1.2)
        
        arrow_D_Dval = Arrow(
            arrow_D_Dtrain.get_center() + 0.54*UP + 0.26*LEFT, label_val.get_left(), 
            color=BLACK, max_tip_length_to_length_ratio=0.15,
            max_stroke_width_to_length_ratio=2)

        self.add(
            hipotesis, gs, errores, rec_errores, 
            label_mejor, label_modelo, label_g_mejor,
            arrow_modelo_g, arrow_D_g, arrow_D_Dtrain,
            arrow_D_Dval
        )

        # Flechas hipotesis a g a errores
        arrows_h_g = VGroup()
        arrows_g_e = VGroup()
        for i in range(4):
            if i == 2:
                continue
            arrow_h_g = Arrow(
                hipotesis[i].get_bottom(), gs[i].get_top(),
                color=BLACK, max_tip_length_to_length_ratio=0.5,
                max_stroke_width_to_length_ratio=5).scale(1.7)
            arrows_h_g.add(arrow_h_g)
            arrow_g_e = Arrow(
                gs[i].get_bottom(), errores[i].get_top(),
                color=BLACK, max_tip_length_to_length_ratio=0.5,
                max_stroke_width_to_length_ratio=6).scale(1.7)
            self.add(arrow_h_g, arrow_g_e)
            arrows_g_e.add(arrow_g_e)

        # Union datasets
        linea_train = Line(
            label_Train.get_right(), arrow_h_g.get_center(),
            color=BLACK).scale(0.94).shift(0.18*RIGHT)
        
        linea_val = Line(
            label_val.get_right(), arrow_g_e.get_center(),
            color=BLACK).scale(0.94).shift(0.15*RIGHT)

        self.add(linea_train, linea_val)

