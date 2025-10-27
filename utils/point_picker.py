import pygame
import sys
import json
import math
import numpy as np
from svgpathtools import svg2paths

SVG_PATH = 'res/svg/salida_bezier.svg'
OUTPUT_JSON = 'res/txt/landmarks.json'
DEFAULT_WINDOW_SIZE = (1200, 900)
BACKGROUND = (30, 30, 30)
DRAW_COLOR = (240, 240, 240)
POINT_COLOR = (255, 50, 50)
FONT_COLOR = (230, 230, 230)

# Labels in Spanish as requested
LABELS = [
    'mano_izquierda', 'mano_derecha',
    'codo_izquierdo', 'codo_derecho',
    'hombro_izquierdo', 'hombro_derecho',
    'pie_izquierdo', 'pie_derecho',
    'rodilla_izquierda', 'rodilla_derecha',
    'coxofemoral_izquierda', 'coxofemoral_derecha',
    'cabeza',
    'cuello',
    'cola',
    'oreja_izquierda', 'oreja_derecha',
    'ojo_izquierdo', 'ojo_derecho',
    'nariz',
    'boca',
    'pecho',
    'abdomen',
    'espalda',
]

SAMPLE_POINTS_PER_PATH = 400
MARGIN = 20


def load_svg_paths(svg_path):
    paths, attributes = svg2paths(svg_path)
    return paths


def compute_bbox(paths):
    min_x = min(p.bbox()[0] for p in paths)
    max_x = max(p.bbox()[1] for p in paths)
    min_y = min(p.bbox()[2] for p in paths)
    max_y = max(p.bbox()[3] for p in paths)
    return min_x, max_x, min_y, max_y


def sample_paths(points_list, n=SAMPLE_POINTS_PER_PATH):
    all_pts = []
    for path in points_list:
        for t in np.linspace(0, 1, n):
            p = path.point(t)
            all_pts.append((p.real, p.imag))
    return all_pts


class SVGRenderer:
    def __init__(self, svg_path, window_size=DEFAULT_WINDOW_SIZE):
        self.paths = load_svg_paths(svg_path)
        self.min_x, self.max_x, self.min_y, self.max_y = compute_bbox(self.paths)
        self.win_w, self.win_h = window_size
        # Determine scale to fit
        svg_w = self.max_x - self.min_x
        svg_h = self.max_y - self.min_y
        scale_x = (self.win_w - 2 * MARGIN) / svg_w if svg_w > 0 else 1.0
        scale_y = (self.win_h - 2 * MARGIN) / svg_h if svg_h > 0 else 1.0
        self.scale = min(scale_x, scale_y)
        # Centering offset
        total_w = svg_w * self.scale
        total_h = svg_h * self.scale
        self.offset_x = (self.win_w - total_w) / 2.0 - self.min_x * self.scale
        self.offset_y = (self.win_h - total_h) / 2.0 - self.min_y * self.scale

    def svg_to_screen(self, x, y):
        sx = x * self.scale + self.offset_x
        sy = y * self.scale + self.offset_y
        return int(sx), int(sy)

    def screen_to_svg(self, sx, sy):
        x = (sx - self.offset_x) / self.scale
        y = (sy - self.offset_y) / self.scale
        return x, y

    def draw(self, surf):
        # Draw sampled path points as lines
        for path in self.paths:
            pts = []
            for t in np.linspace(0, 1, SAMPLE_POINTS_PER_PATH):
                p = path.point(t)
                pts.append(self.svg_to_screen(p.real, p.imag))
            if len(pts) >= 2:
                pygame.draw.aalines(surf, DRAW_COLOR, False, pts)


def run_picker():
    pygame.init()
    # Detect screen resolution and adapt window size so the GUI fits the monitor
    info = pygame.display.Info()
    screen_w = min(DEFAULT_WINDOW_SIZE[0], max(600, info.current_w - 100))
    screen_h = min(DEFAULT_WINDOW_SIZE[1], max(400, info.current_h - 120))
    window_size = (screen_w, screen_h)
    screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
    pygame.display.set_caption('Capibara Landmark Picker')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    renderer = SVGRenderer(SVG_PATH, window_size)

    points = []  # list of dicts: {label, screen, svg}
    idx = 0

    info_lines = [
        'Instrucciones:',
        'Click izquierdo: marcar punto',
        'Click derecho: deshacer última marca',
        "Teclas: s=guardar, q o ESC=salir",
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_s:
                    # guardar
                    save_points(points)
                    print(f'Saved {len(points)} points to {OUTPUT_JSON}')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click -> add
                    if idx < len(LABELS):
                        mx, my = event.pos
                        svg_x, svg_y = renderer.screen_to_svg(mx, my)
                        points.append({'label': LABELS[idx], 'screen': [mx, my], 'svg': [svg_x, svg_y]})
                        print(f"Marked {LABELS[idx]} at screen=({mx},{my}) svg=({svg_x:.2f},{svg_y:.2f})")
                        idx += 1
                    else:
                        print('All labels marked. Press s to save or right-click to undo.')
                elif event.button == 3:  # right click -> undo
                    if points:
                        removed = points.pop()
                        idx = max(0, idx - 1)
                        print(f"Removed {removed['label']}")

        screen.fill(BACKGROUND)
        renderer.draw(screen)

        # Draw existing points
        for p in points:
            sx, sy = p['screen']
            pygame.draw.circle(screen, POINT_COLOR, (sx, sy), 6)
            txt = font.render(p['label'], True, FONT_COLOR)
            screen.blit(txt, (sx + 8, sy - 8))

        # Draw current label prompt
        if idx < len(LABELS):
            prompt = f"Marcar: {LABELS[idx]} ({idx+1}/{len(LABELS)})"
        else:
            prompt = 'Todos los puntos marcados. Presiona s para guardar.'
        prompt_surf = font.render(prompt, True, FONT_COLOR)
        screen.blit(prompt_surf, (10, 10))

        # Draw instructions
        for i, line in enumerate(info_lines):
            surf = font.render(line, True, FONT_COLOR)
            screen.blit(surf, (10, 40 + i * 22))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def save_points(points):
    data = {
        'svg_file': SVG_PATH,
        'labels': points,
    }
    # Ensure folder exists
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    # Quick sanity compile/test: do not auto-run in headless CI; but run when invoked directly
    run_picker()
