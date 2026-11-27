# Tokens de terminal-mono-ui

Fuente de verdad de los valores. `assets/theme.css` los implementa como custom properties
`--t-*`; `assets/DESIGN.template.md` los expone en YAML para agentes.

## Contenido
1. Color: roles y uso
2. Contraste verificado (WCAG)
3. Tipografía
4. Espacio y grilla
5. Forma
6. Movimiento
7. Métricas monoespaciadas (para cálculos de layout)

---

## 1. Color

Un solo acento (verde) señala **estado**: activo, foco, selección, resaltado, CTA principal.
Los demás colores son **semánticos**: si un color no significa algo, va en escala de grises verdosa.

| Token | Hex | Uso | No usar para |
|---|---|---|---|
| `primary` | `#37F712` | pestaña/botón activo, foco, nodo activo, líneas de código del paso, números del índice, marcas de esquina | texto de párrafo, decoración |
| `on-primary` | `#031003` | texto sobre fondo `primary` | — |
| `primary-hover` | `#7DFF63` | hover del botón primario | — |
| `secondary` | `#00A6F4` | enlaces, rutas en el prompt, info, modelo LLM grande | acciones |
| `warning` | `#FE9900` | avisos, decisiones, reintentos, fase/paso actual | errores |
| `danger` | `#FF2157` | errores, "antes", anti-señales, complejidad alta | estados neutros |
| `success` | `#00C24A` | nodos de salida/resultado | estado activo (eso es `primary`) |
| `surface-deep` | `#020403` | terminales, visor de código, inputs, placas de etiqueta | — |
| `surface` | `#050806` | fondo de página | — |
| `panel` | `#090E0A` | paneles, tarjetas, pestañas inactivas | — |
| `panel-high` | `#0D140E` | hover de panel, elementos internos (nodos, kbd) | — |
| `outline` | `#1B2A1D` | bordes por defecto, divisores de tabla | — |
| `outline-strong` | `#2B4430` | bordes punteados, hover, separadores `│` | — |
| `text` | `#D9E8D6` | texto principal, títulos | — |
| `text-2` | `#A3B3A0` | texto secundario, párrafos largos | — |
| `text-3` | `#7F907C` | metadatos, etiquetas, numeración de pestañas | párrafos |
| `text-faint` | `#4D5F4B` | **solo decorativo**: números de línea, timestamps del log | cualquier texto con información |

### Tipos de nodo (diagramas de agentes / flujos)

Se marcan con el **borde izquierdo de 4px** del nodo, nunca rellenando el fondo.

| Token | Hex | Tipo |
|---|---|---|
| `node-input` | `#8C9A89` | entrada / usuario / documento |
| `node-llm` | `#00A6F4` | llamada a LLM grande (p. ej. Sonnet) |
| `node-llm-light` | `#2DE2C5` | LLM rápido/barato (p. ej. Haiku) o paso genérico |
| `node-tool` | `#B47CFF` | herramienta, almacén, memoria |
| `node-human` | `#FF4FA3` | humano en el bucle, checkpoint |
| `node-decision` | `#FE9900` | router, decisión, evaluador |
| `node-output` | `#00C24A` | salida final |
| `edge` | `#2F4A33` | flechas inactivas (las activas usan `primary`) |

### Fondos tintados (estados de caja)

| Uso | Fondo | Borde |
|---|---|---|
| "antes" / error | `#140709` | `#5A1A26` |
| "después" / ok / "cuándo usar" | `#06140A` | `#1F5C2A` |
| nota / aviso | `#1D1608` | `#7A5A14` (punteado) |
| línea de código resaltada | `#0F2A10` | barra izquierda 3px `primary` |

Los bordes de badges usan el color del texto con alfa `55` (p. ej. `#00A6F455`).

## 2. Contraste verificado

Relación de contraste WCAG 2.x calculada sobre las tres superficies:

| Texto | surface `#050806` | panel `#090E0A` | panel-high `#0D140E` |
|---|---|---|---|
| primary | 13.87 | 13.42 | 12.88 |
| secondary | 7.44 | 7.19 | 6.91 |
| warning | 9.36 | 9.06 | 8.70 |
| danger | 5.37 | 5.20 | 4.99 |
| success | 8.45 | 8.17 | 7.85 |
| text | 15.77 | 15.26 | 14.65 |
| text-2 | 9.11 | 8.82 | 8.47 |
| text-3 | 5.92 | 5.73 | 5.50 |
| text-faint | **2.93** | 2.83 | 2.72 |
| on-primary sobre primary | 13.41 | | |

Todo pasa AA (≥ 4.5) salvo `text-faint`, reservado a información redundante o decorativa.
`danger` sobre `panel-high` queda en 4.99: no bajar más su tamaño de 11px.

## 3. Tipografía

Dos familias monoespaciadas, auto-hospedadas (OFL 1.1), sin dependencia de Google en tiempo de ejecución:

- **Space Mono** 400/700 → *display*: títulos, marca, números grandes. Personalidad.
- **JetBrains Mono** variable 400–700 → *texto*: todo lo demás. Legibilidad y alineación.

| Nivel | Familia | Tamaño | Peso | Interlineado | Extra |
|---|---|---|---|---|---|
| `display-hero` | Space Mono | `clamp(38px, 6.2vw, 76px)` | 700 | 0.98 | `letter-spacing:-2px`, 3 líneas con `<br>`, cursor de bloque |
| `headline-lg` | Space Mono | 22px | 700 | 1.2 | título de página de detalle |
| `headline-md` | Space Mono | 20px | 700 | 1.2 | encabezado de sección (`// 01`) |
| `headline-sm` | Space Mono | 17px | 700 | 1.3 | título dentro de panel |
| `brand` | Space Mono | 19px | 700 | 1 | nombre del producto |
| `stat` | Space Mono | 32px | 700 | 1.05 | números del índice |
| `body-md` | JetBrains Mono | 13px | 400 | 1.6 | base |
| `body-lg` | JetBrains Mono | 14px | 400 | 1.6 | párrafo introductorio (máx. 62ch) |
| `body-sm` | JetBrains Mono | 12–12.5px | 400 | 1.5 | listas, paneles densos |
| `label` | JetBrains Mono | 11–11.5px | 700 | 1.4 | MAYÚSCULAS, `letter-spacing:1.2px` (títulos de tarjeta, ptitle) |
| `label-sm` | JetBrains Mono | 10.5px | 400–700 | 1.4 | badges, etiquetas de flechas |
| `code` | JetBrains Mono | 11.5–12px | 400 | 1.55 | visor de código, log |
| `node-title` | JetBrains Mono | 12px | 700 | 17px | nodos de diagrama |
| `node-sub` | JetBrains Mono | 11px | 400 | 15px | subtítulo de nodo |
| `node-meta` | JetBrains Mono | 9.5px | 400 | 1.3 | modelo/tipo, MAYÚSCULAS |

Las fuentes se descargan en subset **latin** (incluye acentos del español). Ese subset **no trae
dibujo de cajas** (`┌ ─ │ ▶`): ver `ascii.md`.

## 4. Espacio y grilla

- Escala base 4px: `4 · 8 · 12 · 16 · 18 · 22 · 26 · 44`.
- Margen lateral de página: **22px**. Separación entre secciones: **44px**.
- Grilla de **12 columnas**, gap **18px**, columnas `minmax(0,1fr)` (nunca `1fr` a secas: un hijo
  con `min-width` grande —un SVG, un `<pre>`— estiraría la página).
- Composición **asimétrica**: 7+5, 5+7, 8+4. Evitar tres tarjetas iguales en fila.
- Por debajo de 980px la grilla colapsa a una columna (`minmax(0,1fr)` + `min-width:0` en los hijos).
- Densidad compacta: padding de panel 16×18, de pestaña 7×11, de badge 3×8.
- Área táctil mínima de botones: **44px** de alto (36px en la variante `is-sm` de controles).

## 5. Forma

- Radio **0** en todo: paneles, botones, pestañas, inputs, badges, chips, barras de progreso, puntos de paso.
- Excepciones: nodos de diagrama **2px**, logo **6px**, LED de estado circular.
- Sin sombras de elevación. La jerarquía se marca con **borde**, **tono de superficie** y
  **marcas de esquina** verdes (10×10px, 2px, esquina superior izquierda e inferior derecha).
- Únicos "brillos" permitidos: glow del LED, del nodo activo y del punto de flujo (`0 0 18px #37F71244`).

## 6. Movimiento

| Token | Duración | Curva | Uso |
|---|---|---|---|
| `state-change` | 120ms | ease | hover/foco de botones, pestañas, paneles |
| `cursor-blink` | 1100ms | `steps(1)` | cursor de bloque del título |
| `log-tick` | 560ms (900ms la primera línea) | lineal | una línea nueva del log simulado |
| `log-restart` | 4200ms | — | pausa antes de reiniciar el log |
| `step-autoplay` | 4200ms | — | avance automático de pasos en un reproductor |
| `flow-dot` | continuo | lineal | punto que recorre las flechas activas |

Todo movimiento debe **explicar algo** (un paso que avanza, un agente que trabaja). Con
`prefers-reduced-motion: reduce`: sin parpadeo, sin transiciones, el log se muestra completo de entrada.

## 7. Métricas monoespaciadas

En una fuente monoespaciada cada carácter mide **0.6 em**. Úsalo para dimensionar cajas de tamaño fijo
(nodos SVG, placas de etiqueta) sin medir en el navegador:

| Tamaño | Ancho por carácter | Recomendado (con margen) |
|---|---|---|
| 12px bold | 7.2px | 7.3 |
| 11px | 6.6px | 6.7 |
| 10.5px | 6.3px | 6.3 |

- Los emojis y símbolos anchos ocupan ~2 caracteres.
- Padding horizontal real de un nodo: `12 + 12 + 4 (borde izq.) + 1.5 (borde der.) = 29.5px`.
- Alto de nodo: `20 + 17·líneas_título + (15·líneas_sub + 4)`.
- Placa de etiqueta: `ancho = caracteres·6.3 + 18`, `alto = 8 + 13·líneas`, máximo ~23 caracteres por línea.
