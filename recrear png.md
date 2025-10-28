# Instrucciones para recrear los PNGs de la animación

Sigue estos comandos en orden desde el directorio raíz del proyecto (`c:\Users\Andrey\Documentos\capibara`):

1. **Generar el video MOV con Manim:**
   ```
   python utils/animar_svg_manim.py
   ```
   Esto crea `media/videos/900p15/SVGAnimation.mov` con la animación renderizada.

2. **Extraer los frames PNG del MOV:**
   ```
   cd media/videos/900p15
   ffmpeg -i SVGAnimation.mov %04d.png
   cd ../../../
   ```
   Esto genera `0001.png` a `0158.png` en `media/videos/900p15/`.

3. **Mover los PNGs al directorio de imágenes (eliminando los antiguos):**
   ```
   rm media/images/animar_svg_manim/*.png
   move media/videos/900p15/*.png media/images/animar_svg_manim/
   ```
   Los PNGs quedan en `media/images/animar_svg_manim/` listos para usar.

4. **Probar la animación:**
   ```
   cd src
   python game.py
   ```
   Esto ejecuta el juego con los nuevos frames.

**Notas:**
- Asegúrate de que `colors.json` tenga los colores deseados para personalizar la apariencia.
- Si modificas colores en `color_picker.py`, guarda y regenera.
- Los PNGs tienen transparencia y se usan en `game.py` para la animación.