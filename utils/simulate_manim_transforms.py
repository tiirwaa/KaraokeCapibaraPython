import numpy as np
import math
from svgpathtools import svg2paths

# Config: indices según animar_svg_manim.py
FEET_IDX = list(range(0, 4))
LEGS_IDX = [23, 24]
SVG_PATH = 'res/svg/salida_bezier.svg'

# Cargar paths
paths, attributes = svg2paths(SVG_PATH)

# Helper: centro de un conjunto de paths (promedio de puntos)
def center_of_paths(indices, npoints=200):
    pts = []
    for i in indices:
        path = paths[i]
        for t in np.linspace(0, 1, npoints):
            p = path.point(t)
            pts.append([p.real, p.imag])
    pts = np.array(pts)
    return pts.mean(axis=0)

# Centro del SVG (bounding box center)
def svg_center():
    min_x = min(p.bbox()[0] for p in paths)
    max_x = max(p.bbox()[1] for p in paths)
    min_y = min(p.bbox()[2] for p in paths)
    max_y = max(p.bbox()[3] for p in paths)
    return np.array([(min_x + max_x) / 2.0, (min_y + max_y) / 2.0])

# Rotar un punto alrededor de un centro
def rotate_around(point, center, angle):
    R = np.array([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]])
    return (R @ (point - center)) + center

# Aplicar shift (vector)
def shift(point, vec):
    return point + np.array(vec)

# Secuencia de transformaciones según animar_svg_manim.py (versión original y versión sincronizada)
# Defino la secuencia como lista de pasos; cada paso puede contener rotation del svg (angle_svg),
# rotation de feet y legs (angle_feet, angle_legs), y shifts aplicados a svg y a feet/legs.

original_sequence = [
    # left turn
    {'svg_rot': math.pi / 6.0, 'feet_rot': math.pi / 12.0, 'legs_rot': math.pi / 8.0, 'svg_shift': (0, 0), 'feet_shift': (0,0), 'legs_shift': (0,0), 'label':'left_turn'},
    # wiggles (series)
    {'svg_rot': 0, 'feet_rot': -math.pi/6.0, 'legs_rot': -math.pi/4.0, 'label':'wiggle1'},
    {'svg_rot': 0, 'feet_rot': math.pi/6.0, 'legs_rot': math.pi/4.0, 'label':'wiggle2'},
    # right turn
    {'svg_rot': -math.pi/3.0, 'feet_rot': -math.pi/12.0, 'legs_rot': -math.pi/8.0, 'label':'right_turn'},
    {'svg_rot': 0, 'feet_rot': math.pi/6.0, 'legs_rot': math.pi/4.0, 'label':'wiggle3'},
    {'svg_rot': 0, 'feet_rot': -math.pi/6.0, 'legs_rot': -math.pi/4.0, 'label':'wiggle4'},
    # center
    {'svg_rot': math.pi/6.0, 'feet_rot': math.pi/12.0, 'legs_rot': math.pi/8.0, 'label':'center'},
    # bounce sequence (shifts + small rotations)
    {'svg_rot': 0, 'svg_shift': (0, 0.5), 'feet_shift': (0, -0.2), 'legs_shift': (0, -0.2), 'feet_rot': math.pi/24.0, 'legs_rot': -math.pi/12.0, 'label':'bounce_up'},
    {'svg_rot': 0, 'svg_shift': (0, -1.0), 'feet_shift': (0, -0.1), 'legs_shift': (0, -0.1), 'feet_rot': -math.pi/24.0, 'legs_rot': math.pi/12.0, 'label':'bounce_down'},
    {'svg_rot': 0, 'svg_shift': (0, 0.5), 'feet_shift': (0, 0.1), 'legs_shift': (0, 0.1), 'feet_rot': math.pi/24.0, 'legs_rot': -math.pi/12.0, 'label':'bounce_up2'},
    # final turns (approx)
    {'svg_rot': math.pi/4.0, 'feet_rot': math.pi/8.0, 'legs_rot': math.pi/6.0, 'label':'final1'},
    {'svg_rot': -math.pi/2.0, 'feet_rot': -math.pi/8.0, 'legs_rot': -math.pi/6.0, 'label':'final2'},
    {'svg_rot': math.pi/4.0, 'feet_rot': math.pi/8.0, 'legs_rot': math.pi/6.0, 'label':'final3'},
]

# Helper que ejecuta la secuencia dada una configuración de rotaciones (usa una copia de centros)
def run_sequence(sequence, sync_feet_legs=False):
    # Centros iniciales
    feet_center = center_of_paths(FEET_IDX)
    legs_center = center_of_paths(LEGS_IDX)
    svg_c = svg_center()

    # Guardar historial
    history = []
    history.append(('initial', np.linalg.norm(feet_center - legs_center), feet_center.copy(), legs_center.copy()))

    for step in sequence:
        label = step.get('label','')
        # 1) rotar svg (si hay)
        angle_svg = step.get('svg_rot', 0.0)
        if angle_svg:
            # TODO: si svg tiene center distinto, rotar cada centro alrededor de svg_c
            feet_center = rotate_around(feet_center, svg_c, angle_svg)
            legs_center = rotate_around(legs_center, svg_c, angle_svg)
            # svg_c también rota alrededor sí mismo -> no cambia
        # 2) aplicar shifts del svg
        svg_shift = step.get('svg_shift', (0,0))
        if svg_shift != (0,0):
            feet_center = shift(feet_center, svg_shift)
            legs_center = shift(legs_center, svg_shift)
            svg_c = shift(svg_c, svg_shift)
        # 3) rotaciones/shifts locales en feet/legs (rotan alrededor de su propio centro después de svg transform)
        feet_shift = step.get('feet_shift', (0,0))
        legs_shift = step.get('legs_shift', (0,0))
        if feet_shift != (0,0):
            feet_center = shift(feet_center, feet_shift)
        if legs_shift != (0,0):
            legs_center = shift(legs_center, legs_shift)

        # rotaciones locales
        feet_angle = step.get('feet_rot', 0.0)
        legs_angle = step.get('legs_rot', 0.0)

        # Si sincronizamos, forzamos same angle (e.g., use legs_angle or average)
        if sync_feet_legs:
            # opcion: hacer iguales a legs_angle para que pierna guíe
            common = legs_angle if legs_angle != 0 else feet_angle
            feet_angle = common
            legs_angle = common

        # Rotar el centro alrededor de su propio centro no cambia la coordenada del centro.
        # IMPORTANTE: rotar un *grupo* alrededor de su centro NO CAMBIA la posición del centro.
        # Lo que sí cambia la posición relativa de sub-subpuntos, pero aquí trackeamos los centros del grupo.
        # Sin embargo, en Manim, si se rota un submobject individual que NO es un grupo, su center tampoco cambia, siempre que la rotación sea alrededor de su propio center.
        # El drift real aparece por mezclar rotaciones alrededor de distintos centros (svg center vs group center) y shifts locales.

        # Aun así, hay un efecto indirecto cuando se combinan: rotar svg mueve los centros; rotar feet luego alrededor de su centro NO mueve ese centro.
        # Pero si feet.animate.rotate se interpreta como rotar alrededor de un centro diferente (p.ej. ORIGIN) entonces sí movería centro. En Manim, rotate() rota alrededor del center por defecto.
        # Para simular la situación problemática asumimos que feet.rotate se aplica alrededor de un centro distinto (p.ej. del svg global) — probamos ambas hipótesis.

        # Hipótesis A: rotar alrededor de su propio center (Manim default): no cambia centers
        history.append((label + '_post_local_rot_owncenter', np.linalg.norm(feet_center - legs_center), feet_center.copy(), legs_center.copy()))

        # Hipótesis B: rotar feet/legs alrededor del centro del svg (mal uso) -> esto movería sus centers
        # Simulamos esto también para comparar
        feet_center_mis = rotate_around(feet_center, svg_c, feet_angle) if feet_angle else feet_center.copy()
        legs_center_mis = rotate_around(legs_center, svg_c, legs_angle) if legs_angle else legs_center.copy()
        history.append((label + '_post_local_rot_svgcenter', np.linalg.norm(feet_center_mis - legs_center_mis), feet_center_mis.copy(), legs_center_mis.copy()))

    return history

# Ejecutar: original
hist_orig = run_sequence(original_sequence, sync_feet_legs=False)
# Ejecutar: sincronizado (forzar mismos ángulos)
hist_sync = run_sequence(original_sequence, sync_feet_legs=True)

# Imprimir resumen
print('Paso, distancia (propia rot), feet_center, legs_center')
for rec in hist_orig:
    print(rec[0], f"{rec[1]:.3f}")

print('\n--- Comparación (mis-rot alrededor svg center) ---')
for rec in hist_orig:
    label = rec[0]
    # buscar en hist_orig la entrada with _post_local_rot_svgcenter
    # hay pares; ya los imprime en orden

for rec in hist_sync:
    pass

print('\nHistórico (original, hipótesis A y B en pares):')
for i in range(len(hist_orig)):
    rec = hist_orig[i]
    print(f"{i}: {rec[0]} distance={rec[1]:.3f}")

print('\nÚltimas entradas (sincronizado):')
for i, rec in enumerate(hist_sync[-6:]):
    print(f"{i}: {rec[0]} distance={rec[1]:.3f} feet={rec[2]} legs={rec[3]}")

# Además, calcular la variación máxima de distancia en cada modo

def max_variation(history):
    dists = [h[1] for h in history]
    return max(dists) - min(dists), min(dists), max(dists)

var_orig = max_variation([h for h in hist_orig if 'post_local_rot_owncenter' in h[0]])
var_mis = max_variation([h for h in hist_orig if 'post_local_rot_svgcenter' in h[0]])
var_sync = max_variation([h for h in hist_sync if 'post_local_rot_owncenter' in h[0]])

print(f"\nVariación original (rot around owncenter entries): delta={var_orig[0]:.3f} min={var_orig[1]:.3f} max={var_orig[2]:.3f}")
print(f"Variación si se rota alrededor de svg center (mal uso): delta={var_mis[0]:.3f} min={var_mis[1]:.3f} max={var_mis[2]:.3f}")
print(f"Variación sincronizada (forzada same angles): delta={var_sync[0]:.3f} min={var_sync[1]:.3f} max={var_sync[2]:.3f}")
