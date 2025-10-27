from manim import *
from svgpathtools import svg2paths
import numpy as np

class SVGAnimation(Scene):
    def construct(self):
        # Cargar path desde el SVG
        paths, _ = svg2paths('res/svg/salida_bezier.svg')
        if not paths:
            self.add(Text("No se encontraron paths en el SVG."))
            return
        
        path = paths[0]  # Usar la primera ruta
        
        # Obtener bounding box para escalar y centrar
        bbox = path.bbox()
        width = bbox[1] - bbox[0]
        height = bbox[3] - bbox[2]
        scale_factor = min(14 / width, 8 / height) if width > 0 and height > 0 else 1
        center_x = (bbox[0] + bbox[1]) / 2
        center_y = (bbox[2] + bbox[3]) / 2
        
        # Convertir el path a puntos para Manim, escalados y centrados
        num_points = 200  # Más puntos para suavidad
        points = [path.point(t / num_points) for t in range(num_points + 1)]
        # Escalar y centrar
        scaled_points = [(p.real - center_x) * scale_factor for p in points]
        scaled_imag = [(p.imag - center_y) * scale_factor for p in points]
        manim_points = [np.array([scaled_points[i], scaled_imag[i], 0]) for i in range(len(points))]
        
        # Crear el objeto VMobject para el path
        svg_path = VMobject()
        svg_path.set_points_as_corners(manim_points)
        svg_path.set_stroke(WHITE, 3)  # Grosor de línea
        
        # Animar: dibujar el path desde el inicio
        self.play(Create(svg_path), run_time=2)
        
        # Crear un punto que se mueva a lo largo del path
        dot = Dot(manim_points[0], color=RED, radius=0.1)
        self.add(dot)
        
        # Animar el punto moviéndose a lo largo del path
        self.play(MoveAlongPath(dot, svg_path), run_time=4, rate_func=linear)
        
        # Pausa final
        self.wait(1)