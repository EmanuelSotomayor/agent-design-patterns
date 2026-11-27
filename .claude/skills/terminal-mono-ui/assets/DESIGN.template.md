---
version: alpha
name: NOMBRE DEL PRODUCTO · Terminal Mono
description: Sistema de diseño de estética terminal para PRODUCTO (completar). Monoespaciado, modo oscuro casi negro, un único acento verde que significa estado, paneles técnicos con marcas de esquina y diagramas de agentes con nodos tipados.
colors:
  primary: "#37F712"
  on-primary: "#031003"
  primary-hover: "#7DFF63"
  secondary: "#00A6F4"
  tertiary: "#FE9900"
  error: "#FF2157"
  surface: "#050806"
  surface-deep: "#020403"
  surface-container: "#090E0A"
  surface-container-high: "#0D140E"
  outline: "#1B2A1D"
  outline-strong: "#2B4430"
  on-surface: "#D9E8D6"
  on-surface-variant: "#A3B3A0"
  on-surface-muted: "#7F907C"
  on-surface-faint: "#4D5F4B"
  node:
    input: "#8C9A89"
    llm: "#00A6F4"
    llm-light: "#2DE2C5"
    tool: "#B47CFF"
    human: "#FF4FA3"
    decision: "#FE9900"
    output: "#00C24A"
    edge: "#2F4A33"
  tint:
    before-bg: "#140709"
    after-bg: "#06140A"
    note-bg: "#1D1608"
    note-text: "#FFD28A"
    code-highlight: "#0F2A10"
  syntax:
    keyword: "#00A6F4"
    string: "#9CFF7D"
    comment: "#5F7A5C"
    number: "#FE9900"
    call: "#2DE2C5"
typography:
  headline-lg:
    fontFamily: Space Mono
    fontSize: 22px
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: -0.2px
  headline-md:
    fontFamily: Space Mono
    fontSize: 20px
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: -0.3px
  headline-sm:
    fontFamily: Space Mono
    fontSize: 17px
    fontWeight: 700
    lineHeight: 1.3
  brand:
    fontFamily: Space Mono
    fontSize: 19px
    fontWeight: 700
    lineHeight: 1
  stat:
    fontFamily: Space Mono
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.05
  body-lg:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.5
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 11.5px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 1.2px
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 10.5px
    fontWeight: 700
    lineHeight: 1.4
  code:
    fontFamily: JetBrains Mono
    fontSize: 11.5px
    fontWeight: 400
    lineHeight: 1.55
  node-title:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: 700
    lineHeight: 17px
  node-sub:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: 400
    lineHeight: 15px
  display-hero-sm:
    fontFamily: Space Mono
    fontSize: 38px
    fontWeight: 700
    lineHeight: 0.98
    letterSpacing: -2px
  display-hero-lg:
    fontFamily: Space Mono
    fontSize: 76px
    fontWeight: 700
    lineHeight: 0.98
    letterSpacing: -2px
rounded:
  none: 0px
  node: 2px
  logo: 6px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  panel-x: 18px
  gutter: 18px
  page-margin: 22px
  xl: 26px
  section: 44px
  columns: 12
  touch-target: 44px
  collapse-breakpoint: 980px
motion:
  state-change:
    duration: 120ms
    delay: 0ms
    timingFunction: ease
  cursor-blink:
    duration: 1100ms
    delay: 0ms
    timingFunction: steps(1)
  log-tick:
    duration: 560ms
    delay: 0ms
    timingFunction: linear
  step-autoplay:
    duration: 4200ms
    delay: 0ms
    timingFunction: linear
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.none}"
    padding: 11px
    height: 44px
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.on-primary}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.none}"
    padding: 11px
    height: 44px
  button-secondary-hover:
    textColor: "{colors.primary}"
  tab:
    backgroundColor: "{colors.surface-container}"
    textColor: "{colors.on-surface-variant}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.none}"
    padding: 7px
  tab-active:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  panel:
    backgroundColor: "{colors.surface-container}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.none}"
    padding: 16px
  panel-hover:
    backgroundColor: "{colors.surface-container-high}"
  input:
    backgroundColor: "{colors.surface-deep}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.none}"
    padding: 10px
  badge:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.secondary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.none}"
    padding: 3px
  code-viewer:
    backgroundColor: "{colors.surface-deep}"
    textColor: "{colors.on-surface}"
    typography: "{typography.code}"
    rounded: "{rounded.none}"
  code-line-active:
    backgroundColor: "{colors.tint.code-highlight}"
    textColor: "{colors.primary}"
  terminal-log:
    backgroundColor: "{colors.surface-deep}"
    textColor: "{colors.on-surface-variant}"
    typography: "{typography.code}"
    rounded: "{rounded.none}"
    padding: 12px
  diagram-node:
    backgroundColor: "{colors.surface-container-high}"
    textColor: "{colors.on-surface}"
    typography: "{typography.node-title}"
    rounded: "{rounded.node}"
    padding: 8px
  diagram-node-active:
    textColor: "{colors.primary}"
  edge-label:
    backgroundColor: "{colors.surface-deep}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.node}"
    height: 20px
  state-before:
    backgroundColor: "{colors.tint.before-bg}"
    textColor: "{colors.error}"
  state-after:
    backgroundColor: "{colors.tint.after-bg}"
    textColor: "{colors.primary}"
  hero-title:
    textColor: "{colors.on-surface}"
    typography: "{typography.display-hero-lg}"
  hero-title-mobile:
    typography: "{typography.display-hero-sm}"
  metadata:
    textColor: "{colors.on-surface-muted}"
    typography: "{typography.label-sm}"
  line-number:
    textColor: "{colors.on-surface-faint}"
    typography: "{typography.code}"
  section-rule:
    backgroundColor: "{colors.outline-strong}"
    height: 1px
  diagram-edge:
    backgroundColor: "{colors.node.edge}"
    height: 2px
  diagram-edge-active:
    backgroundColor: "{colors.primary}"
  diagram-note:
    backgroundColor: "{colors.tint.note-bg}"
    textColor: "{colors.tint.note-text}"
    typography: "{typography.node-sub}"
    rounded: "{rounded.node}"
  legend-swatch-input:
    backgroundColor: "{colors.node.input}"
    size: 10px
  legend-swatch-llm:
    backgroundColor: "{colors.node.llm}"
    size: 10px
  legend-swatch-llm-light:
    backgroundColor: "{colors.node.llm-light}"
    size: 10px
  legend-swatch-tool:
    backgroundColor: "{colors.node.tool}"
    size: 10px
  legend-swatch-human:
    backgroundColor: "{colors.node.human}"
    size: 10px
  legend-swatch-decision:
    backgroundColor: "{colors.node.decision}"
    size: 10px
  legend-swatch-output:
    backgroundColor: "{colors.node.output}"
    size: 10px
  syntax-keyword:
    textColor: "{colors.syntax.keyword}"
  syntax-string:
    textColor: "{colors.syntax.string}"
  syntax-comment:
    textColor: "{colors.syntax.comment}"
  syntax-number:
    textColor: "{colors.syntax.number}"
  syntax-call:
    textColor: "{colors.syntax.call}"
---

# NOMBRE DEL PRODUCTO · Terminal Mono

> Plantilla de la skill **terminal-mono-ui**. Para usarla: copiá `theme.css`, `components.html` y la
> carpeta `fonts/` de la skill a `design/` en la raíz del proyecto, guardá este archivo como `DESIGN.md`
> y reemplazá todo lo marcado como **COMPLETAR** o *(ejemplo)*. Los encabezados quedan en inglés porque
> son los nombres canónicos de la especificación DESIGN.md; el contenido puede ir en el idioma del producto.
> Implementación: `@design/theme.css` · componentes: `@design/components.html`.

## Overview

**COMPLETAR:** qué es el producto y quién lo usa, en dos o tres frases. El estilo lo presenta como una
**herramienta de ingeniería en ejecución**: una terminal con paneles. Funciona mejor con audiencias
técnicas que valoran precisión y transparencia, y con productos que pueden "mostrarse funcionando"
(procesos, agentes, pipelines, datos).

- **Personalidad:** precisa, densa, calma, honesta. Hacker, no gamer; técnica, no fría.
- **Metáfora única:** la terminal. Prompts, comandos, logs, árboles de archivos, comentarios de código.
  No se mezcla con otras metáforas (nada de glassmorphism, ilustraciones ni iconos de colores).
- **Anti-plantilla:** composición asimétrica, sin hero centrado con tres tarjetas iguales, sin
  degradados, sin esquinas redondeadas, sin emojis.
- **Regla de oro:** un solo color de acento (verde) y significa *estado*. Todo lo demás es tono.

## Colors

Fondo casi negro con un tinte verde imperceptible, para que el acento verde se sienta parte del mismo
material. Cuatro niveles de superficie construyen la jerarquía sin sombras.

- **Primary — Verde fósforo (#37F712):** el único acento. Pestaña y botón activos, foco, selección,
  nodo y flecha activos, líneas de código del paso actual, números del índice y marcas de esquina de los
  paneles. Nunca en párrafos ni como decoración. Contraste 13.9:1 sobre el fondo.
- **On-primary (#031003):** texto sobre verde (13.4:1).
- **Secondary — Azul señal (#00A6F4):** enlaces, rutas del prompt, badges de modelo, LLM grande en
  diagramas, keywords de código.
- **Tertiary — Ámbar (#FE9900):** avisos, reintentos, decisiones/routers y la fase actual en la tarjeta
  de paso.
- **Error — Rojo alarma (#FF2157):** errores, el estado "antes", anti-señales, complejidad alta (5.4:1:
  no usar por debajo de 11px).
- **Verde salida (#00C24A, `node.output`):** nodos de salida/resultado. Distinto del primary a propósito:
  el primary es "activo", este es "terminado".
- **Superficies:** `surface-deep` #020403 (terminales, código, inputs) → `surface` #050806 (página) →
  `surface-container` #090E0A (paneles) → `surface-container-high` #0D140E (hover y elementos internos).
- **Bordes:** `outline` #1B2A1D por defecto, `outline-strong` #2B4430 en hover, punteados y separadores.
- **Texto:** `on-surface` #D9E8D6 (15.8:1), `on-surface-variant` #A3B3A0 (9.1:1) para párrafos largos,
  `on-surface-muted` #7F907C (5.9:1) para metadatos, `on-surface-faint` #4D5F4B (2.9:1) **solo
  decorativo** (números de línea, timestamps).
- **Tipos de nodo (`node.*`):** se aplican solo como borde izquierdo de 4px del nodo: entrada gris,
  LLM grande azul, LLM liviano turquesa, herramienta/memoria violeta, humano rosa, decisión ámbar,
  salida verde. Flechas inactivas #2F4A33.
- **Tintes (`tint.*`):** fondos de estado para "antes" (rojo muy oscuro, borde #5A1A26), "después"
  (verde muy oscuro, borde #1F5C2A), notas (ámbar oscuro con texto #FFD28A y borde punteado #7A5A14) y la
  línea de código resaltada. Los bordes de badges usan el color de su texto al 33% de opacidad.

## Typography

Dos monoespaciadas auto-hospedadas (licencia OFL, subset latin), cargadas con `font-display: swap`
desde archivos locales, sin llamadas a Google en tiempo de ejecución.

- **Space Mono 700** para títulos, marca y números grandes: geométrica y con carácter.
- **JetBrains Mono (variable 400–700)** para todo el resto: diseñada para leer código, alinea columnas.
- **Display hero:** 38px (móvil) a 76px (escritorio), interlineado 0.98, tracking -2px, en tres
  líneas con `<br>`, última palabra en primary y un cursor de bloque al final.
- **Labels:** 11–11.5px en MAYÚSCULAS con 1.2px de tracking para títulos de tarjeta (`// TÍTULO`) y
  cabeceras de panel.
- **Base:** 13px/1.6. Párrafos introductorios 14px con ancho máximo de 62 caracteres.
- **Métrica clave:** cada carácter mide 0.6 em (7.2px a 12px, 6.6px a 11px, 6.3px a 10.5px). Los
  tamaños fijos (nodos de diagrama, placas de etiqueta) se calculan con esto; emojis cuentan doble.
- El subset latin **no incluye caracteres de dibujo de cajas**: los diagramas de texto alineados se
  escriben en ASCII puro (`+--`, `|`, `-->`).

## Layout

- Grilla de **12 columnas** con columnas `minmax(0, 1fr)` y gap de 18px; margen de página 22px;
  44px entre secciones.
- **Asimetría deliberada:** paneles en 7+5, 5+7 u 8+4 columnas; el hero es 7 (texto) + 5 (terminal).
- Debajo de 980px todo colapsa a una columna. Ningún hijo puede ensanchar la página: los elementos
  anchos (mapas SVG con ancho mínimo de 1000px para seguir legibles, código, árboles, figuras ASCII)
  hacen scroll horizontal **dentro de su marco**.
- **Navegación:** marca `>_` + pestañas en una o varias filas (nunca menú hamburguesa) + barra de ruta
  tipo prompt en cada vista: `visitante@app:~/seccion/elemento$ ./comando --descriptivo`.
- *(ejemplo)* **Vista de detalle con proceso:** diagrama animado a todo el ancho → [tarjeta del paso |
  código o datos] → paneles de contexto. **COMPLETAR** con las vistas del producto.
- *(ejemplo)* **Catálogo:** grupo (`## Grupo`) → categoría (`> Categoría`) → grilla de fichas; chips para
  saltar entre grupos; detalle con `[1] resumen` / `[2] visualización del flujo`.
- Densidad compacta: padding de panel 16×18, de pestaña 7×11, de badge 3×8.

## Elevation & Depth

Sin sombras. La profundidad se construye con:

1. **Tono de superficie** (4 niveles casi negros, de `surface-deep` a `surface-container-high`).
2. **Bordes de 1px**, más claros en hover; punteados para separadores internos.
3. **Marcas de esquina:** dos escuadras verdes de 10×10px y 2px en las esquinas superior izquierda e
   inferior derecha de cada panel principal. Son la firma del sistema y dicen "esto es un módulo".
   No se anidan: dentro de un panel, las cajas son planas.
4. **Glow** solo donde hay estado vivo: el LED de la barra de estado, el nodo activo
   (`0 0 0 1px primary, 0 0 18px` verde al 27%) y el punto que recorre las flechas activas.

## Shapes

Arquitectura recta: **radio 0** en paneles, botones, pestañas, inputs, badges, chips, barras de
progreso y puntos de paso (cuadrados). Excepciones mínimas: nodos de diagrama con 2px (para separarlos
visualmente de los paneles), el logo `>_` con 6px y el LED de estado circular. Las flechas de los
diagramas terminan exactamente en el borde del nodo, con punta triangular.

## Motion & Micro-interaction

Todo movimiento explica algo; nada se mueve por decoración.

- **Cambios de estado** (hover/foco): 120ms ease, solo color, borde y fondo. Sin `transform` en hover.
- **Cursor de bloque:** parpadeo de 1.1s con `steps(1)`.
- **Log de agente simulado:** una línea cada 560ms (900ms la primera), pausa de 4.2s y reinicio. Con
  botón de pausa (`aria-pressed`). Muestra cómo trabaja un agente (plan, fan-out, reintento, evaluación,
  aprobación humana).
- **Reproductor de pasos:** avance automático cada 4.2s; al cambiar de paso se iluminan nodos y
  flechas, un punto recorre las flechas activas y el visor de código hace scroll a las líneas del paso.
- **Movimiento reducido:** con `prefers-reduced-motion: reduce` no hay parpadeo ni transiciones y el log
  aparece completo desde el inicio.

## Voice & Content Strategy

- **Tono:** preciso, calmo, didáctico. Sin signos de exclamación ni lenguaje de marketing.
- **Idioma:** **COMPLETAR** (p. ej. español neutro con tuteo). Los **nombres propios** de productos,
  técnicas y protocolos quedan en su idioma original; las descripciones se traducen.
- **Terminología:** **COMPLETAR** con los nombres canónicos de los conceptos del producto y sus sinónimos
  prohibidos.
- **Mayúsculas:** tipo oración en títulos; minúsculas en botones, comandos y pestañas de detalle;
  MAYÚSCULAS solo en labels de tarjeta y barra de estado.
- **Marcadores en vez de iconos:** `[01]` número de patrón, `// 01` sección, `## grupo`, `> categoría`,
  `<< antes` / `>> después`, `$ cat archivo.py`, `[resumen]`, `+` / `-` en listas, `»` para pistas,
  `etiqueta: valor` en badges (`modelo: Sonnet 4.6`, `tool: web_search`, `evento: step_start`).
- **Botones:** verbo + objeto con atajo opcional: `[↵] empezar por el patrón 01`, `[/] abrir la biblioteca`.
- **Comandos ficticios** descriptivos y verosímiles: `./explorar --modo=aprendizaje`, `ls --agrupar`,
  `cat resumen.md`, `./reproducir --flujo`.
- **Cifras** siempre calculadas desde los datos; números con separador de miles local (`2.734`).
- **Vacíos y errores:** decir qué pasó y qué hacer (`Sin resultados.` + sugerencia; `La fuente original
  de este patrón no incluye un diagrama de flujo. Revisa la pestaña Resumen.`).

## Components

Implementación canónica en `@design/components.html`, con marcadores `<!-- COMPONENT: nombre -->`;
clases con prefijo `t-` en `@design/theme.css`.

- **Brand:** `>_` verde en caja 38×38 + nombre en Space Mono 19px; enlaza a la home.
- **Tabs (menú principal):** `~ Inicio`, `≡ Visión general`, `01 … NN` ítems numerados, `/ Catálogo`. Activa en
  verde invertido con `aria-current="page"`.
- **Pathbar:** prompt `usuario@app:~/ruta$ comando` en cada vista salvo la home.
- **Status bar:** borde izquierdo verde, LED, `SISTEMA EN LÍNEA`, cifras separadas por `│`.
- **Panel:** `surface-container`, borde 1px, marcas de esquina; variante enlazable con foco y Enter.
- **Section header:** `// 01  Título ───── meta`.
- **Buttons:** primario verde (uno por vista) y secundario transparente con borde; 44px de alto.
- **Badges, chips, segmented, detail-tabs, input:** radio 0, borde del color de su rol.
- **Terminal log:** ventana con barra `□ □ □ archivo.log`, timestamps tenues y categorías coloreadas;
  el contenido simula el proceso real del producto.
- **Code viewer:** archivo completo numerado (`$ cat archivo.py · N líneas`), líneas del paso con fondo
  verde oscuro, número verde y barra izquierda de 3px.
- **Before/after:** `<< antes de la acción` en rojo y `>> después de la acción` en verde, con el estado
  concreto de los datos.
- **Diagrama de agente:** nodos en `foreignObject` (título 12px, subtítulo 11px, modelo 9.5px en
  mayúsculas), borde izquierdo por tipo de nodo, flechas recortadas al borde con punta, etiquetas en
  placas ubicadas en el tramo libre más largo (≥ 6px de aire), bucles por encima o por debajo de la fila,
  idas y vueltas en paralelo. Diagramas de secuencia con participantes, líneas de vida punteadas,
  notas ámbar y marcos `loop`/`alt`.
- **Player controls:** `⏮ ◀ ▶ reproducir ▶ ⏭`, barra de progreso verde, `Paso N de M`, puntos
  cuadrados; teclado `← → Espacio`; clic en un nodo salta a su paso.
- **Stats, tree y keys:** índice numérico en celdas, taxonomía como salida de `$ tree` (las carpetas
  navegan), tabla de atajos con `<kbd>`.

## Do's and Don'ts

- Do usar el verde solo para estado (activo, foco, selección, resaltado) y para un único CTA por vista.
- Don't usar emojis ni iconos de colores en la interfaz; si vienen en los datos, quitarlos al renderizar.
- Do construir jerarquía con tono de superficie, bordes y marcas de esquina.
- Don't usar sombras de elevación, degradados ni esquinas redondeadas (salvo nodos 2px, logo 6px, LED).
- Do calcular los tamaños fijos con la métrica de 0.6 em y verificar que ningún texto se recorte.
- Don't usar `┌ ─ │ ▶` en figuras que deban alinearse; usar ASCII puro.
- Do usar columnas `minmax(0, 1fr)` y scroll interno para todo contenido ancho.
- Don't dejar que un mapa, un `<pre>` o el visor de código ensanchen la página en móvil.
- Do mostrar la ubicación con el prompt de ruta y las cifras calculadas desde los datos.
- Don't animar nada que no explique un proceso; respetar `prefers-reduced-motion`.
- Do mantener contraste ≥ 4.5:1 en todo texto informativo; `on-surface-faint` solo para lo decorativo.
- Don't mezclar metáforas visuales: todo es terminal.
