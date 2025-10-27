from manim import *

config.transparent = True

class SVGAnimation(Scene):
    def construct(self):
        # Cargar el SVG completo usando SVGMobject
        svg = SVGMobject('res/svg/salida_bezier.svg')
        
        # Cambiar el color del trazo a blanco para que sea visible en el fondo negro
        svg.set_stroke(WHITE, 2)
        svg.set_fill(opacity=0)  # Sin relleno
        
        # Escalar y centrar el SVG
        svg.scale(3)  # Match the scale in capibara.py for consistent debugging
        svg.move_to(ORIGIN)
        
        # Mostrar el SVG estático inicialmente
        self.add(svg)
        self.wait(1)
        
        # Animación de baile: rotaciones y movimientos
        # Girar a la izquierda
        self.play(Rotate(svg, angle=PI/6, run_time=0.5))
        # Girar a la derecha
        self.play(Rotate(svg, angle=-PI/3, run_time=0.5))
        # Volver al centro
        self.play(Rotate(svg, angle=PI/6, run_time=0.5))
        
        # Mover arriba y abajo (rebote)
        self.play(svg.animate.shift(UP * 0.5), run_time=0.3)
        self.play(svg.animate.shift(DOWN * 1.0), run_time=0.3)
        self.play(svg.animate.shift(UP * 0.5), run_time=0.3)
        
        # Más giros para simular baile
        self.play(Rotate(svg, angle=PI/4, run_time=0.4))
        self.play(Rotate(svg, angle=-PI/2, run_time=0.4))
        self.play(Rotate(svg, angle=PI/4, run_time=0.4))
        
        # Final: volver a posición original
        self.play(svg.animate.move_to(ORIGIN).rotate(0), run_time=1)
        
        self.wait(1)