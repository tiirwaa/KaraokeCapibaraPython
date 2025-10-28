#!/usr/bin/env python3
"""
Convierte paths (polilíneas/segmentos) de un SVG a paths suaves usando
Catmull-Rom -> Cubic Bezier y guarda un nuevo SVG.

Uso:
    pip install svgpathtools
    python3 convert_svg_to_bezier.py lineal.svg salida_bezier.svg
"""
import sys
import math
from svgpathtools import svg2paths, wsvg, Path, CubicBezier

def points_from_path(path):
    """Extrae una lista de puntos (complex) de un Path.
    Si el path tiene segmentos distintos de Line, se toma start de cada segmento y al final el end.
    """
    pts = []
    for seg in path:
        pts.append(seg.start)
    if len(path) > 0:
        pts.append(path[-1].end)
    return pts

def catmull_rom_to_beziers(points, closed=False):
    """Convierte una lista de puntos (complex) a una lista de CubicBezier
    usando la aproximación Catmull-Rom a Bezier.
    Si hay menos de 2 puntos devuelve [].
    """
    n = len(points)
    if n < 2:
        return []

    beziers = []

    # función helper para obtener punto con manejo de extremos
    def P(i):
        if closed:
            return points[i % n]
        else:
            if i < 0:
                return points[0]
            elif i >= n:
                return points[-1]
            else:
                return points[i]

    # crear una curva por cada segmento entre P1->P2 (i from 0..n-2)
    last_index = n if closed else n - 1
    for i in range(0, last_index):
        P0 = P(i - 1)
        P1 = P(i)
        P2 = P(i + 1)
        P3 = P(i + 2)

        # fórmula Catmull-Rom -> Bezier (uniform parameterization)
        control1 = P1 + (P2 - P0) / 6.0
        control2 = P2 - (P3 - P1) / 6.0

        bez = CubicBezier(P1, control1, control2, P2)
        beziers.append(bez)

    return beziers

def convert_svg(input_file, output_file, closed_guess=False):
    paths, attributes = svg2paths(input_file)

    new_paths = []
    new_attrs = []

    print(f"Leídos {len(paths)} paths desde '{input_file}'")

    for i, path in enumerate(paths):
        pts = points_from_path(path)
        print(f"Path {i}: {len(pts)} puntos extraídos, longitud total aproximada = {path.length():.2f}")

        # si detectamos que el path apunta a cerrarse (último punto igual al primero) tratamos como cerrado
        closed = False
        if len(pts) > 2 and abs(pts[0] - pts[-1]) < 1e-6:
            closed = True
        elif closed_guess:
            # opción de forzar cerrado si se desea
            closed = True

        beziers = catmull_rom_to_beziers(pts, closed=closed)
        if beziers:
            new_path = Path(*beziers)
        else:
            # mantener path vacío si no hay segmentos transformados
            new_path = path

        new_paths.append(new_path)
        # conservar atributos básicos si existen
        attr = attributes[i].copy() if i < len(attributes) else {}
        new_attrs.append(attr)

    wsvg(new_paths, attributes=new_attrs, filename=output_file)
    print(f"Escrito '{output_file}' con {len(new_paths)} paths (curvas cúbicas).")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 convert_svg_to_bezier.py lineal.svg salida_bezier.svg")
        sys.exit(1)
    input_svg = sys.argv[1]
    output_svg = sys.argv[2]
    convert_svg(input_svg, output_svg, closed_guess=False)