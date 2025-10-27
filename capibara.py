import pygame
import numpy as np
import sys
import random
import winsound
import os

# Deshabilitar audio en SDL para que winsound funcione
os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['SDL_INIT_AUDIO'] = '0'

# Inicializar solo los subsistemas necesarios de Pygame
pygame.display.init()
pygame.font.init()

# Configuración de la ventana (reduzco tamaño para que no sea demasiado grande)
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Capibara Bailando")
clock = pygame.time.Clock()

def play_audio():
    print("Iniciando reproducción de audio")
    winsound.PlaySound('capibara.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

def stop_audio():
    print("Deteniendo audio")
    winsound.PlaySound(None, winsound.SND_PURGE)

# Iniciar audio automáticamente
play_audio()
print("Audio iniciado automáticamente")

# Cargar letras de la canción
lyrics = []
with open('letra.txt', 'r', encoding='utf-8') as f:
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

# Física básica
gravity = np.array([0.0, 0.5])
velocity = np.array([0.0, 0.0])
position = np.array([WIDTH // 2, HEIGHT // 2], dtype=float)

# Escala global (usa la misma en dibujo y física)
# Reducida para que el capibara entre mejor en la ventana
SCALE = 2

# Función para dibujar el capibara con todos los detalles (escalado x3 para tamaño mayor)
def draw_capibara(pos, time_factor, on_ground):
    # Nueva versión: diseño limpio y estilizado inspirado en la imagen de referencia
    scale = SCALE
    bob = np.sin(time_factor * 2.0) * 4.0 * scale  # pequeño balanceo

    rotation_angle = np.sin(time_factor * 1.0) * 0.5  # Aumentar el ángulo para más movimiento lateral
    surf_width = 700
    surf_height = 700
    capibara_surf = pygame.Surface((surf_width, surf_height), pygame.SRCALPHA)
    center_x = surf_width // 2
    center_y = surf_height // 2

    # Paleta simplificada (usar colores ya definidos arriba)
    body_color = (139, 69, 19)  # más rojizo para parecer más natural
    outline_color = DARK_BROWN
    belly_color = (241, 196, 144)
    nose_color = (200, 150, 140)

    # Coordenadas base
    x, y = center_x, center_y

    # Cuerpo dividido en secciones: torso superior e inferior para más detalle
    body_w = 100 * scale  # Reducir ancho para elipses menos anchas
    body_h = 250 * scale  # Aumentar altura para mejor relación de aspecto (más alargado)
    # Torso superior (pecho)
    upper_body_h = 120 * scale  # Reducir para mejor proporción
    upper_body_rect = pygame.Rect(int(x - body_w/2), int(y - body_h/2 + bob + 30 * scale), int(body_w), int(upper_body_h))  # Bajar más
    upper_outline_rect = upper_body_rect.inflate(12 * scale, 12 * scale)
    pygame.draw.ellipse(capibara_surf, outline_color, upper_outline_rect)
    pygame.draw.ellipse(capibara_surf, body_color, upper_body_rect)

    # Torso inferior (abdomen/caderas, ligeramente más ancho)
    lower_body_h = 130 * scale  # Aumentar para cubrir más
    lower_body_w = body_w + 10 * scale  # menos ancho para mejor proporción
    lower_body_rect = pygame.Rect(int(x - lower_body_w/2), int(y - body_h/2 + bob + upper_body_h - 50 * scale), int(lower_body_w), int(lower_body_h))  # Subir más
    lower_outline_rect = lower_body_rect.inflate(12 * scale, 12 * scale)
    pygame.draw.ellipse(capibara_surf, outline_color, lower_outline_rect)
    pygame.draw.ellipse(capibara_surf, body_color, lower_body_rect)

    # Barriga más clara en la parte inferior
    belly_rect = lower_body_rect.inflate(-40 * scale, -50 * scale)
    pygame.draw.ellipse(capibara_surf, belly_color, belly_rect)

    # Cabeza (más pequeña y redondeada, superpuesta)
    head_w = 70 * scale
    head_h = 60 * scale
    head_x = x
    head_y = y - body_h/2 + 40 * scale + bob
    head_rect = pygame.Rect(int(head_x - head_w/2), int(head_y - head_h/2), int(head_w), int(head_h))
    pygame.draw.ellipse(capibara_surf, outline_color, head_rect.inflate(10 * scale, 10 * scale))
    pygame.draw.ellipse(capibara_surf, body_color, head_rect)

    # Orejas simples
    ear_w, ear_h = 26 * scale, 36 * scale
    left_ear = pygame.Rect(int(head_x - 30 * scale - ear_w/2), int(head_y - 40 * scale), int(ear_w), int(ear_h))
    right_ear = pygame.Rect(int(head_x + 30 * scale - ear_w/2), int(head_y - 40 * scale), int(ear_w), int(ear_h))
    pygame.draw.ellipse(capibara_surf, outline_color, left_ear.inflate(6 * scale, 6 * scale))
    pygame.draw.ellipse(capibara_surf, body_color, left_ear)
    pygame.draw.ellipse(capibara_surf, outline_color, right_ear.inflate(6 * scale, 6 * scale))
    pygame.draw.ellipse(capibara_surf, body_color, right_ear)

    # Ojos pequeños y simpáticos
    eye_y = head_y - 5 * scale
    eye_x_offset = 18 * scale
    pygame.draw.circle(capibara_surf, BLACK, (int(head_x - eye_x_offset), int(eye_y)), int(4 * scale))  # Reducir radio
    pygame.draw.circle(capibara_surf, BLACK, (int(head_x + eye_x_offset), int(eye_y)), int(4 * scale))  # Reducir radio

    # Nariz y hocico sencillo
    nose_w, nose_h = 26 * scale, 18 * scale
    nose_rect = pygame.Rect(int(head_x - nose_w/2), int(head_y + 2 * scale), int(nose_w), int(nose_h))
    pygame.draw.ellipse(capibara_surf, outline_color, nose_rect.inflate(4 * scale, 4 * scale))
    pygame.draw.ellipse(capibara_surf, nose_color, nose_rect)

    # Boca (línea simple)
    mouth_start = (int(head_x - 10 * scale), int(head_y + 18 * scale))
    mouth_end = (int(head_x + 10 * scale), int(head_y + 18 * scale))
    pygame.draw.arc(capibara_surf, outline_color, (mouth_start[0], mouth_start[1] - 6 * scale, 20 * scale, 12 * scale), 3.14, 0, int(3 * scale))

    # Bigotes (pocos puntitos alrededor del hocico)
    for dx in (-20 * scale, -10 * scale, 10 * scale, 20 * scale):
        pygame.draw.circle(capibara_surf, outline_color, (int(head_x + dx), int(head_y + 6 * scale)), int(1 * scale))  # Reducir radio

    # Patas delanteras (reposicionadas y con pequeña inclinación hacia dentro)
    paw_w, paw_h = 36 * scale, 24 * scale
    # Ajuste fino: bajar un poco los brazos respecto al pecho y separarlos más
    # Bajar las manos un poco más (ajuste solicitado)
    front_y = head_y + 26 * scale
    # Aumentar separación horizontal entre manos
    front_x_offset = 45 * scale  # Acercar más al cuerpo
    # Brazos articulados (hombro -> codo -> mano)
    upper_len = 28 * scale
    lower_len = 26 * scale
    arm_thickness = int(12 * scale)

    # función auxiliar para dibujar un brazo dado el hombro y un desfase de fase
    def draw_arm(shoulder_x, shoulder_y, phase_offset):
        # calcular ángulos animados
        angle = np.sin(time_factor * 3.0 + phase_offset) * 0.5  # en radianes
        # vector hacia abajo con ángulo
        elbow_dx = int(np.sin(angle) * upper_len)
        elbow_dy = int(np.cos(angle) * upper_len)
        elbow = np.array([shoulder_x + elbow_dx, shoulder_y + elbow_dy])

        # ángulo para el antebrazo, algo más cerrado
        angle2 = angle + 0.4 * np.sin(time_factor * 4.0 + phase_offset)
        hand_dx = int(np.sin(angle2) * lower_len)
        hand_dy = int(np.cos(angle2) * lower_len)
        hand = np.array([elbow[0] + hand_dx, elbow[1] + hand_dy])

        # dibujar segmentos gruesos como líneas con grosor, y círculos en articulaciones
        pygame.draw.line(capibara_surf, outline_color, (shoulder_x, shoulder_y), tuple(elbow.astype(int)), arm_thickness)
        pygame.draw.line(capibara_surf, outline_color, tuple(elbow.astype(int)), tuple(hand.astype(int)), arm_thickness)
        # rellenar interior del brazo (ligero offset) para simular el color del cuerpo
        # dibujar "relleno" central usando líneas más delgadas en body_color
        pygame.draw.line(capibara_surf, body_color, (shoulder_x, shoulder_y), tuple(elbow.astype(int)), max(1, arm_thickness - 2))
        pygame.draw.line(capibara_surf, body_color, tuple(elbow.astype(int)), tuple(hand.astype(int)), max(1, arm_thickness - 2))

        # articulaciones
        pygame.draw.circle(capibara_surf, body_color, tuple(elbow.astype(int)), int(arm_thickness / 2))  # Revertir a original
        # mano (pequeña elipse)
        hand_rect = pygame.Rect(0, 0, int(paw_w), int(paw_h))
        hand_rect.center = (int(hand[0]), int(hand[1]))
        pygame.draw.ellipse(capibara_surf, outline_color, hand_rect.inflate(int(4 * scale), int(4 * scale)))
        pygame.draw.ellipse(capibara_surf, body_color, hand_rect)

    # hombros (ligeramente altos, cerca del pecho)
    shoulder_y = int(head_y + 20 * scale)  # Bajar un poco más
    left_shoulder_x = int(x - front_x_offset + 6 * scale)
    right_shoulder_x = int(x + front_x_offset - 6 * scale)

    draw_arm(left_shoulder_x, shoulder_y, phase_offset=0.0)
    draw_arm(right_shoulder_x, shoulder_y, phase_offset=1.5)

    # Piernas traseras articuladas (cadera -> rodilla -> pie)
    hip_x_offset = 20 * scale  # Acercar al cuerpo
    hip_y = int(y + 70 * scale + bob)  # Acercar verticalmente al cuerpo
    upper_leg = 36 * scale
    lower_leg = 38 * scale
    leg_thickness = int(14 * scale)
    ground_y = HEIGHT - 60

    def draw_leg(hip_x, hip_y, phase, on_ground, ground_y, time_factor):
        if on_ground:
            # Target for walking: oscillate x, y at ground
            target_x = np.sin(time_factor * 2.5 + phase) * 30 * scale
            target_y = ground_y - hip_y
            L1 = upper_leg
            L2 = lower_leg
            d = np.sqrt(target_x**2 + target_y**2)
            if d <= L1 + L2 and d >= abs(L1 - L2):
                cos_a2 = (target_x**2 + target_y**2 - L1**2 - L2**2) / (2 * L1 * L2)
                a2 = np.arccos(np.clip(cos_a2, -1, 1))
                a1 = np.arctan2(target_y, target_x) - np.arctan2(L2 * np.sin(a2), L1 + L2 * np.cos(a2))
                angle1 = a1
                angle2 = a1 + a2
            else:
                # Fallback to animation
                angle1 = -0.2 + np.sin(time_factor * 2.5 + phase) * 0.3
                angle2 = angle1 + 0.9 - 0.3 * np.cos(time_factor * 3.0 + phase)
        else:
            angle1 = -0.2 + np.sin(time_factor * 2.5 + phase) * 0.3
            angle2 = angle1 + 0.9 - 0.3 * np.cos(time_factor * 3.0 + phase)

        knee_dx = int(np.sin(angle1) * upper_leg)
        knee_dy = int(np.cos(angle1) * upper_leg)
        knee = np.array([hip_x + knee_dx, hip_y + knee_dy])

        foot_dx = int(np.sin(angle2) * lower_leg)
        foot_dy = int(np.cos(angle2) * lower_leg)
        foot = np.array([knee[0] + foot_dx, knee[1] + foot_dy])

        # dibujar segmentos (contorno) y relleno interior
        pygame.draw.line(capibara_surf, outline_color, (hip_x, hip_y), tuple(knee.astype(int)), leg_thickness)
        pygame.draw.line(capibara_surf, outline_color, tuple(knee.astype(int)), tuple(foot.astype(int)), leg_thickness)
        pygame.draw.line(capibara_surf, body_color, (hip_x, hip_y), tuple(knee.astype(int)), max(1, leg_thickness - 2))
        pygame.draw.line(capibara_surf, body_color, tuple(knee.astype(int)), tuple(foot.astype(int)), max(1, leg_thickness - 2))

        # articulaciones
        pygame.draw.circle(capibara_surf, body_color, (int(hip_x), int(hip_y)), int(leg_thickness / 2))  # Revertir a original
        pygame.draw.circle(capibara_surf, body_color, tuple(knee.astype(int)), int(leg_thickness / 2))  # Revertir a original

        # pie como pequeña elipse
        foot_rect = pygame.Rect(0, 0, int(34 * scale), int(18 * scale))
        foot_rect.center = (int(foot[0]), int(foot[1]))
        pygame.draw.ellipse(capibara_surf, outline_color, foot_rect.inflate(int(4 * scale), int(4 * scale)))
        pygame.draw.ellipse(capibara_surf, body_color, foot_rect)

    # dibujar pierna izquierda y derecha (mirrored)
    left_hip_x = int(x - hip_x_offset)
    right_hip_x = int(x + hip_x_offset)
    draw_leg(left_hip_x, hip_y, phase=0.0, on_ground=on_ground, ground_y=ground_y, time_factor=time_factor)
    draw_leg(right_hip_x, hip_y, phase=1.6, on_ground=on_ground, ground_y=ground_y, time_factor=time_factor)

    # Boceto final: ojos con brillo
    pygame.draw.circle(capibara_surf, WHITE, (int(head_x - eye_x_offset + 3 * scale), int(eye_y - 2 * scale)), int(1 * scale))  # Reducir radio
    pygame.draw.circle(capibara_surf, WHITE, (int(head_x + eye_x_offset + 3 * scale), int(eye_y - 2 * scale)), int(1 * scale))  # Reducir radio

    rotated_surf = pygame.transform.rotate(capibara_surf, np.degrees(rotation_angle))
    # Simular perspectiva 3D: reducir el ancho cuando gira para dar ilusión de profundidad
    scale_x = 1 - abs(rotation_angle) * 0.4
    scaled_width = int(rotated_surf.get_width() * scale_x)
    scaled_surf = pygame.transform.scale(rotated_surf, (scaled_width, rotated_surf.get_height()))
    screen.blit(scaled_surf, (pos[0] - scaled_surf.get_width()//2, pos[1] - rotated_surf.get_height()//2))

def draw_grass(time_factor):
    grass_height = 20 * SCALE
    grass_color = GREEN
    dirt_height = 40
    # Dibujar tierra debajo
    pygame.draw.rect(screen, DARK_BROWN, (0, HEIGHT - dirt_height, WIDTH, dirt_height))
    # Dibujar césped encima
    for x in range(0, WIDTH, int(10 * SCALE)):
        sway = np.sin(time_factor * 2.0 + x * 0.05) * 3 * SCALE
        pygame.draw.line(screen, grass_color, (x, HEIGHT - dirt_height), (x + sway, HEIGHT - dirt_height - grass_height), int(2 * SCALE))

# Bucle principal
running = True
time_elapsed = 0
while running:
    dt = clock.tick(60) / 1000.0
    time_elapsed += dt

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
            elif event.key == pygame.K_s:
                stop_audio()

    # Física
    velocity += gravity * dt
    position += velocity * dt

    # Ajustar límites en función de la escala y el tamaño del cuerpo
    body_h = 220 * SCALE
    body_w = 140 * SCALE
    floor_height = 60
    # altura máxima del centro del cuerpo para que la base del cuerpo quede sobre el suelo
    max_center_y = HEIGHT - floor_height - (body_h / 2) - 50  # Subir un poco más el capibara
    if position[1] >= max_center_y:
        position[1] = max_center_y
        velocity[1] *= -0.8

    # límites laterales según el ancho del cuerpo
    side_margin = int(body_w / 2 + 20)
    if position[0] <= side_margin or position[0] >= WIDTH - side_margin:
        velocity[0] *= -1

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

    # Dibujar capibara
    on_ground = position[1] >= max_center_y
    draw_capibara(position, time_elapsed, on_ground)

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