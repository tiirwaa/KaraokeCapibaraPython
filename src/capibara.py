import pygame
import numpy as np
import sys
import random
import winsound
import os
import glob
from svgpathtools import svg2paths

# Deshabilitar audio en SDL para que winsound funcione
os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['SDL_INIT_AUDIO'] = '0'

# Inicializar solo los subsistemas necesarios de Pygame
pygame.display.init()
pygame.font.init()

# Configuración de la ventana
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Capibara Bailando")
clock = pygame.time.Clock()

# Load Manim frames
frames_path = '../media/images/animar_svg_manim/'
frames = [pygame.image.load(os.path.join(frames_path, f)) for f in sorted(os.listdir(frames_path)) if f.endswith('.png')]
num_frames = len(frames)
print(f"Loaded {num_frames} frames")

# Load SVG paths for capybara
paths, attributes = svg2paths('../res/svg/salida_bezier.svg')

# Precompute points for each path for faster drawing
path_points = []
for path in paths:
    total_length = path.length()
    num_points = 500  # More points for smoothness
    points = [path.point(t / num_points) for t in range(num_points + 1)]
    path_points.append(points)

# Get bounding box for centering
if paths:
    min_x = min(p.bbox()[0] for p in paths)
    max_x = max(p.bbox()[1] for p in paths)
    min_y = min(p.bbox()[2] for p in paths)
    max_y = max(p.bbox()[3] for p in paths)
    svg_center_x = (min_x + max_x) / 2
    svg_center_y = (min_y + max_y) / 2
else:
    svg_center_x = 0
    svg_center_y = 0

# Animation steps matching Manim
PI = np.pi
steps = [
    (0.5, 'rotate', PI/6),
    (0.5, 'rotate', -PI/3),
    (0.5, 'rotate', PI/6),
    (0.3, 'shift', (0, 0.5)),  # UP
    (0.3, 'shift', (0, -1.0)),  # DOWN
    (0.3, 'shift', (0, 0.5)),  # UP
    (0.4, 'rotate', PI/4),
    (0.4, 'rotate', -PI/2),
    (0.4, 'rotate', PI/4),
    (1.0, 'reset', None),
]
cycle_time = sum(dur for dur, _, _ in steps)

def play_audio():
    print("Iniciando reproducción de audio")
    winsound.PlaySound('../res/wav/capibara.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

def stop_audio():
    print("Deteniendo audio")
    winsound.PlaySound(None, winsound.SND_PURGE)

# Iniciar audio automáticamente
play_audio()
print("Audio iniciado automáticamente")

# Cargar letras de la canción
lyrics = []
with open('../res/txt/letra.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            lyrics.append(line) 

# Procesar eventos: lyrics o instrumentales
events = []
for line in lyrics:
    if line.startswith('[') and line.endswith('s]'):
        try:
            duration = float(line[1:-2])
            events.append(('instrumental', duration))
        except ValueError:
            pass
    else:
        events.append(('lyric', line))

# Variables para letras
current_word_index = 0
last_word_change = 0
word_time = 0.3  # segundos por palabra
current_y = 300
current_word_data = []
is_instrumental = False
current_event_index = 0
last_event_change = 0

# Inicializar el primer evento
if events:
    event_type, *content = events[0]
    if event_type == 'instrumental':
        is_instrumental = True
    else:
        is_instrumental = False
        current_line = content[0]
        words = current_line.split()
        current_word_data = []
        if words:
            # Calcular anchos para centrar la línea
            font_normal = pygame.font.Font(None, 40)
            widths = []
            for word in words:
                if word.strip():
                    temp_surf = font_normal.render(word, True, (255,255,255))
                    widths.append(temp_surf.get_width())
            total_width = sum(widths) + (len(widths) - 1) * 20
            start_x = 50  # Start more to the left
            current_x = start_x
            y = current_y
            for word, width in zip(words, widths):
                if not word.strip():
                    continue
                color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                angle = 0
                # normal
                surf_normal = font_normal.render(word, True, color)
                surf_normal_rot = pygame.transform.rotate(surf_normal, angle)
                # big
                font_big = pygame.font.Font(None, 80)
                surf_big = font_big.render(word, True, color)
                surf_big_rot = pygame.transform.rotate(surf_big, angle)
                current_word_data.append((surf_normal_rot, surf_big_rot, current_x, y))
                current_x += width + 20
        current_word_index = 0
        last_word_change = 0

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GREEN = (0, 128, 0)
PINK = (255, 192, 203)
DARK_BROWN = (101, 67, 33)
LIGHT_BROWN = (160, 82, 45)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Confetti particles
confetti_particles = []

# Física básica
gravity = np.array([0.0, 0.0])  # Disable gravity for centering
velocity = np.array([0.0, 0.0])
position = np.array([WIDTH // 2, HEIGHT // 2], dtype=float)  # Center position in new window

# Escala global (usa la misma en dibujo y física)
# Reducida para que el capibara entre mejor en la ventana
SCALE = 2

def get_ground_y(x):
    return HEIGHT - 150 + (x / WIDTH) * 50

def draw_capibara(pos, time_factor, on_ground):
    # Calculate frame index based on time
    t = time_factor % cycle_time
    frame_index = int((t / cycle_time) * num_frames) % num_frames
    frame = frames[frame_index]
    # Scale down to match Pygame scale (Manim scale=3, Pygame effective scale=1)
    scale_factor = 1 / 3  # Since Manim is 3x larger
    new_width = int(frame.get_width() * scale_factor)
    new_height = int(frame.get_height() * scale_factor)
    scaled_frame = pygame.transform.scale(frame, (new_width, new_height))
    # Center at pos, lower and slightly left
    rect = scaled_frame.get_rect(center=(int(pos[0]) - 20, int(pos[1]) + 160))
    screen.blit(scaled_frame, rect)

def draw_grass(time_factor):
    grass_height = 20 * SCALE
    grass_color = GREEN
    # Dibujar tierra debajo con inclinación para dar profundidad
    dirt_points = [(0, HEIGHT - 150), (WIDTH, HEIGHT - 100), (WIDTH, HEIGHT), (0, HEIGHT)]
    pygame.draw.polygon(screen, DARK_BROWN, dirt_points)
    # Dibujar césped encima con base inclinada
    for x in range(0, WIDTH, int(10 * SCALE)):
        base_y = HEIGHT - 150 + (x / WIDTH) * 50  # Inclinación de 150 a 100
        ground_height = HEIGHT - base_y
        for dy in range(0, int(ground_height), int(10 * SCALE)):
            y = base_y + dy
            sway = np.sin(time_factor * 2.0 + x * 0.05 + dy * 0.1) * 3 * SCALE
            pygame.draw.line(screen, grass_color, (x, y), (x + sway, y - grass_height), int(2 * SCALE))

def draw_shadow(pos, scale, time_factor):
    shadow_color = (0, 0, 0, 100)  # semi-transparent black
    shadow_width = 140 * scale
    shadow_height = 40 * scale
    shadow_surf = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surf, shadow_color, (0, 0, shadow_width, shadow_height))

    # Apply same deformation as capibara for realism
    rotation_angle = np.sin(time_factor * 1.0) * 0.2
    rotated_shadow = pygame.transform.rotate(shadow_surf, np.degrees(rotation_angle))
    scale_x = 1 - abs(rotation_angle) * 0.4
    scaled_width = int(rotated_shadow.get_width() * scale_x)
    scaled_shadow = pygame.transform.scale(rotated_shadow, (scaled_width, rotated_shadow.get_height()))

    shadow_x = pos[0] - scaled_shadow.get_width() // 2 + 10
    shadow_y = get_ground_y(pos[0]) - scaled_shadow.get_height() // 2 + 60
    screen.blit(scaled_shadow, (shadow_x, shadow_y))

def spawn_confetti(num=5):
    party_colors = [RED, YELLOW, GREEN, BLUE, PINK, (255, 0, 255), (0, 255, 255)]
    for _ in range(num):
        x = random.randint(0, WIDTH)
        y = -10
        vx = random.uniform(-1, 1)
        vy = random.uniform(1, 3)
        color = random.choice(party_colors)
        size = random.randint(3, 8)
        confetti_particles.append({'x': x, 'y': y, 'vx': vx, 'vy': vy, 'color': color, 'size': size})

# Bucle principal
running = True
time_elapsed = 0
frame_count = 0
while running:
    dt = clock.tick(60) / 1000.0
    time_elapsed += dt
    frame_count += 1

    # Spawn confetti periodically
    if frame_count % 50 == 0:
        spawn_confetti(3)

    current_event = events[current_event_index]

    # Check for end
    if current_event[0] == 'lyric' and current_event[1] == '[END]':
        stop_audio()
        running = False
        continue

    # Cambiar palabra actual
    if current_event[0] == 'instrumental':
        duration = current_event[1]
    else:
        line = current_event[1]
        words = line.split()
        duration = word_time * len(words) + 1  # un poco de margen al final
    if time_elapsed - last_event_change >= duration:
        print(f"At time {time_elapsed:.2f}, switching from event {current_event_index}: {current_event}, duration {duration}")
        current_event_index = (current_event_index + 1) % len(events)
        last_event_change = time_elapsed
        event_type, *content = events[current_event_index]
        print(f"To event {current_event_index}: {event_type}")
        if event_type == 'instrumental':
            is_instrumental = True
            print("Setting to instrumental")
        else:
            is_instrumental = False
            print("Setting to lyric")
            current_line = content[0]
            if current_line == '[END]':
                stop_audio()
                running = False
                continue
            words = current_line.split()
            current_word_data = []
            if words:
                # Calcular anchos para centrar la línea
                font_normal = pygame.font.Font(None, 40)
                widths = []
                for word in words:
                    if word.strip():
                        temp_surf = font_normal.render(word, True, (255,255,255))
                        widths.append(temp_surf.get_width())
                total_width = sum(widths) + (len(widths) - 1) * 20
                start_x = 50  # Start more to the left
                current_x = start_x
                y = current_y
                for word, width in zip(words, widths):
                    if not word.strip():
                        continue
                    color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                    angle = 0
                    # normal
                    surf_normal = font_normal.render(word, True, color)
                    surf_normal_rot = pygame.transform.rotate(surf_normal, angle)
                    # big
                    font_big = pygame.font.Font(None, 80)
                    surf_big = font_big.render(word, True, color)
                    surf_big_rot = pygame.transform.rotate(surf_big, angle)
                    current_word_data.append((surf_normal_rot, surf_big_rot, current_x, y))
                    current_x += width + 20
            current_word_index = 0
            last_word_change = time_elapsed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Física (disabled for centering)
    # velocity += gravity * dt
    # position += velocity * dt

    # Update confetti
    for particle in confetti_particles[:]:
        particle['vy'] += gravity[1] * dt
        particle['x'] += particle['vx'] * dt
        particle['y'] += particle['vy'] * dt
        if particle['y'] > HEIGHT + 10:
            confetti_particles.remove(particle)

    # Límites (disabled for centering)
    # body_h = 220 * SCALE
    # body_w = 140 * SCALE
    # floor_height = 140
    # max_center_y = HEIGHT - floor_height - (body_h / 2) + 30
    # if position[1] >= max_center_y:
    #     position[1] = max_center_y
    #     velocity[1] *= -0.8
    # side_margin = int(body_w / 2 + 20)
    # if position[0] <= side_margin or position[0] >= WIDTH - side_margin:
    #     velocity[0] *= -1

    # Avanzar palabra actual en letras
    if not is_instrumental and current_word_data:
        if time_elapsed - last_word_change >= word_time:
            current_word_index += 1
            last_word_change = time_elapsed
            if current_word_index >= len(current_word_data):
                current_word_index = len(current_word_data) - 1  # Mantener la última palabra resaltada

    # Limpiar pantalla
    screen.fill((135, 206, 235))  # Azul cielo

    # Dibujar suelo (ajustado) - ahora con césped animado
    draw_grass(time_elapsed)

    # Dibujar sombra
    draw_shadow(position, SCALE, time_elapsed)

    # Dibujar capibara
    on_ground = True  # Static, no physics
    draw_capibara(position, time_elapsed, on_ground)

    # Draw confetti
    for particle in confetti_particles:
        pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), particle['size'])

    # Dibujar letras o instrumental
    if is_instrumental:
        font = pygame.font.Font(None, 100)
        text_surf = font.render("Instrumental", True, YELLOW)
        screen.blit(text_surf, (WIDTH//2 - text_surf.get_width()//2, 100))
    else:
        # Dibujar letras con efecto karaoke por palabras
        for i, (surf_normal, surf_big, x, y) in enumerate(current_word_data):
            if i == current_word_index:
                w, h = surf_big.get_size()
                factor = 2
                new_w = int(w * factor)
                new_h = int(h * factor)
                scaled_surf = pygame.transform.scale(surf_big, (new_w, new_h))
                screen.blit(scaled_surf, (x, y - 150))  # Position big letters 50px above
            else:
                screen.blit(surf_normal, (x, y))

    # Actualizar pantalla
    pygame.display.flip()

stop_audio()
pygame.quit()
sys.exit()