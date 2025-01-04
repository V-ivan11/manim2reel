from manim import *

class HolaMundo(Scene):
    def construct(self):
        # Crear el pentágono
        pentagono = RegularPolygon(n=5, color=BLUE, radius = 4)

        # Crear el texto
        texto = Tex("Hola Mundo", font_size=96)

        # Colocar el texto en el centro del pentágono
        texto.move_to(pentagono.get_center())

        # Mostrar el pentágono y el texto
        self.add(pentagono, texto)
        

class HolaMundoAnimado(Scene):
    def construct(self):
        # Crear el pentágono
        pentagono = RegularPolygon(n=5, color=BLUE, radius = 4)

        # Crear el texto
        texto = Tex("Hola Mundo", font_size=96)

        # Colocar el texto en el centro del pentágono
        texto.move_to(pentagono.get_center())

        # Mostrar el pentágono y el texto
        self.add(pentagono, texto)
        
        # Animación de aparición del pentágono y el texto
        self.play(FadeIn(pentagono), FadeIn(texto))

        # Animación de rotación del pentágono
        self.play(Rotate(pentagono, angle=PI))

        # Animación de cambio de tamaño del texto
        self.play(texto.animate.scale(1.5))

        # Animación de desplazamiento del texto hacia arriba
        self.play(texto.animate.shift(UP))

        # Animación de desaparición de ambos objetos
        self.play(FadeOut(pentagono), FadeOut(texto))
