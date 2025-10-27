# Capibara Bailando

## Descripción
Este proyecto es una animación gráfica interactiva en Python que muestra un capibara bailando al ritmo de una canción. Utiliza física básica para simular saltos y movimientos, incluye efectos visuales como confeti y sombras, y muestra las letras de la canción en estilo karaoke. El capibara está diseñado con detalles animados, incluyendo expresiones faciales y movimientos articulados.

## Características
- **Animación del Capibara**: Modelo detallado con cabeza, cuerpo, patas articuladas, orejas, bigotes y cola, animado con movimientos fluidos.
- **Física**: Simulación de gravedad, rebotes y límites para el movimiento del capibara.
- **Efectos Visuales**: Confeti cayendo, sombras dinámicas, césped animado y fondo cielo.
- **Reproducción de Audio**: Música de fondo usando winsound (solo en Windows).
- **Karaoke**: Letras sincronizadas con la canción, resaltando palabras en tiempo real.
- **Interacción**: Controles básicos (ESC para salir).

## Requisitos
- Python 3.x
- Librerías: Pygame, NumPy
- Sistema operativo: Windows (debido a winsound para audio)
- Archivo de audio: `capibara.wav` (debe estar en el mismo directorio)

## Instalación
1. Clona o descarga el repositorio.
2. Instala las dependencias:
   ```
   pip install pygame numpy
   ```
3. Asegúrate de que `capibara.wav` esté presente en el directorio del proyecto.

## Uso
Ejecuta el script principal:
```
python capibara.py
```
- La ventana gráfica se abrirá mostrando la animación.
- Presiona ESC para salir.
- Presiona S para detener el audio.

## Archivos
- `capibara.py`: Script principal con la lógica de animación y dibujo.
- `letra.txt`: Archivo de texto con las letras de la canción y marcadores de tiempo para instrumentales.
- `plan.md`: Documento con el plan detallado del proyecto, incluyendo diseño y pasos de implementación.
- `capibara.wav`: Archivo de audio de la canción (no incluido, debe proporcionarse).

## Cómo Funciona
El script carga las letras desde `letra.txt`, procesa eventos (letras o instrumentales) con duraciones. Usa un bucle principal para actualizar física, animar el capibara, dibujar elementos y sincronizar con el audio. El capibara se dibuja usando formas vectoriales en Pygame, con animaciones basadas en trigonometría y tiempo.

## Notas
- El audio usa winsound, que es específico de Windows. Para otros sistemas, modifica el código para usar otra librería como pygame.mixer.
- La animación está optimizada para 60 FPS.

## Autor
Andrey Rodríguez Araya