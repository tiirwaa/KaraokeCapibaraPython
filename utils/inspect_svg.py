from svgpathtools import svg2paths, Line

# Cargar el SVG
paths, attributes = svg2paths('res/svg/salida_bezier.svg')

print(f"Total paths: {len(paths)}")
for i, path in enumerate(paths):
    # Obtener el punto inicial
    start_point = path.start
    # Calcular longitud aproximada
    length = path.length()
    # Bounding box
    bbox = path.bbox()
    min_x, max_x, min_y, max_y = bbox
    # Es línea recta?
    is_line = len(path) == 1 and isinstance(path[0], Line)
    print(f"Path {i}: Start ({start_point.real:.1f}, {start_point.imag:.1f}), Length: {length:.1f}, BBox: x[{min_x:.1f}-{max_x:.1f}] y[{min_y:.1f}-{max_y:.1f}], Is Line: {is_line}")