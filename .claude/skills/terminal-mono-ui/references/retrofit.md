# Re-tematizar una aplicación existente

Proceso para llevar una UI ya construida al estilo terminal-mono-ui sin reescribirla. Está basado en
una migración real (una app de una sola página con mapas SVG animados, visor de código, biblioteca
de ~300 fichas y diagramas generados); los problemas listados son los que efectivamente aparecieron.

## Contenido
1. Inventario
2. Capa de tema (variables)
3. Texto de interfaz: emojis → marcadores
4. Geometría: recalcular para monoespaciada
5. Layout: desbordes horizontales
6. Verificación
7. Problemas conocidos y su causa

---

## 1. Inventario
```bash
python3 scripts/inventory.py index.html src/**/*.css
```
Informa emojis (con líneas de ejemplo), `border-radius`, degradados, sombras, colores hex más usados,
variables CSS existentes y familias tipográficas. Separá dos casos:
- emojis en **código de interfaz** (etiquetas, botones, títulos) → se reemplazan (paso 3);
- emojis en **datos** (contenido, JSON, nombres que vienen de una fuente) → no se editan los datos;
  se quitan al renderizar.

## 2. Capa de tema
Si la app ya usa custom properties, no reescribas componentes: agregá **al final** de la hoja una capa
que redefina las variables y anule lo que no encaja.

1. Redefiní en `:root` las variables existentes con los tokens (mapeo típico):
   `--bg→surface`, `--panel→panel`, `--line→outline`, `--text→text`, `--muted→text-2`,
   `--dim→text-3`, `--accent→primary`, y los colores semánticos a sus equivalentes.
2. `html, body { font-family: var(--t-mono) }` y títulos en `var(--t-display)`.
3. Anulá en bloque: `border-radius:0` (con `!important` si hace falta), `box-shadow:none`,
   fondos con `gradient(...)` → color plano, `transform` en hover → nada.
4. Agregá las marcas de esquina a los contenedores principales (tarjetas, paneles, mapas).
5. Revisá colores hardcodeados que no pasan por variables (sombras con rgba azul, fondos de estados,
   colores de resaltado de sintaxis, `fill`/`stroke` de SVG) y llevalos a la paleta.

Si la app no usa variables, primero extraé a custom properties los colores repetidos que dio el inventario.

## 3. Texto de interfaz: emojis → marcadores
| Antes | Después |
|---|---|
| icono en pestaña (`🔀 Routing`) | número con cero: `02 Routing`; `~` inicio, `≡` resumen, `/` biblioteca |
| icono en título de página | `[05] Título` |
| `💡 Consejo…` | `» Consejo…` |
| `🧠 Sonnet` / `🔧 tool` / `📡 evento` | `modelo: Sonnet` / `tool: x` / `evento: y` |
| `⬅ Antes` / `➡ Después` | `<< antes` / `>> después` |
| `📄 archivo.py` | `$ cat archivo.py` |
| `📋 Resumen` / `🔀 Flujo` | `[1] resumen` / `[2] visualización del flujo` |
| `✅ Recomendado` / `❌ Evitar` | título limpio + listas con marcadores `+` / `-` |
| `📚 Biblioteca` en texto | `/ Biblioteca` |

Para datos con emojis al inicio (títulos importados), quitar al renderizar:
```js
const stripEmoji = s => String(s).replace(/^[\p{Extended_Pictographic}️‍\s]+/u, "");
```
Reemplazos de texto hechos con un script: verificá que cada patrón aparezca **exactamente** las veces
esperadas antes de escribir (assert), así ningún reemplazo falla en silencio. Ojo con `sed` y textos que
contienen el delimitador (`|`, `/`): usar Python.

Si los textos mencionan colores de la versión anterior ("resaltadas en azul"), actualizarlos.

## 4. Geometría
La monoespaciada es más ancha (0.6 em por carácter). Todo lo que tenga **tamaño fijo calculado**
se recalcula:
- Nodos de diagramas en `<foreignObject>` (ancho/alto fijos): actualizar las constantes de ancho por
  carácter (`tokens.md` §7) y regenerar. Usar el padding **real** del CSS (borde incluido) en el cálculo.
- Placas de etiquetas: ancho `caracteres·6.3+18`. Si se miden en el navegador (`getComputedTextLength`),
  mejor aún.
- Grillas de diagramas: si una etiqueta no entra en el hueco entre columnas, ensanchar **esa** grilla
  (p. ej. columna de 250 → 270px), no achicar la letra.
- Tras recalcular, volver a correr la validación de colisiones (nodo/nodo, etiqueta/nodo,
  etiqueta/etiqueta, flecha que atraviesa un nodo ajeno).

## 5. Layout: desbordes horizontales
Síntoma: en pantallas angostas toda la página se ensancha y el texto de las tarjetas se corta.
Causa: una pista de grilla `1fr` tiene mínimo `auto`; un hijo con `min-width` grande (SVG con
`min-width:1000px` para seguir legible, `<pre>` con líneas largas, visor de código con
`min-width:max-content`) la estira.
Solución:
```css
.layout   { grid-template-columns: minmax(0, 1fr); }
.layout > * { min-width: 0; }
@media (max-width: 940px) { .two-cols { grid-template-columns: minmax(0, 1fr); } }
pre, .tree, .codeview, .mapwrap { overflow-x: auto; }
```
El contenido ancho hace scroll **dentro de su marco**; la página nunca.

## 6. Verificación
```bash
python3 scripts/check_layout.py index.html --widths 1440,760,500 \
  --view "inicio:goHome()" --view "detalle:openItem('x')"
```
Revisa errores JS, desborde horizontal (y qué elemento lo causa) y texto recortado en nodos/tarjetas.
Además:
- capturas de pantalla a 1440 y 760 px de cada vista principal, y mirarlas;
- buscar emojis restantes en el código de interfaz con `inventory.py`;
- probar teclado: `Tab` muestra el foco verde, `Enter` en paneles enlazables, flechas en reproductores.

## 7. Problemas conocidos
| Síntoma | Causa | Arreglo |
|---|---|---|
| Cajas ASCII desalineadas | subset latin sin `┌─│▶`, fallback con otro ancho | ASCII puro (`ascii.md`) |
| Marca y pestañas `<a>` salen azules | regla genérica `a{color}` con más especificidad | limitarla a `a:not([class])` |
| Texto cortado dentro de nodos | anchos de carácter de fuente proporcional; emojis cuentan doble; palabras largas sin espacios | métricas mono, `vlen` con emojis=2, cortar palabras largas y `overflow-wrap:anywhere` |
| Página más ancha que la pantalla | `1fr` en grillas con hijos anchos | `minmax(0,1fr)` + `min-width:0` |
| Etiqueta de flecha toca un nodo | hueco entre columnas < ancho de placa + 12px | ensanchar la grilla de ese diagrama |
| Captura headless sale negra tras `scrollIntoView` | limitación de la captura | ocultar lo de arriba en vez de hacer scroll |
| Pruebas a 420px dan 485px de ancho | Chromium headless no baja de ~500px de ventana | probar a 500px como mínimo |
