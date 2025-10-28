import pygame
import sys
import json
import math
import numpy as np
from svgpathtools import svg2paths

# Add environment variable for Windows
import os
os.environ['SDL_VIDEODRIVER'] = 'windib'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SVG_PATH = os.path.join(SCRIPT_DIR, '..', 'res', 'svg', 'salida_bezier.svg')
OUTPUT_JSON = os.path.join(SCRIPT_DIR, '..', 'res', 'txt', 'colors.json')
DEFAULT_WINDOW_SIZE = (1024, 768)  # Adjusted window size
BACKGROUND = (30, 30, 30)
DRAW_COLOR = (240, 240, 240)
POINT_COLOR = (255, 50, 50)
FONT_COLOR = (230, 230, 230)

# Predefined colors for picker
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (0, 128, 0),    # Dark Green
    (128, 128, 128),# Gray
    (139, 69, 19),  # Brown
    (0, 0, 0),      # Black
    (255, 255, 255),# White
]

SAMPLE_POINTS_PER_PATH = 1000
MARGIN = 20
COLOR_BUTTON_SIZE = 40
COLOR_BUTTON_MARGIN = 10


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
        # Determine scale to fit SVG in left part
        svg_w = self.max_x - self.min_x
        svg_h = self.max_y - self.min_y
        scale_x = ((self.win_w - 200) - 2 * MARGIN) / svg_w if svg_w > 0 else 1.0  # Leave space for color picker
        scale_y = (self.win_h - 2 * MARGIN) / svg_h if svg_h > 0 else 1.0
        self.scale = min(scale_x, scale_y)
        # Centering offset
        total_w = svg_w * self.scale
        total_h = svg_h * self.scale
        self.offset_x = MARGIN - self.min_x * self.scale
        self.offset_y = (self.win_h - total_h) / 2.0 - self.min_y * self.scale

    def svg_to_screen(self, x, y):
        sx = x * self.scale + self.offset_x
        sy = y * self.scale + self.offset_y
        return int(sx), int(sy)

    def screen_to_svg(self, sx, sy):
        x = (sx - self.offset_x) / self.scale
        y = (sy - self.offset_y) / self.scale
        return x, y

    def draw(self, surf, path_colors=None):
        if path_colors is None:
            path_colors = {}
        # Draw sampled path points as lines (no fill) for all paths
        for i, path in enumerate(self.paths):
            color = path_colors.get(i, DRAW_COLOR)
            pts = []
            for t in np.linspace(0, 1, SAMPLE_POINTS_PER_PATH):
                p = path.point(t)
                pts.append(self.svg_to_screen(p.real, p.imag))
            if len(pts) >= 2:
                pygame.draw.aalines(surf, color, path.isclosed(), pts)


def compute_path_centers(paths):
    centers = []
    for path in paths:
        pts = [path.point(t) for t in np.linspace(0, 1, 200)]
        xs = [p.real for p in pts]
        ys = [p.imag for p in pts]
        centers.append((sum(xs)/len(xs), sum(ys)/len(ys)))
    return centers


def nearest_path_index(pt, centers):
    dists = [math.hypot(c[0]-pt[0], c[1]-pt[1]) for c in centers]
    return np.argmin(dists)


def draw_color_picker(surf, selected_color_idx):
    x_start = DEFAULT_WINDOW_SIZE[0] - 150
    y_start = 50
    for i, color in enumerate(COLORS):
        rect = pygame.Rect(x_start, y_start + i * (COLOR_BUTTON_SIZE + COLOR_BUTTON_MARGIN),
                           COLOR_BUTTON_SIZE, COLOR_BUTTON_SIZE)
        pygame.draw.rect(surf, color, rect)
        if i == selected_color_idx:
            pygame.draw.rect(surf, (255, 255, 255), rect, 3)  # Highlight selected


def run_color_picker():
    pygame.init()
    screen = pygame.display.set_mode(DEFAULT_WINDOW_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption('KaraokeCapibaraPython SVG Color Picker')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    renderer = SVGRenderer(SVG_PATH, DEFAULT_WINDOW_SIZE)
    path_centers = compute_path_centers(renderer.paths)

    # Load existing colors
    path_colors = {}
    try:
        with open(OUTPUT_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
            path_colors = {int(k): tuple(v) for k, v in data.get('path_colors', {}).items()}
    except FileNotFoundError:
        pass

    selected_color_idx = 0
    selected_color = COLORS[selected_color_idx]

    info_lines = [
        'Instrucciones:',
        'Click izquierdo en SVG: rellenar path cerrado más cercano',
        'Click en colores: seleccionar color',
        's=guardar, q o ESC=salir',
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
                    # Save
                    data = {
                        'svg_file': SVG_PATH,
                        'path_colors': {str(k): list(v) for k, v in path_colors.items()},
                    }
                    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    print(f'Saved colors to {OUTPUT_JSON}')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    mx, my = event.pos
                    # Check if clicked on color picker
                    x_start = DEFAULT_WINDOW_SIZE[0] - 150
                    y_start = 50
                    clicked_color = False
                    for i in range(len(COLORS)):
                        rect = pygame.Rect(x_start, y_start + i * (COLOR_BUTTON_SIZE + COLOR_BUTTON_MARGIN),
                                           COLOR_BUTTON_SIZE, COLOR_BUTTON_SIZE)
                        if rect.collidepoint(mx, my):
                            selected_color_idx = i
                            selected_color = COLORS[i]
                            clicked_color = True
                            break
                    if not clicked_color:
                        # Click on SVG
                        svg_x, svg_y = renderer.screen_to_svg(mx, my)
                        nearest_idx = nearest_path_index((svg_x, svg_y), path_centers)
                        path_colors[nearest_idx] = selected_color
                        print(f'Colored path {nearest_idx} with {selected_color}')

        screen.fill(BACKGROUND)
        renderer.draw(screen, path_colors)

        # Draw color picker
        draw_color_picker(screen, selected_color_idx)

        # Draw instructions
        for i, line in enumerate(info_lines):
            surf = font.render(line, True, FONT_COLOR)
            screen.blit(surf, (DEFAULT_WINDOW_SIZE[0] - 180, 50 + len(COLORS) * (COLOR_BUTTON_SIZE + COLOR_BUTTON_MARGIN) + 20 + i * 22))

        # Draw selected color info
        color_text = f'Color seleccionado: {selected_color}'
        surf = font.render(color_text, True, FONT_COLOR)
        screen.blit(surf, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    run_color_picker()