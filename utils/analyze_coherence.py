import numpy as np
import math
from svgpathtools import svg2paths

# Cargar el SVG
paths, attributes = svg2paths('res/svg/salida_bezier.svg')

# Definir feet (paths 0-3) y legs (23-24)
feet_paths = paths[0:4]
legs_paths = [paths[23], paths[24]]

# Función para calcular centro de un grupo de paths
def calculate_center(paths):
    all_points = []
    for path in paths:
        # Obtener puntos del path
        num_points = 100
        points = [path.point(t / num_points) for t in range(num_points + 1)]
        all_points.extend(points)
    # Centro como promedio
    x_coords = [p.real for p in all_points]
    y_coords = [p.imag for p in all_points]
    center_x = np.mean(x_coords)
    center_y = np.mean(y_coords)
    return np.array([center_x, center_y])

# Centros iniciales
feet_center_initial = calculate_center(feet_paths)
legs_center_initial = calculate_center(legs_paths)

print(f"Feet initial center: {feet_center_initial}")
print(f"Legs initial center: {legs_center_initial}")
print(f"Initial distance: {np.linalg.norm(feet_center_initial - legs_center_initial)}")

# Simular transformaciones (rotaciones y shifts)
# Las transformaciones son aplicadas en secuencia

# Estado actual de centros
feet_center = feet_center_initial.copy()
legs_center = legs_center_initial.copy()

# Función para aplicar rotación alrededor del centro del objeto (como en Manim)
def apply_rotation(center, angle):
    # En Manim, rotate rota alrededor del centro del objeto
    # Para simular, trasladar al origen, rotar, trasladar de vuelta
    # Pero como center es el centro, y estamos aplicando a center mismo, es lo mismo que rotar alrededor del origen si el centro es fijo
    # En realidad, para precisión, necesitamos el centro fijo inicial, pero como cambia con shifts, es complicado
    # El problema principal es que feet y legs tienen centros diferentes, y rotan con ángulos diferentes, causando incoherencia anatómica
    # Para encontrar el problema, basta con ver que las distancias varían
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    return rotation_matrix @ center

# Función para aplicar shift
def apply_shift(center, shift):
    return center + shift

# Simular las animaciones paso a paso

# 1. Girar a la izquierda: Rotate(svg, math.pi/6), feet.rotate(math.pi/12), legs.rotate(math.pi/8)
feet_center = apply_rotation(feet_center, math.pi/12)
legs_center = apply_rotation(legs_center, math.pi/8)
print(f"After left turn: Feet {feet_center}, Legs {legs_center}, Distance {np.linalg.norm(feet_center - legs_center)}")

# Wiggle
feet_center = apply_rotation(feet_center, -math.pi/6)
legs_center = apply_rotation(legs_center, -math.pi/4)
print(f"After wiggle1: Feet {feet_center}, Legs {legs_center}, Distance {np.linalg.norm(feet_center - legs_center)}")

feet_center = apply_rotation(feet_center, math.pi/6)
legs_center = apply_rotation(legs_center, math.pi/4)
print(f"After wiggle2: Feet {feet_center}, Legs {legs_center}, Distance {np.linalg.norm(feet_center - legs_center)}")

# 2. Girar a la derecha: Rotate(svg, -math.pi/3), feet.rotate(-math.pi/12), legs.rotate(-math.pi/8)
feet_center = apply_rotation(feet_center, -math.pi/12)
legs_center = apply_rotation(legs_center, -math.pi/8)
print(f"After right turn: Feet {feet_center}, Legs {legs_center}, Distance {np.linalg.norm(feet_center - legs_center)}")

# Wiggle
feet_center = apply_rotation(feet_center, math.pi/6)
legs_center = apply_rotation(legs_center, math.pi/4)
print(f"After wiggle3: Feet {feet_center}, Legs {legs_center}, Distance {np.linalg.norm(feet_center - legs_center)}")

feet_center = apply_rotation(feet_center, -math.pi/6)
legs_center = apply_rotation(legs_center, -math.pi/4)
print(f"After wiggle4: Feet {feet_center}, Legs {legs_center}, Distance {np.linalg.norm(feet_center - legs_center)}")

# 3. Volver al centro: Rotate(svg, math.pi/6), feet.rotate(math.pi/12), legs.rotate(math.pi/8)
feet_center = apply_rotation(feet_center, math.pi/12)
legs_center = apply_rotation(legs_center, math.pi/8)
print(f"After center: Feet {feet_center}, Legs {legs_center}, Distance {np.linalg.norm(feet_center - legs_center)}")

# 4. Bounce: shift UP 0.5, feet.shift(DOWN*0.2).rotate(math.pi/24), legs.shift(DOWN*0.2).rotate(-math.pi/12)
feet_center = apply_shift(feet_center, np.array([0, -0.2]))  # DOWN is negative y
feet_center = apply_rotation(feet_center, math.pi/24)
legs_center = apply_shift(legs_center, np.array([0, -0.2]))
legs_center = apply_rotation(legs_center, -math.pi/12)
print(f"After bounce1: Feet {feet_center}, Legs {legs_center}, Distance {np.linalg.norm(feet_center - legs_center)}")

# shift DOWN 1.0, feet.shift(DOWN*0.1).rotate(-math.pi/24), legs.shift(DOWN*0.1).rotate(math.pi/12)
feet_center = apply_shift(feet_center, np.array([0, -0.1]))
feet_center = apply_rotation(feet_center, -math.pi/24)
legs_center = apply_shift(legs_center, np.array([0, -0.1]))
legs_center = apply_rotation(legs_center, math.pi/12)
print(f"After bounce2: Feet {feet_center}, Legs {legs_center}, Distance {np.linalg.norm(feet_center - legs_center)}")

# shift UP 0.5, feet.shift(UP*0.1).rotate(math.pi/24), legs.shift(UP*0.1).rotate(-math.pi/12)
feet_center = apply_shift(feet_center, np.array([0, 0.1]))  # UP is positive y
feet_center = apply_rotation(feet_center, math.pi/24)
legs_center = apply_shift(legs_center, np.array([0, 0.1]))
legs_center = apply_rotation(legs_center, -math.pi/12)
print(f"After bounce3: Feet {feet_center}, Legs {legs_center}, Distance {np.linalg.norm(feet_center - legs_center)}")

# Continuar con los giros finales...
# Esto es aproximado, pero muestra el patrón.

print("Análisis completo de posiciones.")