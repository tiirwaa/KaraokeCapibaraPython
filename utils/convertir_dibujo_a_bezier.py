import cv2
import numpy as np

def convertir_a_bezier(imagen_path, output_path):
    # Leer la imagen con canales alpha si existe
    img = cv2.imread(imagen_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error: No se pudo cargar la imagen {imagen_path}")
        return
    
    if img.shape[2] == 4:  # Imagen con alpha (RGBA)
        alpha = img[:, :, 3]
        thresh = (alpha > 0).astype(np.uint8) * 255  # Máscara de las líneas (donde alpha > 0)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)  # Para depuración
    else:  # Imagen sin alpha
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.shape[2] == 3 else img
        _, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV)
    
    # Encontrar todos los contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtrar contornos pequeños (ruido)
    contours = [c for c in contours if cv2.contourArea(c) > 10]
    
    print(f"Número de contornos detectados: {len(contours)}")
    
    # Depuración: dibujar contornos en la imagen original para verificar
    img_color = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)  # Convertir a color para dibujar en rojo
    cv2.drawContours(img_color, contours, -1, (0, 0, 255), 2)  # Dibujar todos los contornos en rojo
    cv2.imwrite('contours_debug.png', img_color)
    print("Imagen de depuración guardada como 'contours_debug.png'. Ábrela para ver los contornos detectados sobre la imagen original.")
    
    # Crear paths SVG
    svg_paths = []
    total_points = 0
    for contour in contours:
        if len(contour) < 3:
            continue
        # Aproximar el contorno con un polígono (esto crea líneas rectas, pero se pueden suavizar en un editor vectorial)
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        total_points += len(approx)
        
        # Construir el path SVG
        d = "M{},{} ".format(approx[0][0][0], approx[0][0][1])
        for point in approx[1:]:
            d += "L{},{} ".format(point[0][0], point[0][1])
        d += "Z"  # Cerrar el path
        svg_paths.append('<path d="{}" fill="none" stroke="black" stroke-width="1" />'.format(d))
    
    print(f"Número de paths SVG generados: {len(svg_paths)}")
    print(f"Total de puntos en los paths: {total_points}")
    print("Para verificar la fidelidad, abre la imagen original 'dibujo.png' y el SVG generado en un visor de imágenes/vectorial y compara visualmente.")
    
    # Crear contenido SVG
    height, width = img_gray.shape
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">
{}
</svg>'''.format(width, height, '\n'.join(svg_paths))
    
    # Escribir el archivo SVG
    with open(output_path, 'w') as f:
        f.write(svg_content)
    
    print(f"Conversión completada. Archivo guardado en {output_path}")
    print("Nota: Los paths están en líneas rectas. Para convertir a curvas Bézier suaves, abre el SVG en un editor como Inkscape y usa 'Object to Path' o 'Stroke to Path'.")
    
    # Comprobación del contenido SVG
    try:
        with open(output_path, 'r') as f:
            svg_content = f.read()
        print("\nContenido del archivo SVG generado:")
        print(svg_content[:1000])  # Mostrar los primeros 1000 caracteres para evitar output demasiado largo
        if len(svg_content) > 1000:
            print("... (contenido truncado)")
    except Exception as e:
        print(f"Error al leer el archivo SVG: {e}")

# Uso del script
if __name__ == "__main__":
    convertir_a_bezier('dibujo.png', 'dibujo_bezier.svg')