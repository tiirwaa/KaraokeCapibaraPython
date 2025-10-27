#!/usr/bin/env python3
"""
Ejemplo de manipulación de SVG con svgpathtools y animación con pygame.

Este script carga un SVG, manipula los paths (ej: escala), y luego anima un punto moviéndose a lo largo de la primera path en pygame.
"""

import pygame
import sys
from svgpathtools import svg2paths, wsvg, Path
import numpy as np

def manipular_svg(input_file, output_file, scale_factor=1.0, translate=(0, 0)):
    """
    Carga un SVG, escala y traslada los paths, y guarda un nuevo SVG.
    """
    paths, attributes = svg2paths(input_file)

    new_paths = []
    for path in paths:
        # Escalar y trasladar cada path
        scaled_path = path.scaled(scale_factor, scale_factor)
        translated_path = scaled_path.translated(translate[0] + translate[1]*1j)  # complejo para traslación
        new_paths.append(translated_path)

    wsvg(new_paths, attributes=attributes, filename=output_file)
    print(f"SVG manipulado guardado en {output_file}")
    return new_paths

def animar_path_pygame(path, screen_width=800, screen_height=600):
    """
    Anima un punto moviéndose a lo largo del path usando pygame.
    """
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Animación SVG Path")
    clock = pygame.time.Clock()

    # Obtener puntos a lo largo del path
    total_length = path.length()
    num_points = 1000
    points = [path.point(t / num_points) for t in range(num_points + 1)]

    # Convertir a coordenadas pygame (y invertido)
    pygame_points = [(p.real, screen_height - p.imag) for p in points]

    # Dibujar el path estático
    for i in range(1, len(pygame_points)):
        pygame.draw.line(screen, (0, 0, 0), pygame_points[i-1], pygame_points[i], 2)

    # Animar un punto rojo moviéndose
    running = True
    index = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Limpiar y redibujar
        screen.fill((255, 255, 255))
        # Redibujar path
        for i in range(1, len(pygame_points)):
            pygame.draw.line(screen, (0, 0, 0), pygame_points[i-1], pygame_points[i], 2)

        # Dibujar punto animado
        if index < len(pygame_points):
            pygame.draw.circle(screen, (255, 0, 0), pygame_points[index], 5)
            index += 1
        else:
            index = 0  # Reiniciar animación

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python manipular_animar_svg.py <input_svg> [output_svg]")
        sys.exit(1)

    input_svg = sys.argv[1]
    output_svg = sys.argv[2] if len(sys.argv) > 2 else "manipulado.svg"

    # Manipular SVG
    paths = manipular_svg(input_svg, output_svg, scale_factor=1.5, translate=(50, 50))

    # Animar el primer path
    if paths:
        animar_path_pygame(paths[0])
    else:
        print("No hay paths para animar.")