import os
import pygame
import numpy as np
import json
from svgpathtools import svg2paths

class Capibara:
    def __init__(self, width=900, height=700, scale=2):
        self.width = width
        self.height = height
        self.scale = scale

        # Load Manim frames
        frames_path = os.path.join(os.path.dirname(__file__), '..', 'media', 'images', 'animar_svg_manim')
        frames_path = os.path.normpath(frames_path)
        self.frames = []
        if os.path.isdir(frames_path):
            for f in sorted(os.listdir(frames_path)):
                if f.endswith('.png'):
                    try:
                        self.frames.append(pygame.image.load(os.path.join(frames_path, f)))
                    except Exception:
                        pass
        self.num_frames = len(self.frames)

        # Load SVG paths to compute centers and optional landmarks
        svg_path = os.path.join(os.path.dirname(__file__), '..', 'res', 'svg', 'salida_bezier.svg')
        svg_path = os.path.normpath(svg_path)
        try:
            self.paths, _ = svg2paths(svg_path)
        except Exception:
            self.paths = []

        # Bounding box center
        if self.paths:
            min_x = min(p.bbox()[0] for p in self.paths)
            max_x = max(p.bbox()[1] for p in self.paths)
            min_y = min(p.bbox()[2] for p in self.paths)
            max_y = max(p.bbox()[3] for p in self.paths)
            self.svg_center_x = (min_x + max_x) / 2.0
            self.svg_center_y = (min_y + max_y) / 2.0
        else:
            self.svg_center_x = 0
            self.svg_center_y = 0

        # Try to load landmarks
        self.landmarks = {}
        landmarks_file = os.path.join(os.path.dirname(__file__), '..', 'res', 'txt', 'landmarks.json')
        landmarks_file = os.path.normpath(landmarks_file)
        if os.path.exists(landmarks_file):
            try:
                with open(landmarks_file, 'r', encoding='utf-8') as f:
                    lm = json.load(f)
                    for item in lm.get('labels', []):
                        self.landmarks[item['label']] = tuple(item['svg'])
            except Exception:
                self.landmarks = {}

        # anchor point defaults to svg center
        if 'coxofemoral_izquierda' in self.landmarks and 'coxofemoral_derecha' in self.landmarks:
            lx, ly = self.landmarks['coxofemoral_izquierda']
            rx, ry = self.landmarks['coxofemoral_derecha']
            self.anchor_svg_x = (lx + rx) / 2.0
            self.anchor_svg_y = (ly + ry) / 2.0
        else:
            self.anchor_svg_x = self.svg_center_x
            self.anchor_svg_y = self.svg_center_y

    def get_ground_y(self, x):
        # Same formula used elsewhere: ground y depends on x
        return self.height - 150 + (x / float(self.width)) * 50

    def draw(self, screen, pos, time_factor, on_ground=True, angle=0):
        # Draw the current frame aligned so anchor maps to pos
        if not self.frames:
            return
        t = time_factor
        # simple frame selector: cycle over frames using time
        idx = int((t * 10) % self.num_frames) if self.num_frames > 0 else 0
        frame = self.frames[idx]

        # Scale down to match previous behaviour (Manim scale=3, Pygame effective scale ~1.5)
        scale_factor = 1.0 / 3
        new_w = int(frame.get_width() * scale_factor)
        new_h = int(frame.get_height() * scale_factor)
        try:
            scaled = pygame.transform.scale(frame, (new_w, new_h))
            actual_scale = scale_factor
        except Exception:
            scaled = frame
            actual_scale = 1.0

        # Rotate the scaled frame
        rotated = pygame.transform.rotate(scaled, angle)

        # Compute vector from svg center to anchor
        vec_x = self.anchor_svg_x - self.svg_center_x
        vec_y = self.anchor_svg_y - self.svg_center_y
        scaled_vec_x = vec_x * actual_scale
        scaled_vec_y = vec_y * actual_scale

        rect_center_x = int(pos[0] - scaled_vec_x) - 20
        rect_center_y = int(pos[1] + 280 - scaled_vec_y)
        rect = rotated.get_rect(center=(rect_center_x, rect_center_y))
        screen.blit(rotated, rect)

    # Optional helper to expose anchor
    def get_anchor_svg(self):
        return (self.anchor_svg_x, self.anchor_svg_y)
