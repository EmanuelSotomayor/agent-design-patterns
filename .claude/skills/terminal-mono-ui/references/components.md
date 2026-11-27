# Componentes de terminal-mono-ui

Cada componente tiene un ejemplo funcional en `assets/components.html`, marcado con
`<!-- COMPONENT: nombre -->`. Copiá el HTML de ahí; esta guía explica anatomía, estados y por qué.

## Contenido
- Navegación: brand · tabs · pathbar · status-bar
- Estructura: section-header · panel · card-title · grid asimétrica
- Acciones: botones · chips · segmented · detail-tabs · input
- Datos: badges · stats · tree · keys · listas +/- · before-after
- Terminal y código: terminal-log · code-viewer
- Diagramas: nodos · flechas · etiquetas · player-controls
- Hero de landing

---

## Navegación

### brand
`>_` en caja 38×38 (borde `outline-strong`, radio 6px, verde) + nombre en Space Mono 19px.
Es un enlace a la home. Sin logo gráfico: el prompt **es** el logo.

### tabs — menú principal
- Texto: `<span class="t-n">MARCA</span>Etiqueta`. Marcas: `~` inicio, `≡` visión general,
  `01..NN` ítems numerados con cero a la izquierda, `/` biblioteca o búsqueda.
- Estado activo: **fondo verde invertido** (`primary` + `on-primary`). Marcar con `aria-current="page"`.
- Hover: borde `outline-strong`, texto `text`.
- Envuelven en varias filas (`flex-wrap`): no esconder ítems en menús hamburguesa.

### pathbar — prompt de ubicación
`usuario@app:~/ruta/actual$ comando-que-describe-la-vista`
- `usuario@app` en `primary`, ruta en `secondary`, comando en `text-3`.
- La ruta refleja la jerarquía real (grupo/categoría/elemento, en slugs). El comando dice qué hace la
  vista: `ls` (lista), `cat resumen.md` (lectura), `./ejecutar --paso-a-paso` (animación),
  `./reproducir --flujo`.
- Va arriba del contenido de cada vista excepto la home (que tiene su propio prompt en el hero).
- Una sola línea con `text-overflow:ellipsis`.

### status-bar
Borde izquierdo de 3px `primary`, LED verde con glow, `ETIQUETA EN MAYÚSCULAS` en `text`,
separadores `│` en `outline-strong`, y a la derecha metadatos en `text-3`.
**Las cifras se calculan desde los datos**, nunca se escriben a mano.

## Estructura

### section-header
`// 01  Título ─────────(línea punteada)──────── meta`
Número en `primary`, título Space Mono 20px, regla punteada flexible, meta a la derecha en 11px.

### panel
- Fondo `panel`, borde 1px `outline`, padding 16×18, radio 0.
- **Marcas de esquina**: pseudo-elementos 10×10 con borde de 2px `primary` arriba-izquierda y
  abajo-derecha. Son la firma visual del sistema: identifican "esto es un módulo".
- `t-ptitle`: cabecera interna en MAYÚSCULAS 11px, `[01]`/`$ comando` en `primary`, meta a la derecha,
  línea punteada debajo.
- Variante enlazable (`is-link`): `tabindex="0"`, `role="link"`, Enter activa; hover eleva el fondo a `panel-high`.
- No anidar paneles con marcas: dentro de un panel usar cajas planas (`panel-high` + borde `outline`).

### card-title
Título de tarjeta como comentario de código: `// TÍTULO` en 11.5px MAYÚSCULAS, `//` verde, texto `text-3`.

### grid asimétrica
12 columnas `minmax(0,1fr)`; combinar spans distintos por fila (7+5, 5+7). Colapsa a 1 columna < 980px.

## Acciones

### botones
| Variante | Estilo | Uso |
|---|---|---|
| `is-primary` | fondo verde, texto `on-primary` | **una** acción principal por vista |
| (por defecto) | transparente, borde `outline-strong` | acciones secundarias |
| `is-sm` | 12px, alto 36px | controles de reproducción |
Prefijo opcional de tecla `[↵]`, `[≡]`, `[/]` con opacidad .7. Etiqueta en minúscula, verbo + objeto:
"empezar por el patrón 01", "abrir la biblioteca". Hover: borde y texto verdes. Disabled: opacidad .4.

### chips
Filtros/atajos de navegación. Borde `outline-strong`, contador en `<small>` `text-3`, hover verde.

### segmented
Alterna fuentes o modos. Opción activa en verde invertido, igual que las pestañas.

### detail-tabs
`[1] resumen  [2] visualización del flujo` — subrayado verde de 2px en la activa, línea punteada base.

### input
Fondo `surface-deep`, borde `outline-strong`, foco con borde `primary`. Placeholder en `text-3`.

## Datos

### badges
Formato `etiqueta: valor` en vez de iconos: `modelo: Sonnet 4.6`, `tool: web_search`, `evento: step_start`.
Color por rol (info azul, tool violeta, ok verde, warn naranja, err rojo), fondo transparente,
borde del mismo color con alfa 55.

### stats (índice numérico)
Celdas en grilla con bordes compartidos, número Space Mono 32px verde, etiqueta en MAYÚSCULAS 11px.

### tree
Salida de `$ tree`: carpeta en negrita `text`, ramas `├──`/`└──` en `outline-strong`,
hojas en `secondary`, contadores y comentarios `# ...` en `text-3`. Con `overflow-x:auto`.
Las carpetas pueden ser botones que navegan a esa sección.

### keys
Tabla de atajos: `<kbd>` con borde inferior de 2px, descripción en `text-2`, filas separadas por línea punteada.

### listas +/-
`t-list-ok` con marcador `+ ` verde y `t-list-bad` con `- ` rojo. Reemplazan ✅/❌.

### before-after
Dos cajas lado a lado: `<< antes de la acción` (rojo) y `>> después de la acción` (verde).
Muestran el **estado de los datos** alrededor de una acción, no adjetivos.

## Terminal y código

### terminal-log
Ventana con barra (`□ □ □` en cuadrados, nombre de archivo, descripción, botón pausa) y un `<pre>`.
Líneas: `[ts]` en `text-faint`, `[categoría]` coloreada (`ok` verde, `in` azul, `wr` naranja, `er` rojo),
mensaje en `text-2`, comando inicial `$ ...` en negrita `text`.
Si se anima: una línea cada 560ms, pausa de 4.2s y reinicio, botón pausa con `aria-pressed`,
y con movimiento reducido se muestra completo y sin botón. El contenido debe **simular el dominio real**
(p. ej. la ejecución de un agente), no texto de relleno.

### code-viewer
- Archivo completo con números de línea (44px, alineados a la derecha, `text-faint`, borde derecho).
- Encabezado `$ cat <b>archivo.py</b> · N líneas`.
- Líneas activas: fondo `#0F2A10`, número verde en negrita, barra izquierda de 3px verde; al cambiar de
  paso, hacer scroll hasta la primera línea resaltada.
- Sintaxis: keywords azul, strings verde claro `#9CFF7D`, comentarios `#5F7A5C` itálica,
  números/decoradores naranja, llamadas a `self.*` turquesa.

## Diagramas

### nodo (`t-node`, dentro de `<foreignObject>`)
Título 12px negrita, subtítulo 11px, meta 9.5px MAYÚSCULAS (p. ej. el modelo). Borde izquierdo de 4px
por tipo (ver tokens). Activo: borde y halo verde, título verde. Nota: fondo ámbar oscuro y borde punteado.
Sin iconos ni emojis dentro del nodo: el tipo lo dice el color del borde y la leyenda.
El tamaño se calcula con las métricas monoespaciadas (`tokens.md` §7) para que nada se recorte.

### flechas
`stroke:#2F4A33`, 2px, punta de flecha por `marker-end`. Activa: verde, 2.6px, punta verde.
Deben **terminar en el borde del nodo** (recortar la recta contra el rectángulo), no en su centro.
Bucles por encima/debajo de la fila; flechas de ida y vuelta en paralelo, desplazadas ±16–26px.

### etiqueta de flecha
Placa `surface-deep` con borde `outline-strong` y radio 2px, texto 10.5px negrita. Ubicarla en el tramo
libre más largo de la flecha, con ≥ 6px de aire respecto de cualquier nodo. Partir en dos líneas si pasa
de ~23 caracteres.

### punto de flujo
Círculo r=4 `#DFFFD6` con glow verde que recorre las flechas activas del paso actual.

### player-controls
`⏮ ◀ [▶ reproducir] ▶ ⏭` (reproducir en `is-primary`), barra de progreso verde clicable,
`Paso N de M`, y fila de puntos cuadrados (hecho = verde oscuro, actual = verde con outline).
Teclado: `←` `→` y `Espacio`. Clic en un nodo salta al primer paso donde participa.

## Hero de landing
Grilla 7+5: a la izquierda prompt `visitante@app:~$ ./explorar --modo=...`, título display en tres
líneas con la última palabra en verde y cursor de bloque, uno o dos párrafos (máx. 62ch) y 2–3 botones
(uno primario). A la derecha, un `terminal-log` que muestra el producto "funcionando".
Debajo: secciones `// 01..06` con módulos asimétricos, anatomía en ASCII, índice de cifras,
taxonomía como `tree`, atajos y fuentes. Cierre con una línea `EOF · nombre-del-proyecto`.
