# Plan para Animación de Capibara Bailando

## Objetivo
Crear un script en Python (`capibara.py`) que muestre una animación gráfica de un capibara bailando, utilizando física, matemática avanzada, múltiples capas vectoriales y un estilo de dibujo animado.

## Requisitos
- Python 3.x instalado
- Librerías recomendadas: Pygame (para gráficos 2D y animaciones), NumPy (para cálculos matemáticos avanzados y vectores), opcionalmente Matplotlib para visualizaciones complejas o Pymunk para física 2D.
- Se ejecuta en una ventana gráfica.

## Componentes Detallados del Capibara
Para hacer el capibara mucho más detallado y realista, dividirlo en múltiples capas vectoriales avanzadas con animación compleja, inspirado en dibujos animados con expresiones y movimientos fluidos:

- **Cabeza**: Elipse base redondeada con sombreado para volumen 3D simulado, incluyendo contorno suave.
- **Ojos**: Dos círculos para globos oculares con pupilas centrales (círculos más pequeños), cejas arqueadas (líneas curvas) que se mueven para expresiones (sorprendido, feliz), y posibilidad de parpadeo (cerrar temporalmente).
- **Nariz**: Triángulo pequeño o corazón para forma adorable, con sombras para profundidad.
- **Boca**: Curva parabólica para sonrisa, con dientes pequeños (líneas verticales) visibles al abrir, y animación de habla o risa (cambio de forma).
- **Orejas**: Dos elipses semicirculares con interior rosado, moviéndose sutilmente (rotación ligera) para expresar emoción.
- **Bigotes**: Varias líneas finas saliendo de la nariz, ondulándose con el movimiento para realismo.
- **Cuerpo**: Elipse grande con textura de pelaje (líneas curvas paralelas para pelo), manchas marrones oscuras distribuidas aleatoriamente, y sombreado para curvas.
- **Patas Delanteras**: Dos segmentos articulados (hombro, codo, mano) dibujados como líneas conectadas, con "manos" como círculos pequeños; animación de baile con levantamiento, giro y balanceo usando trigonometría.
- **Patas Traseras**: Similar a las delanteras pero más musculosas, con énfasis en saltos (extensión y contracción), articulaciones para rodillas y pies.
- **Cola**: Serie de elipses conectadas en curva sinusoidal, con pelo en el extremo (líneas radiales), moviéndose como un látigo durante el baile.
- **Detalles Adicionales**: Mejillas rosadas (círculos suaves), gotas de sudor durante el esfuerzo, expresiones faciales cambiantes (ojos más grandes para sorpresa), pelo erizado en la espalda, y accesorios como un sombrero pequeño o gafas para estilo animado.
- **Efectos Especiales**: Partículas de polvo o estrellas alrededor para énfasis en movimientos, sombras dinámicas que siguen el capibara, y transiciones suaves entre poses.

Cada componente se dibujará usando vectores avanzados (polígonos, splines, gradientes) y se animará con transformaciones matemáticas complejas (matrices de rotación, escalado no uniforme, interpolación de curvas para movimientos naturales).

## Pasos de Implementación (Checklist)
- [x] **Configurar Entorno**: Instalar Pygame, NumPy y configurar entorno virtual Python.
- [x] **Inicializar Ventana**: Crear ventana con Pygame (800x600), configurar colores (negro, blanco, marrón, verde), reloj para 60 FPS.
- [x] **Definir Vectores Base**: Crear arrays NumPy para posiciones (float), velocidades (float) y fuerzas físicas (gravedad, etc.).
- [x] **Diseñar Cabeza**: Dibujar elipse base redondeada con sombreado para volumen.
- [x] **Agregar Ojos**: Dibujar círculos para globos oculares, pupilas centrales, cejas arqueadas con movimiento.
- [x] **Agregar Nariz**: Dibujar triángulo o corazón pequeño con sombras.
- [x] **Agregar Boca**: Dibujar curva parabólica para sonrisa, con dientes y animación de apertura.
- [x] **Agregar Orejas**: Dibujar elipses semicirculares con interior rosado y movimiento sutil.
- [x] **Agregar Bigotes**: Dibujar líneas finas ondulantes desde la nariz.
- [x] **Diseñar Cuerpo**: Dibujar elipse grande con textura de pelaje (líneas curvas), manchas marrones y sombreado.
- [x] **Diseñar Patas Delanteras**: Dibujar segmentos articulados (hombro, codo, mano) con círculos para "manos", animación de baile.
- [x] **Diseñar Patas Traseras**: Dibujar segmentos similares con énfasis en saltos y articulaciones.
- [x] **Diseñar Cola**: Dibujar serie de elipses en curva sinusoidal con pelo en el extremo.
- [x] **Agregar Detalles Adicionales**: Dibujar mejillas rosadas, expresiones cambiantes, pelo erizado, accesorios.
- [x] **Implementar Física**: Aplicar gravedad (vector [0, 0.5]), velocidad, rebotes en suelo/paredes usando ecuaciones.
- [x] **Agregar Animación**: Usar delta time para movimientos suaves, rotaciones con trigonometría, escalas con álgebra lineal.
- [x] **Capas y Profundidad**: Dibujar componentes en orden correcto (fondo: cuerpo, frente: cabeza) para efecto de capas.
- [x] **Efectos Especiales**: Agregar partículas de polvo, sombras dinámicas, transiciones entre poses.
- [x] **Interacción de Usuario**: Manejar eventos de teclado (ESC para salir) y cierre de ventana.
- [x] **Optimización**: Asegurar 60 FPS, manejar memoria eficientemente, evitar lag.
- [x] **Pruebas**: Ejecutar script, verificar animación fluida, física correcta, expresiones, y cierre sin errores.

## Salida Esperada
- Una animación gráfica en una ventana mostrando un capibara bailando con movimientos realistas basados en física.
- Salida elegante al cerrar la ventana.

## Pruebas
- Ejecutar el script y verificar que la animación sea suave y responda a la física.
- Probar cierre de la ventana y posibles errores.

## Recomendaciones de Librerías Gráficas
- **Pygame**: Ideal para animaciones 2D con física simple. Fácil de usar para dibujar formas, manejar eventos y crear bucles de juego.
- **NumPy**: Para cálculos vectoriales y matemáticos avanzados (e.g., rotaciones, fuerzas).
- **Pymunk**: Para simulaciones de física más complejas (colisiones, cuerpos rígidos).
- **Matplotlib**: Si se quiere integrar gráficos científicos, pero menos adecuado para animaciones en tiempo real.
- **Arcade**: Alternativa a Pygame con mejor rendimiento para juegos 2D.

## Consejos y Técnicas para Diseñar por Código
Diseñar gráficos complejos como el capibara sin un diseñador requiere un enfoque sistemático. Aquí van técnicas prácticas para simplificar el proceso y lograr resultados profesionales:

1. **Empieza con Bocetos Simples**: Antes de codificar, imagina o dibuja a mano el capibara dividido en partes básicas (cabeza como elipse, cuerpo como círculo, patas como líneas). Usa proporciones simples (e.g., cabeza 1/3 del cuerpo). Busca imágenes de capibaras para inspiración y adapta formas geométricas.

2. **Construye con Formas Básicas y Vectores**: Usa `pygame.draw` (círculos, elipses, líneas, polígonos) para todo. Define posiciones con NumPy arrays (e.g., `head_pos = body_pos + np.array([0, -40])`). Calcula posiciones relativas y usa trigonometría para curvas (e.g., cola sinusoidal con `np.sin(t)`).

3. **Agrega Detalles Paso a Paso (Iteración)**: No intentes todo de golpe. Agrega un detalle a la vez (primero cuerpo, luego ojos). Crea funciones modulares como `draw_head(pos)` para reutilizar. Usa toggles (e.g., `show_whiskers = True`) para activar/desactivar partes en pruebas. Ejecuta frecuentemente y ajusta números (e.g., tamaño de ojos).

4. **Simula Efectos Visuales con Código**: Para sombreado, usa líneas/arcos superpuestos. Para texturas (pelaje), dibuja líneas curvas paralelas. Anima con `time_elapsed` para interpolación (e.g., `angle = time_elapsed * speed`). Cambia expresiones basadas en tiempo (e.g., ojos más grandes cada 2 segundos).

5. **Maneja Física y Movimiento con Matemáticas**: Usa vectores para gravedad (`velocity += gravity * dt`), rebotes (`velocity[1] *= -0.8`). Para articulaciones, calcula puntos con trigonometría (e.g., `elbow = shoulder + length * np.array([np.cos(angle), np.sin(angle)])`). Estudia rotaciones con matrices NumPy.

6. **Herramientas y Librerías Auxiliares**: Instala `pygame.gfxdraw` para formas suaves o `pygame.surfarray` para manipular píxeles. Mira ejemplos en pygame.org o GitHub. Considera Turtle para principiantes o Arcade para más rendimiento.

7. **Optimización y Debugging**: Limita FPS a 60, usa sprites para grupos. Mide tiempo con `pygame.time.get_ticks()`. Agrega marcadores visuales (e.g., `pygame.draw.circle(screen, RED, pos, 5)`) para debuggear posiciones. Usa debugger de VS Code.

8. **Inspiración y Mejora Continua**: Estudia juegos simples (e.g., Pong) para sprites. Crea un "modo debug" con grids. Practica con formas simples primero. Recuerda: es iterativo – dibuja, prueba, ajusta, repite.