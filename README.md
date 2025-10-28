# Capibara Bailando# Capibara Bailando



## Descripción## Descripción

Proyecto Python que muestra una animación interactiva de un capibara bailando sincronizado con música. Incluye una implementación básica de física para saltos, efectos visuales (confeti, sombras), y un sistema de letras estilo karaoke.Proyecto Python que muestra una animación interactiva de un capibara bailando sincronizado con música. Incluye una implementación básica de física para saltos, efectos visuales (confeti, sombras), y un sistema de letras estilo karaoke.



## RequisitosEsta rama/documento describe la estructura actual del repositorio y cómo ejecutar el proyecto en Windows. Contiene instrucciones de instalación y notas sobre compatibilidad de audio.

- Python 3.8+

- Dependencias listadas en `requirements.txt`:## Contenido principal del repositorio

  - pygameEstructura (resumen):

  - numpy

  - Pillow- `main.py` — Punto de entrada principal.

  - opencv-python- `recreate_pngs.py` — Herramienta para regenerar PNGs (ver `recrear png.md`).

  - svgpathtools- `requirements.txt` — Lista de dependencias Python.

  - manim (opcional, para regenerar animaciones con `utils/animar_svg_manim.py`)- `res/` — Recursos (imágenes, SVGs, textos, colores, letras).

- `media/` — Medios (imágenes, videos) usados en pruebas/producción.

## Instalación- `src/` — Código fuente principal:

1. Clona o descarga el repositorio.   - `audio.py` — Gestión de audio (AudioManager).

2. Crea un entorno virtual:   - `capibara_model.py` — Representación y dibujo del capibara.

   ```powershell   - `game.py` — Bucle principal, manejo de eventos y composición de componentes.

   python -m venv .venv   - `lyrics.py` — Carga y sincronización de letras (karaoke).

   .\.venv\Scripts\Activate.ps1- `utils/` — Utilidades y scripts auxiliares (conversiones SVG, pruebas, color picker, etc.).

   ```

3. Instala dependencias:### Herramientas auxiliares (`utils/`)

   ```powershell

   pip install -r requirements.txtEl directorio `utils/` contiene varias utilidades para trabajar con los recursos SVG y colores del proyecto. Dos herramientas importantes incluidas son:

   ```

4. Asegúrate de tener recursos como `res/txt/letra.txt` y `res/wav/capibara.wav` (opcional).- `utils/color_picker.py` — Interfaz Pygame para pintar y asignar colores a los paths del SVG.

   - Ruta SVG por defecto: `res/svg/salida_bezier.svg` (referenciada como `../res/svg/salida_bezier.svg` desde `utils/`).

## Ejecución   - Archivo de salida por defecto: `res/txt/colors.json` (guardado como `../res/txt/colors.json`).

Ejecuta desde la raíz:   - Uso: desde la raíz del proyecto ejecuta:

```powershell

python main.py      ```powershell

```      python utils\color_picker.py

      ```

Controles:

- ESC: salir   - Permite seleccionar colores predefinidos y aplicarlos al path cerrado más cercano al clic. Guarda un JSON con el mapeo `path_index -> color`.



## Estructura del Proyecto- `utils/point_picker.py` — Herramienta para marcar puntos de referencia (landmarks) sobre el SVG.

- `main.py`: Punto de entrada principal.   - Ruta SVG por defecto: `res/svg/salida_bezier.svg` (referenciada como `../res/svg/salida_bezier.svg` desde `utils/`).

- `recreate_pngs.py`: Regenera PNGs de animación usando Manim y ffmpeg.   - Archivo de salida por defecto: `res/txt/landmarks.json` (guardado como `../res/txt/landmarks.json`).

- `src/`:   - Uso: desde la raíz del proyecto ejecuta:

  - `audio.py`: Gestiona audio con `pygame.mixer`.

  - `game.py`: Bucle principal, eventos, dibujo.      ```powershell

  - `capibara_model.py`: Modelo del capibara, carga frames PNG.      python utils\point_picker.py

  - `lyrics.py`: Manejo de letras karaoke.      ```

- `utils/`:

  - `color_picker.py`: Asigna colores a paths SVG.   - Flujo: hace zoom/ajusta el SVG en pantalla, permite marcar puntos con etiquetas en español (por ejemplo `mano_izquierda`, `cabeza`, `cola`, etc.), y guardar el resultado en JSON.

  - `point_picker.py`: Marca landmarks en SVG.

  - `convertir_dibujo_a_bezier.py`: Convierte imagen raster a SVG lineal.Notas sobre ejecución en Windows:

  - `convert_svg_to_bezier.py`: Convierte SVG lineal a Bézier.- `color_picker.py` establece `SDL_VIDEODRIVER=windib` para mejorar compatibilidad con algunas instalaciones de Pygame en Windows. Si la ventana no aparece, prueba a ajustar esa variable o ejecutar desde PowerShell con privilegios normales.

  - `animar_svg_manim.py`: Genera animación con Manim.- Ambas utilidades requieren `pygame`, `numpy` y `svgpathtools` (están listadas en `requirements.txt`).

- `res/`: Recursos (SVG, textos, colores, audio).

- `media/`: Imágenes y videos generados.Hay también archivos y carpetas auxiliares: `README.md`, `auditoria.md`, `recrear png.md`, `res/txt/letra.txt`, y scripts dentro de `utils/`.



## Utilidades## Requisitos

### Flujo para Preparar SVG- Python 3.8+ (o 3.x compatible).

1. Vectorizar dibujo raster a SVG lineal:- Dependencias (ver `requirements.txt`). Instálalas con:

   ```powershell

   python utils\convertir_dibujo_a_bezier.py```powershell

   ```pip install -r requirements.txt

   Genera `dibujo_bezier.svg`.```



2. Convertir a curvas Bézier:Dependencias clave incluidas en `requirements.txt`:

   ```powershell- pygame

   python utils\convert_svg_to_bezier.py dibujo_bezier.svg res/svg/salida_bezier.svg- numpy

   ```- Pillow

   Crea `res/svg/salida_bezier.svg` usado por la animación.- opencv-python

- svgpathtools

### Herramientas Interactivas- manim (opcional, para regenerar la animación con `utils/animar_svg_manim.py`)

- Asignar colores:

  ```powershell## Instalación rápida

  python utils\color_picker.py

  ```1. Clona o descarga el repositorio.

- Marcar landmarks:2. Crea y activa un entorno virtual (recomendado):

  ```powershell

  python utils\point_picker.py```powershell

  ```python -m venv .venv; .\.venv\Scripts\Activate.ps1

```

- Convertir PNG a SVG Bezier:

  ```powershell

  python utils/png_to_bezier_gui.py

  ```

  Interfaz gráfica para convertir un PNG a SVG Bezier. Selecciona un archivo PNG y una carpeta de salida; el proceso automatiza la conversión en dos pasos (raster a SVG lineal, luego a Bezier).

### Regenerar Animación

```powershell3. Instala dependencias:

python recreate_pngs.py

``````powershell

Requiere `manim` y `ffmpeg`.pip install -r requirements.txt

```

## Notas

- Audio usa `pygame.mixer` para portabilidad.4. Asegúrate de tener los recursos necesarios (por ejemplo, `res/txt/letra.txt` y el audio si lo usas). Si no tienes `capibara.wav`, la animación debería arrancar pero sin audio.

- Si faltan recursos, la animación puede ejecutarse sin audio o con placeholders.

- Para desarrollo, instala `manim` y `ffmpeg` para regenerar frames.## Ejecución



## AutorEjecuta el proyecto desde la raíz del repositorio:

Andrey Rodríguez Araya
```powershell
python main.py
```

Controles comunes (según implementación actualmente en `src/game.py`):
- ESC: salir

Si quieres ejecutar utilidades:

```powershell
python recreate_pngs.py
python utils/color_picker.py
python utils/point_picker.py
python utils/png_to_bezier_gui.py
```

Para regenerar las imágenes PNG que se usan como frames en la animación (workflow completo):

- `recreate_pngs.py` invoca primero `utils/animar_svg_manim.py` (usa Manim) y luego `ffmpeg` para extraer frames.
- Requisitos adicionales para este flujo:
   - Instalar `manim` (recomendado: la versión community disponible en pip como `manim`).
   - Tener `ffmpeg` disponible en PATH (instalación del sistema, no es un paquete pip).

Ejemplo (desde la raíz):

```powershell
python recreate_pngs.py
```

Si prefieres ejecutar solo Manim (para debug):

```powershell
python utils\animar_svg_manim.py
```

## Notas sobre audio y compatibilidad
- Audio: el proyecto ya usa `pygame.mixer` a través de `src/audio.py` (más portable que `winsound`). Si quieres usar otra librería (por ejemplo `pydub`) puedes reemplazar `AudioManager`.

Ejemplo mínimo de uso con `pygame.mixer` (similar a lo que hace `src/audio.py`):

```python
import pygame
pygame.mixer.init()
pygame.mixer.music.load('res/wav/capibara.wav')
pygame.mixer.music.play(-1)  # -1 = loop
```

## Solución de problemas rápida
- Si la ventana no aparece: asegúrate de que `pygame` esté instalado y que no haya excepciones al iniciar `main.py`.
- Si falta audio: confirma la ruta del archivo WAV o usa `pygame.mixer`.
- Si faltan recursos (SVG/PNG): revisa `res/` y `media/`.

## Siguientes mejoras sugeridas
1. Añadir `CONTRIBUTING.md` y un `LICENSE`.
2. Añadir tests unitarios mínimos (p. ej. comprobación de carga de recursos y parsing de `letra.txt`).
3. Añadir comprobaciones en el arranque para avisar recursos faltantes.

Adicional — resumen breve de archivos importantes (actualizado tras analizar el código):

- `main.py` — inicializa `pygame` y arranca la clase `Game` (entrada principal).
- `src/audio.py` — `AudioManager` singleton. Usa `pygame.mixer` para reproducir `res/wav/capibara.wav` por defecto.
- `src/game.py` — Clase `Game`: inicializa la ventana, el bucle principal, carga `Capibara`, `LyricsManager` y `AudioManager`. Dibuja césped, sombra, confeti y renderiza las letras estilo karaoke. Lee `res/txt/landmarks.json` si existe.
- `src/capibara_model.py` — `Capibara` carga frames PNG desde `media/images/animar_svg_manim/` y usa `svgpathtools` para calcular centros y anchors desde `res/svg/salida_bezier.svg` y `res/txt/landmarks.json`.
- `src/lyrics.py` — `LyricsManager` carga `res/txt/letra.txt`, procesa eventos de tipo `lyric` o `instrumental` y dibuja/animar palabras estilo karaoke.
- `recreate_pngs.py` — Script para regenerar la animación: corre `utils/animar_svg_manim.py` (Manim) y `ffmpeg` para extraer PNGs a `media/images/animar_svg_manim/`.

Utilidades en `utils/`:

- `utils/color_picker.py` — Interfaz Pygame para asignar colores a paths del SVG (`res/txt/colors.json`).
- `utils/point_picker.py` — Interfaz Pygame para marcar landmarks (guarda `res/txt/landmarks.json`).
- `utils/convert_svg_to_bezier.py` — Convierte paths a curvas Bézier (Catmull-Rom → CubicBezier) usando `svgpathtools`.
- `utils/convertir_dibujo_a_bezier.py` — Extrae contornos desde una imagen usando OpenCV y genera un SVG (paths lineales). Útil para vectorizar un dibujo escaneado.
- `utils/png_to_bezier_gui.py` — Interfaz gráfica (tkinter) para convertir un PNG a SVG Bezier. Selecciona un PNG, lo procesa en dos pasos (raster a SVG lineal, luego a Bezier), y guarda el resultado en una carpeta elegida.
- `utils/animar_svg_manim.py` — Escena Manim que carga `res/svg/salida_bezier.svg`, aplica colores desde `res/txt/colors.json` / `landmarks.json` y genera `SVGAnimation.mov`/PNGs. Requiere `manim` y `ffmpeg`.

- Flujo para convertir un dibujo a la versión Bézier usada en la animación

1) Vectorizar el dibujo raster (ej. `dibujo.png`) a un SVG con paths lineales usando OpenCV:

```powershell
python utils\convertir_dibujo_a_bezier.py
```

Esto genera por defecto un SVG con paths poligonales (líneas) como `dibujo_bezier.svg` (o el archivo que especifiques). Es un primer paso para obtener un SVG desde una imagen escaneada o dibujada a mano.

2) Convertir los paths poligonales a curvas Bézier suaves (Catmull-Rom → CubicBezier) usando `svgpathtools`:

```powershell
python utils\convert_svg_to_bezier.py dibujo_bezier.svg res/svg/salida_bezier.svg
```

Este script crea `salida_bezier.svg`, que es el SVG final con curvas cúbicas que usan `utils/animar_svg_manim.py` y `src/capibara_model.py`.

Resumen: convertir_dibujo_a_bezier.py (raster -> SVG lineal) → convert_svg_to_bezier.py (SVG lineal -> SVG Bézier `salida_bezier.svg`) → animar_svg_manim.py / Manim para generar frames.

Alternativamente, usa `python utils/png_to_bezier_gui.py` para una interfaz gráfica que automatiza estos pasos y permite elegir la carpeta de salida.

Notas rápidas de compatibilidad y uso:
- Para editar colores/landmarks antes de renderizar con Manim, usa `utils/color_picker.py` y `utils/point_picker.py`.
- Si no tienes `capibara.wav`, la animación arranca sin audio pero las letras y la sincronización dependerán de `pygame.mixer.music.get_pos()` en `src/game.py`.

## Autor
Andrey Rodríguez Araya

---