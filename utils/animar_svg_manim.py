from manim import *
import json
import math
import numpy as np
from svgpathtools import svg2paths

config.transparent = True
config.quality = "low_quality"
config.save_pngs = True
config.write_to_movie = True
config.frame_size = (1280, 900)


class SVGAnimation(Scene):
    def construct(self):
        # Cargar el SVG completo usando SVGMobject
        svg = SVGMobject('res/svg/salida_bezier.svg')

        # Cambiar el color del trazo a negro para que sea visible en el fondo azul, y más grueso
        svg.set_stroke(BLACK, 4)
        svg.set_fill(opacity=0)  # Sin relleno

        # Escalar y centrar el SVG
        svg.scale(5)  # Match the scale in capibara.py for consistent debugging
        svg.move_to(ORIGIN)

        # Seleccionar pies/piernas usando landmarks guardados para evitar mapeos incorrectos
        # Cargamos los landmarks (coordenadas en espacio SVG, generadas por utils/point_picker.py)
        import json
        from svgpathtools import svg2paths

        landmarks_path = 'res/txt/landmarks.json'
        try:
            with open(landmarks_path, 'r', encoding='utf-8') as lf:
                lm = json.load(lf)
                labels = {p['label']: tuple(p['svg']) for p in lm.get('labels', [])}
        except Exception as e:
            print(f'Warning: no se pudo cargar {landmarks_path}: {e}. Usando mapeo por defecto.')
            labels = {}

        # Usar svgpathtools para calcular centros por path (asumimos mismo orden de submobjects)
        paths, _ = svg2paths('res/svg/salida_bezier.svg')
        def path_center(path, n=200):
            pts = [path.point(t) for t in np.linspace(0, 1, n)]
            xs = [p.real for p in pts]
            ys = [p.imag for p in pts]
            return (sum(xs)/len(xs), sum(ys)/len(ys))


        def norm_color(rgb):
            """Normalize a color to a list of floats in 0..1 suitable for Manim.set_fill.
            Accepts:
              - list/tuple of 3 ints (0..255)
              - list/tuple of 3 floats (0..1)
              - list/tuple of 4 floats/ints (RGBA)
            Returns list of 3 floats [R,G,B] or None on bad input.
            """
            if rgb is None:
                return None
            try:
                # If it's something like numpy types, convert to native python numbers
                rgb_list = list(rgb)
            except Exception:
                return None
            if len(rgb_list) >= 3:
                r, g, b = rgb_list[0], rgb_list[1], rgb_list[2]
                try:
                    # If values appear to be integers > 1, assume 0..255 and convert to hex
                    def to_int(x):
                        try:
                            return int(x)
                        except Exception:
                            return 0

                    if any(isinstance(c, (int,)) and c > 1 for c in (r, g, b)):
                        ri, gi, bi = to_int(r), to_int(g), to_int(b)
                    else:
                        # assume floats 0..1 -> convert to 0..255
                        ri = int(round(float(r) * 255.0))
                        gi = int(round(float(g) * 255.0))
                        bi = int(round(float(b) * 255.0))
                    # clamp
                    ri = max(0, min(255, ri))
                    gi = max(0, min(255, gi))
                    bi = max(0, min(255, bi))
                    return "#{:02X}{:02X}{:02X}".format(ri, gi, bi)
                except Exception:
                    return None
            return None

        path_centers = [path_center(p) for p in paths]

        def nearest_path_indices(pt, k=2):
            # retorna índices de los k paths más cercanos al punto pt (x,y)
            dists = [math.hypot(pc[0]-pt[0], pc[1]-pt[1]) for pc in path_centers]
            idxs = sorted(range(len(dists)), key=lambda i: dists[i])
            return idxs[:k]

        # Mapear pies (puede haber varios subpaths que forman el pie; tomamos los 2 más cercanos)
        left_foot_idxs = []
        right_foot_idxs = []
        if 'pie_izquierdo' in labels:
            left_foot_idxs = nearest_path_indices(labels['pie_izquierdo'], k=2)
        if 'pie_derecho' in labels:
            right_foot_idxs = nearest_path_indices(labels['pie_derecho'], k=2)

        # Mapear coxofemorales (usaremos el más cercano como la "pierna")
        left_leg_idx = None
        right_leg_idx = None
        if 'coxofemoral_izquierda' in labels:
            left_leg_idx = nearest_path_indices(labels['coxofemoral_izquierda'], k=1)[0]
        if 'coxofemoral_derecha' in labels:
            right_leg_idx = nearest_path_indices(labels['coxofemoral_derecha'], k=1)[0]

        # Evitar asignar la misma path a múltiples partes: deduplicar índices
        used_idxs = set()
        def take_unique(idxs):
            out = []
            for i in idxs:
                if i not in used_idxs:
                    out.append(i)
                    used_idxs.add(i)
            return out

        # Convertir índices de paths a submobjects del SVGMobject (mismo orden)
        def submobj(i):
            try:
                return svg.submobjects[i]
            except Exception:
                return None

        # apply deduplication so one path isn't assigned twice
        left_foot_idxs = take_unique(left_foot_idxs)
        right_foot_idxs = take_unique(right_foot_idxs)
        # ensure legs indices are reserved too
        if left_leg_idx is not None and left_leg_idx not in used_idxs:
            used_idxs.add(left_leg_idx)
        if right_leg_idx is not None and right_leg_idx not in used_idxs:
            used_idxs.add(right_leg_idx)

        left_foot_subs = [submobj(i) for i in left_foot_idxs if submobj(i) is not None]
        # deduplicate by object id to avoid adding same submobject twice
        seen = set()
        uniq_left = []
        for s in left_foot_subs:
            if id(s) not in seen:
                uniq_left.append(s)
                seen.add(id(s))
        left_foot_subs = uniq_left

        right_foot_subs = [submobj(i) for i in right_foot_idxs if submobj(i) is not None]
        uniq_right = []
        for s in right_foot_subs:
            if id(s) not in seen:
                uniq_right.append(s)
                seen.add(id(s))
        right_foot_subs = uniq_right
        left_leg_sub = submobj(left_leg_idx) if left_leg_idx is not None else None
        right_leg_sub = submobj(right_leg_idx) if right_leg_idx is not None else None

        # Debug prints: mostrar mapeo encontrado
        print('Landmark -> path indices:')
        print(' left_foot_idxs=', left_foot_idxs)
        print(' right_foot_idxs=', right_foot_idxs)
        print(' left_leg_idx=', left_leg_idx, ' right_leg_idx=', right_leg_idx)
        try:
            print(' left_foot_centers=', [path_centers[i] for i in left_foot_idxs])
            print(' right_foot_centers=', [path_centers[i] for i in right_foot_idxs])
            if left_leg_idx is not None:
                print(' left_leg_center=', path_centers[left_leg_idx])
            if right_leg_idx is not None:
                print(' right_leg_center=', path_centers[right_leg_idx])
        except Exception:
            pass

        # Crear grupos leg -> include leg + its foot submobjects
        # Ensure we don't add the same submobject twice into a group
        def make_leg_group(leg_sub, foot_subs):
            members = []
            if leg_sub is not None:
                members.append(leg_sub)
            for fs in foot_subs:
                if all(fs is not m for m in members):
                    members.append(fs)
            return VGroup(*members) if members else VGroup()

        leg_group0 = make_leg_group(left_leg_sub, left_foot_subs)
        leg_group1 = make_leg_group(right_leg_sub, right_foot_subs)

        legs = VGroup(leg_group0, leg_group1)
        # Flat feet group for legacy prints/usage
        feet = VGroup(*([s for s in (left_foot_subs + right_foot_subs) if s is not None]))

        # Mapear otros puntos nuevos
        head_idxs = []
        neck_idx = None
        tail_idx = None
        left_ear_idx = None
        right_ear_idx = None
        left_eye_idx = None
        right_eye_idx = None
        nose_idx = None
        mouth_idx = None
        chest_idx = None
        abdomen_idx = None
        back_idx = None
        left_glasses_idxs = []
        right_glasses_idxs = []
        left_cheek_idxs = []
        right_cheek_idxs = []
        forehead_idxs = []

        if 'cabeza' in labels:
            head_idxs = nearest_path_indices(labels['cabeza'], k=10)  # Más paths para cubrir toda la cara y pelo
        if 'cuello' in labels:
            neck_idx = nearest_path_indices(labels['cuello'], k=1)[0]
        if 'cola' in labels:
            tail_idx = nearest_path_indices(labels['cola'], k=1)[0]
        if 'oreja_izquierda' in labels:
            left_ear_idx = nearest_path_indices(labels['oreja_izquierda'], k=1)[0]
        if 'oreja_derecha' in labels:
            right_ear_idx = nearest_path_indices(labels['oreja_derecha'], k=1)[0]
        if 'ojo_izquierdo' in labels:
            left_eye_idx = nearest_path_indices(labels['ojo_izquierdo'], k=1)[0]
        if 'ojo_derecho' in labels:
            right_eye_idx = nearest_path_indices(labels['ojo_derecho'], k=1)[0]
        if 'nariz' in labels:
            nose_idx = nearest_path_indices(labels['nariz'], k=1)[0]
        if 'boca' in labels:
            mouth_idx = nearest_path_indices(labels['boca'], k=1)[0]
        if 'pecho' in labels:
            chest_idx = nearest_path_indices(labels['pecho'], k=1)[0]
        if 'abdomen' in labels:
            abdomen_idx = nearest_path_indices(labels['abdomen'], k=1)[0]
        if 'espalda' in labels:
            back_idx = nearest_path_indices(labels['espalda'], k=1)[0]
        if 'anteojo izquierdo' in labels:
            left_glasses_idxs = nearest_path_indices(labels['anteojo izquierdo'], k=5)
        if 'anteojo derecho' in labels:
            right_glasses_idxs = nearest_path_indices(labels['anteojo derecho'], k=5)
        if 'cachete izquierdo' in labels:
            left_cheek_idxs = nearest_path_indices(labels['cachete izquierdo'], k=2)
        if 'cachete derecho' in labels:
            right_cheek_idxs = nearest_path_indices(labels['cachete derecho'], k=2)
        if 'frente' in labels:
            forehead_idxs = nearest_path_indices(labels['frente'], k=5)

        # Excluir índices de anteojos de la cabeza para evitar conflicto de colores
        head_idxs = [idx for idx in head_idxs if idx not in left_glasses_idxs and idx not in right_glasses_idxs]

        # Excluir índices de cachetes y frente de anteojos para evitar colorear partes equivocadas
        left_glasses_idxs = [idx for idx in left_glasses_idxs if idx not in left_cheek_idxs and idx not in right_cheek_idxs and idx not in forehead_idxs and idx != left_ear_idx and idx != right_ear_idx]
        right_glasses_idxs = [idx for idx in right_glasses_idxs if idx not in left_cheek_idxs and idx not in right_cheek_idxs and idx not in forehead_idxs and idx != left_ear_idx and idx != right_ear_idx]

        # Excluir índices de ojos de cachetes y frente para evitar colorear partes equivocadas
        left_cheek_idxs = [idx for idx in left_cheek_idxs if idx != left_eye_idx and idx != right_eye_idx and idx not in left_glasses_idxs and idx not in right_glasses_idxs and idx != left_ear_idx and idx != right_ear_idx]
        right_cheek_idxs = [idx for idx in right_cheek_idxs if idx != left_eye_idx and idx != right_eye_idx and idx not in left_glasses_idxs and idx not in right_glasses_idxs and idx != left_ear_idx and idx != right_ear_idx]
        forehead_idxs = [idx for idx in forehead_idxs if idx != left_eye_idx and idx != right_eye_idx and idx not in left_glasses_idxs and idx not in right_glasses_idxs and idx != left_ear_idx and idx != right_ear_idx]

        # Debug prints after exclusions
        print(' forehead path centers=', [path_centers[i] for i in forehead_idxs])
        print(' right_glasses path centers=', [path_centers[i] for i in right_glasses_idxs])
        print(' left_glasses path centers=', [path_centers[i] for i in left_glasses_idxs])
        for idx in head_idxs + [neck_idx, tail_idx, left_ear_idx, right_ear_idx, left_eye_idx, right_eye_idx, nose_idx, mouth_idx, chest_idx, abdomen_idx, back_idx] + left_cheek_idxs + right_cheek_idxs + forehead_idxs + left_glasses_idxs + right_glasses_idxs:
            if idx is not None and idx not in used_idxs:
                used_idxs.add(idx)

        # Crear submobjects
        head_subs = [submobj(i) for i in head_idxs if submobj(i) is not None]
        neck_sub = submobj(neck_idx) if neck_idx is not None else None
        tail_sub = submobj(tail_idx) if tail_idx is not None else None
        left_ear_sub = submobj(left_ear_idx) if left_ear_idx is not None else None
        right_ear_sub = submobj(right_ear_idx) if right_ear_idx is not None else None
        left_eye_sub = submobj(left_eye_idx) if left_eye_idx is not None else None
        right_eye_sub = submobj(right_eye_idx) if right_eye_idx is not None else None
        nose_sub = submobj(nose_idx) if nose_idx is not None else None
        mouth_sub = submobj(mouth_idx) if mouth_idx is not None else None
        chest_sub = submobj(chest_idx) if chest_idx is not None else None
        abdomen_sub = submobj(abdomen_idx) if abdomen_idx is not None else None
        back_sub = submobj(back_idx) if back_idx is not None else None
        left_glasses_subs = [submobj(i) for i in left_glasses_idxs if submobj(i) is not None]
        right_glasses_subs = [submobj(i) for i in right_glasses_idxs if submobj(i) is not None]
        left_cheek_subs = [submobj(i) for i in left_cheek_idxs if submobj(i) is not None]
        right_cheek_subs = [submobj(i) for i in right_cheek_idxs if submobj(i) is not None]
        forehead_subs = [submobj(i) for i in forehead_idxs if submobj(i) is not None]

        # Load colors from JSON
        colors_path = 'res/txt/colors.json'
        try:
            with open(colors_path, 'r', encoding='utf-8') as f:
                color_data = json.load(f)
                path_colors = color_data.get('path_colors', {})
        except Exception as e:
            print(f'Warning: could not load {colors_path}: {e}')
            path_colors = {}

        print("Loaded path_colors from json:", path_colors)

        # Collect submobjects to remove if color is white (255,255,255)
        to_remove = []

        # Apply colors to individual paths
        for idx_str, rgb in path_colors.items():
            idx = int(idx_str)
            sub = submobj(idx)
            if sub is not None:
                # Diagnostic prints: show the raw rgb loaded from JSON and its type
                print(f"DEBUG: path {idx} - raw RGB from json: {rgb} (type={type(rgb)})")
                if rgb == [255, 255, 255]:
                    to_remove.append(sub)
                    print(f"Removing white path {idx}")
                else:
                    # Apply as-is (no behavior change) but then print what Manim stored
                    try:
                        # Normalize rgb (0..255 ints -> 0..1 floats) before passing to Manim
                        normalized = norm_color(rgb)
                        if normalized is None:
                            # fallback to original value if normalization failed
                            sub.set_fill(rgb, opacity=1)
                        else:
                            sub.set_fill(normalized, opacity=1)
                    except Exception as e:
                        print(f"DEBUG: Error calling set_fill on path {idx} with {rgb}: {e}")
                    # After calling set_fill, inspect the object's fill_color (how Manim interpreted it)
                    try:
                        internal_color = tuple(sub.fill_color)
                    except Exception:
                        internal_color = getattr(sub, 'fill_color', None)
                    print(f"DEBUG: path {idx} - after set_fill, sub.fill_color = {internal_color} (type={type(internal_color)})")
                    print(f"Set path {idx} to color {rgb}")

        print(f"Applied individual colors. Submobjects with fill: {len([s for s in svg.submobjects if s.fill_opacity > 0])}")

        # Crear grupos
        head_group = VGroup(*[s for s in head_subs + [neck_sub, left_ear_sub, right_ear_sub, left_eye_sub, right_eye_sub, nose_sub, mouth_sub] + left_cheek_subs + right_cheek_subs + forehead_subs if s is not None])
        body_group = VGroup(*[s for s in [chest_sub, abdomen_sub, back_sub] if s is not None])
        tail_group = VGroup(tail_sub) if tail_sub else VGroup()
        glasses_group = VGroup(*[s for s in left_glasses_subs + right_glasses_subs if s is not None])

        # Apply group colors based on individual colors in the group to correct correlation
        def apply_group_color_from_individual(group):
            # Diagnostic: inspect what colors individual submobjects have (as stored internally)
            colors_in_group = []
            for sub in group.submobjects:
                if sub.fill_opacity > 0:
                    try:
                        colors_in_group.append(tuple(sub.fill_color))
                    except Exception:
                        colors_in_group.append(getattr(sub, 'fill_color', None))
            unique_colors = list(set(colors_in_group))
            print(f"DEBUG: group {group} - colors_in_group={colors_in_group} unique_colors={unique_colors}")
            if len(unique_colors) == 1 and unique_colors[0] is not None:
                # Compute a proper group_color normalized to 0..1 floats
                col = unique_colors[0]
                # col may be (r,g,b,a) or (r,g,b)
                try:
                    col3 = tuple(col[:3])
                except Exception:
                    col3 = None
                group_color = norm_color(col3) if col3 is not None else None
                print(f"DEBUG: group {group} - computed normalized group_color = {group_color}")
                if group_color is not None:
                    for sub in group.submobjects:
                        sub.set_fill(group_color, opacity=1)
                print(f"Set group to color {group_color}")

        apply_group_color_from_individual(head_group)
        apply_group_color_from_individual(body_group)
        apply_group_color_from_individual(tail_group)
        apply_group_color_from_individual(legs)

        # For glasses, set to black if any is colored black, else keep
        glasses_colors = [tuple(sub.fill_color) for sub in glasses_group.submobjects if sub.fill_opacity > 0]
        if (0,0,0) in glasses_colors:
            for sub in glasses_group.submobjects:
                sub.set_fill(BLACK, opacity=1)

        print(f"After group colors. Submobjects with fill: {len([s for s in svg.submobjects if s.fill_opacity > 0])}")

        # Colores específicos para ojos, nariz, boca
        if left_eye_sub:
            left_eye_sub.set_fill(BLACK, opacity=1)
        if right_eye_sub:
            right_eye_sub.set_fill(BLACK, opacity=1)
        if nose_sub:
            nose_sub.set_fill("#FFB6C1", opacity=1)  # Light pink
        if mouth_sub:
            mouth_sub.set_fill("#FFB6C1", opacity=1)  # Light pink

        # Asegurar que los anteojos sean negros
        for sub in left_glasses_subs:
            sub.set_fill(BLACK, opacity=1)
        for sub in right_glasses_subs:
            sub.set_fill(BLACK, opacity=1)

        # Forzar regeneración de cache 2
        left_joint = labels.get('coxofemoral_izquierda', (0,0))
        right_joint = labels.get('coxofemoral_derecha', (0,0))
        # Escalar por 5 (como el SVG) y asumir origen en (0,0)
        left_joint_point = np.array([left_joint[0] * 5, left_joint[1] * 5, 0])
        right_joint_point = np.array([right_joint[0] * 5, right_joint[1] * 5, 0])

        # Puntos de rotación para cabeza y cola
        head_center = labels.get('cabeza', (0,0))
        head_point = np.array([head_center[0] * 5, head_center[1] * 5, 0])
        tail_center = labels.get('cola', (0,0))
        tail_point = np.array([tail_center[0] * 5, tail_center[1] * 5, 0])

        print("Regenerating animation with updated glasses coloring 3")

        # Remove submobjects with white color
        for sub in to_remove:
            svg.remove(sub)
        print(f"Removed {len(to_remove)} white paths. Total submobjects now: {len(svg.submobjects)}")

        # Ensure all submobjects have fill to avoid transparent (blue) areas
        default_set = 0
        for sub in svg.submobjects:
            if sub.fill_opacity == 0:
                sub.set_fill((240, 240, 240), opacity=1)  # Default to light gray for uncolored parts, matching color_picker
                default_set += 1
        print(f"Set default color to {default_set} uncolored submobjects. Total colored: {len([s for s in svg.submobjects if s.fill_opacity > 0])}")

        # Collect unique colors for debugging
        colors_used = set()
        for sub in svg.submobjects:
            if sub.fill_opacity > 0:
                colors_used.add(tuple(sub.fill_color))
        print(f"Unique colors used: {sorted(colors_used)}")

        self.add(svg)
        self.wait(1)

        # Animación de baile: rotaciones y movimientos; rotamos las piernas (padres) para que las patas las sigan
        # Girar a la izquierda
        self.play(leg_group0.animate.rotate(PI/8, about_point=left_joint_point), leg_group1.animate.rotate(PI/8, about_point=right_joint_point), run_time=0.5)
        print(f"After left turn: Feet center: {feet.get_center()}, Legs center: {legs.get_center()}")
        # Wiggle (rotaciones aplicadas a las piernas -> las patas siguen automáticamente)
        self.play(leg_group0.animate.rotate(-PI/4, about_point=left_joint_point), leg_group1.animate.rotate(-PI/4, about_point=right_joint_point), run_time=0.2)
        self.play(leg_group0.animate.rotate(PI/4, about_point=left_joint_point), leg_group1.animate.rotate(PI/4, about_point=right_joint_point), run_time=0.2)

        # Girar a la derecha
        self.play(leg_group0.animate.rotate(-PI/8, about_point=left_joint_point), leg_group1.animate.rotate(-PI/8, about_point=right_joint_point), run_time=0.5)
        print(f"After right turn: Feet center: {feet.get_center()}, Legs center: {legs.get_center()}")
        # Wiggle
        self.play(leg_group0.animate.rotate(PI/4, about_point=left_joint_point), leg_group1.animate.rotate(PI/4, about_point=right_joint_point), run_time=0.2)
        self.play(leg_group0.animate.rotate(-PI/4, about_point=left_joint_point), leg_group1.animate.rotate(-PI/4, about_point=right_joint_point), run_time=0.2)

        # Volver al centro
        self.play(leg_group0.animate.rotate(PI/8, about_point=left_joint_point), leg_group1.animate.rotate(PI/8, about_point=right_joint_point), run_time=0.5)
        print(f"After center: Feet center: {feet.get_center()}, Legs center: {legs.get_center()}")

        # Bounce: aplicamos shifts a las piernas
        self.play(leg_group0.animate.shift(DOWN * 0.2).rotate(PI/24, about_point=left_joint_point), leg_group1.animate.shift(DOWN * 0.2).rotate(PI/24, about_point=right_joint_point), run_time=0.3)
        self.play(leg_group0.animate.shift(DOWN * 0.1).rotate(-PI/24, about_point=left_joint_point), leg_group1.animate.shift(DOWN * 0.1).rotate(-PI/24, about_point=right_joint_point), run_time=0.3)
        self.play(leg_group0.animate.shift(UP * 0.1).rotate(PI/24, about_point=left_joint_point), leg_group1.animate.shift(UP * 0.1).rotate(PI/24, about_point=right_joint_point), run_time=0.3)
        print(f"After bounce: Feet center: {feet.get_center()}, Legs center: {legs.get_center()}")

        self.play(leg_group0.animate.rotate(PI/6, about_point=left_joint_point), leg_group1.animate.rotate(PI/6, about_point=right_joint_point), run_time=0.4)
        # Wiggle
        self.play(leg_group0.animate.rotate(-PI/3, about_point=left_joint_point), leg_group1.animate.rotate(-PI/3, about_point=right_joint_point), run_time=0.2)
        self.play(leg_group0.animate.rotate(PI/3, about_point=left_joint_point), leg_group1.animate.rotate(PI/3, about_point=right_joint_point), run_time=0.2)

        self.play(leg_group0.animate.rotate(-PI/6, about_point=left_joint_point), leg_group1.animate.rotate(-PI/6, about_point=right_joint_point), run_time=0.4)
        # Wiggle
        self.play(leg_group0.animate.rotate(PI/3, about_point=left_joint_point), leg_group1.animate.rotate(PI/3, about_point=right_joint_point), run_time=0.2)
        self.play(leg_group0.animate.rotate(-PI/3, about_point=left_joint_point), leg_group1.animate.rotate(-PI/3, about_point=right_joint_point), run_time=0.2)

        self.play(leg_group0.animate.rotate(PI/6, about_point=left_joint_point), leg_group1.animate.rotate(PI/6, about_point=right_joint_point), run_time=0.4)
        print(f"After final turns: Feet center: {feet.get_center()}, Legs center: {legs.get_center()}")

        # Animar cabeza y cola
        if head_group:
            self.play(head_group.animate.rotate(PI/12, about_point=head_point), run_time=0.3)
            self.play(head_group.animate.rotate(-PI/12, about_point=head_point), run_time=0.3)
        if tail_group:
            self.play(tail_group.animate.shift(RIGHT * 0.1).rotate(PI/8), run_time=0.2)
            self.play(tail_group.animate.shift(LEFT * 0.1).rotate(-PI/8), run_time=0.2)

        # Final: volver a posición original
        # Rotar legs a 0 (siempre alrededor de su centro) y mover svg al origen
        self.play(svg.animate.move_to(ORIGIN), leg_group0.animate.rotate(0, about_point=left_joint_point), leg_group1.animate.rotate(0, about_point=right_joint_point), run_time=1)
        if head_group:
            self.play(head_group.animate.rotate(0, about_point=head_point), run_time=0.5)
        if tail_group:
            self.play(tail_group.animate.rotate(0), run_time=0.5)

        self.wait(1)

if __name__ == '__main__':
    scene = SVGAnimation()
    scene.render()