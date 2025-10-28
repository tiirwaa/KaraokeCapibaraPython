# Capibara Bailando

## Descripción
Proyecto Python que muestra una animación interactiva de un capibara bailando sincronizado con música. Incluye una implementación básica de física para saltos, efectos visuales (confeti, sombras), y un sistema de letras estilo karaoke.

Esta rama/documento describe la estructura actual del repositorio y cómo ejecutar el proyecto en Windows. Contiene instrucciones de instalación y notas sobre compatibilidad de audio.

## Contenido principal del repositorio
Estructura (resumen):

- `main.py` — Punto de entrada principal.
- `recreate_pngs.py` — Herramienta para regenerar PNGs (ver `recrear png.md`).
- `requirements.txt` — Lista de dependencias Python.
- `res/` — Recursos (imágenes, SVGs, textos, colores, letras).
- `media/` — Medios (imágenes, videos) usados en pruebas/producción.
- `src/` — Código fuente principal:
   - `audio.py` — Gestión de audio (AudioManager).
   - `capibara_model.py` — Representación y dibujo del capibara.
   - `game.py` — Bucle principal, manejo de eventos y composición de componentes.
   - `lyrics.py` — Carga y sincronización de letras (karaoke).
- `utils/` — Utilidades y scripts auxiliares (conversiones SVG, pruebas, color picker, etc.).

### Herramientas auxiliares (`utils/`)

El directorio `utils/` contiene varias utilidades para trabajar con los recursos SVG y colores del proyecto. Dos herramientas importantes incluidas son:

- `utils/color_picker.py` — Interfaz Pygame para pintar y asignar colores a los paths del SVG.
   - Ruta SVG por defecto: `res/svg/salida_bezier.svg` (referenciada como `../res/svg/salida_bezier.svg` desde `utils/`).
   - Archivo de salida por defecto: `res/txt/colors.json` (guardado como `../res/txt/colors.json`).
   - Uso: desde la raíz del proyecto ejecuta:

      ```powershell
      python utils\color_picker.py
      ```

   - Permite seleccionar colores predefinidos y aplicarlos al path cerrado más cercano al clic. Guarda un JSON con el mapeo `path_index -> color`.

- `utils/point_picker.py` — Herramienta para marcar puntos de referencia (landmarks) sobre el SVG.
   - Ruta SVG por defecto: `res/svg/salida_bezier.svg` (referenciada como `../res/svg/salida_bezier.svg` desde `utils/`).
   - Archivo de salida por defecto: `res/txt/landmarks.json` (guardado como `../res/txt/landmarks.json`).
   - Uso: desde la raíz del proyecto ejecuta:

      ```powershell
      python utils\point_picker.py
      ```

   - Flujo: hace zoom/ajusta el SVG en pantalla, permite marcar puntos con etiquetas en español (por ejemplo `mano_izquierda`, `cabeza`, `cola`, etc.), y guardar el resultado en JSON.

Notas sobre ejecución en Windows:
- `color_picker.py` establece `SDL_VIDEODRIVER=windib` para mejorar compatibilidad con algunas instalaciones de Pygame en Windows. Si la ventana no aparece, prueba a ajustar esa variable o ejecutar desde PowerShell con privilegios normales.
- Ambas utilidades requieren `pygame`, `numpy` y `svgpathtools` (están listadas en `requirements.txt`).

Hay también archivos y carpetas auxiliares: `README.md`, `auditoria.md`, `recrear png.md`, `res/txt/letra.txt`, y scripts dentro de `utils/`.

## Requisitos
- Python 3.8+ (o 3.x compatible).
- Dependencias (ver `requirements.txt`). Instálalas con:

```powershell
pip install -r requirements.txt
```

Dependencias clave incluidas en `requirements.txt`:
- pygame
- numpy
- Pillow
- opencv-python
- svgpathtools

Nota sobre audio: el proyecto contiene código que usa `winsound` (Windows). Si quieres soporte multiplataforma, reemplaza `winsound` por `pygame.mixer` o `pydub`.

## Instalación rápida

1. Clona o descarga el repositorio.
2. Crea y activa un entorno virtual (recomendado):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

3. Instala dependencias:

```powershell
pip install -r requirements.txt
```

4. Asegúrate de tener los recursos necesarios (por ejemplo, `res/txt/letra.txt` y el audio si lo usas). Si no tienes `capibara.wav`, la animación debería arrancar pero sin audio.

## Ejecución

Ejecuta el proyecto desde la raíz del repositorio:

```powershell
python main.py
```

Controles comunes (según implementación actualmente en `src/game.py`):
- ESC: salir
- S: detener o silenciar el audio

Si quieres ejecutar utilidades:

```powershell
python recreate_pngs.py
python utils/color_picker.py
```

## Notas sobre audio y compatibilidad
- Windows: el código puede usar `winsound` para reproducir WAVs (rápido y simple). Eso limita la reproducibilidad en macOS/Linux.
- Recomendación: migrar a `pygame.mixer` para reproducir audio de forma multiplataforma; `pygame` ya está en `requirements.txt`.

Ejemplo mínimo de uso con `pygame.mixer` (si decides migrar):

```python
import pygame
pygame.mixer.init()
pygame.mixer.music.load('capibara.wav')
pygame.mixer.music.play()
```

## Solución de problemas rápida
- Si la ventana no aparece: asegúrate de que `pygame` esté instalado y que no haya excepciones al iniciar `main.py`.
- Si falta audio: confirma la ruta del archivo WAV o usa `pygame.mixer`.
- Si faltan recursos (SVG/PNG): revisa `res/` y `media/`.

## Siguientes mejoras sugeridas
1. Añadir `CONTRIBUTING.md` y un `LICENSE`.
2. Añadir tests unitarios mínimos (p. ej. comprobación de carga de recursos y parsing de `letra.txt`).
3. Reemplazar `winsound` por `pygame.mixer` para multiplataforma.
4. Añadir comprobaciones en el arranque para avisar recursos faltantes.

## Autor
Andrey Rodríguez Araya

---

Si quieres, puedo también:
- Ejecutar una prueba rápida (arrancar `main.py`) y reportar errores/advertencias.
- Añadir sección `CONTRIBUTING.md` o un archivo `SUPPORT.md` con instrucciones de depuración.