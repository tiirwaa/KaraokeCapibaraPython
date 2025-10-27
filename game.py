import pygame
import numpy as np
import random
import sys
from audio import AudioManager
from lyrics import LyricsManager
from capibara_model import Capibara
from physics import Physics

class Game:
    def __init__(self, width=900, height=700):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Capibara Bailando")
        self.clock = pygame.time.Clock()

        self.audio_manager = AudioManager()
        self.lyrics_manager = LyricsManager()
        self.capibara = Capibara()
        self.physics = Physics(width, height)

        self.confetti_particles = []
        self.time_elapsed = 0
        self.frame_count = 0

        # Colores
        self.colors = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'brown': (139, 69, 19),
            'green': (0, 128, 0),
            'pink': (255, 192, 203),
            'dark_brown': (101, 67, 33),
            'light_brown': (160, 82, 45),
            'gray': (128, 128, 128),
            'yellow': (255, 255, 0),
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'sky': (135, 206, 235)
        }

        self.audio_manager.play_audio()

    def spawn_confetti(self, num=5):
        party_colors = [self.colors['red'], self.colors['yellow'], self.colors['green'], self.colors['blue'], self.colors['pink'], (255, 0, 255), (0, 255, 255)]
        for _ in range(num):
            x = random.randint(0, self.width)
            y = -10
            vx = random.uniform(-1, 1)
            vy = random.uniform(1, 3)
            color = random.choice(party_colors)
            size = random.randint(3, 8)
            self.confetti_particles.append({'x': x, 'y': y, 'vx': vx, 'vy': vy, 'color': color, 'size': size})

    def update_confetti(self, dt):
        for particle in self.confetti_particles[:]:
            particle['vy'] += self.physics.gravity[1] * dt
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            if particle['y'] > self.height + 10:
                self.confetti_particles.remove(particle)

    def draw_grass(self, time_factor):
        grass_height = 20 * self.capibara.scale
        grass_color = self.colors['green']
        dirt_points = [(0, self.height - 150), (self.width, self.height - 100), (self.width, self.height), (0, self.height)]
        pygame.draw.polygon(self.screen, self.colors['dark_brown'], dirt_points)
        for x in range(0, self.width, int(10 * self.capibara.scale)):
            base_y = self.height - 150 + (x / self.width) * 50
            ground_height = self.height - base_y
            for dy in range(0, int(ground_height), int(10 * self.capibara.scale)):
                y = base_y + dy
                sway = np.sin(time_factor * 2.0 + x * 0.05 + dy * 0.1) * 3 * self.capibara.scale
                pygame.draw.line(self.screen, grass_color, (x, y), (x + sway, y - grass_height), int(2 * self.capibara.scale))

    def draw_shadow(self, pos, time_factor):
        shadow_color = (0, 0, 0, 100)
        shadow_width = 140 * self.capibara.scale
        shadow_height = 40 * self.capibara.scale
        shadow_surf = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, shadow_color, (0, 0, shadow_width, shadow_height))

        rotation_angle = np.sin(time_factor * 1.0) * 0.2
        rotated_shadow = pygame.transform.rotate(shadow_surf, np.degrees(rotation_angle))
        scale_x = 1 - abs(rotation_angle) * 0.4
        scaled_width = int(rotated_shadow.get_width() * scale_x)
        scaled_shadow = pygame.transform.scale(rotated_shadow, (scaled_width, rotated_shadow.get_height()))

        shadow_x = pos[0] - scaled_shadow.get_width() // 2 + 10
        shadow_y = self.capibara.get_ground_y(pos[0]) - scaled_shadow.get_height() // 2 + 60
        self.screen.blit(scaled_shadow, (shadow_x, shadow_y))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            self.time_elapsed += dt
            self.frame_count += 1

            if self.frame_count % 50 == 0:
                self.spawn_confetti(3)

            if self.lyrics_manager.update(self.time_elapsed):
                running = False
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.physics.update(dt)
            self.update_confetti(dt)

            self.screen.fill(self.colors['sky'])

            self.draw_grass(self.time_elapsed)
            self.draw_shadow(self.physics.position, self.time_elapsed)
            self.capibara.draw(self.screen, self.physics.position, self.time_elapsed, self.physics.is_on_ground())

            for particle in self.confetti_particles:
                pygame.draw.circle(self.screen, particle['color'], (int(particle['x']), int(particle['y'])), particle['size'])

            self.lyrics_manager.render(self.screen, self.width, self.height)

            pygame.display.flip()

        self.audio_manager.stop_audio()
        pygame.quit()
        sys.exit()