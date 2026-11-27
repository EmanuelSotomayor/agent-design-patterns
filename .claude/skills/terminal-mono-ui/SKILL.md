---
name: terminal-mono-ui
description: 'Sistema de diseño de estética terminal/hacker para interfaces web — tipografía monoespaciada (Space Mono + JetBrains Mono auto-hospedadas), modo oscuro casi negro, un único acento verde #37F712 para estado, paneles técnicos con marcas de esquina, navegación tipo menú de consola con prompt de ruta, diagramas ASCII, logs de terminal animados y diagramas de agentes/flujos con nodos tipados. Usa esta skill siempre que el usuario pida una UI o landing con estética terminal, hacker, consola, CLI, matrix, devtool, "modo oscuro técnico", "monoespaciada", "anti-plantilla" o "que no parezca un template", cuando quiera re-tematizar o "aplicar el mismo diseño" a una app existente con ese estilo, cuando construya visualizadores técnicos (agentes de IA, pipelines, flujos paso a paso, documentación de APIs, dashboards de ingeniería), o cuando pida un DESIGN.md para este estilo. Incluye theme.css listo para copiar, hoja de componentes, plantilla de DESIGN.md y scripts de inventario y verificación de layout.'
---

# terminal-mono-ui

Intención: que la interfaz se lea como una herramienta de ingeniería que está funcionando —una
terminal con paneles— y no como una plantilla de landing. Densa, precisa, oscura, con un solo color que
significa "acá está pasando algo".

## Cuándo aplica y cuándo no
- **Sí**: landings de productos técnicos, devtools, visualizadores de agentes/flujos, documentación
  interactiva, dashboards de ingeniería, re-tematizar una app existente a este estilo.
- **No por defecto**: productos de consumo masivo, contenido editorial largo, marcas con identidad
  propia que no sea técnica. Si el usuario no pidió esta estética, preguntá antes de imponerla.

## Archivos de la skill
| Archivo | Para qué | Cuándo leerlo |
|---|---|---|
| `assets/theme.css` | tokens + todos los componentes con prefijo `t-` | copiarlo siempre |
| `assets/fonts/` | Space Mono 400/700, JetBrains Mono variable, licencias OFL | copiar junto al CSS |
| `assets/components.html` | hoja viva de componentes, `<!-- COMPONENT: nombre -->` | antes de maquetar: copiar HTML de ahí |
| `assets/DESIGN.template.md` | DESIGN.md (formato Google, versión alpha) del sistema | al entregar, adaptarlo al proyecto |
| `references/tokens.md` | colores con rol, contraste verificado, tipografía, espacio, movimiento, métricas mono | al definir o dudar de un valor |
| `references/components.md` | anatomía, estados y reglas de cada componente | al construir un componente |
| `references/retrofit.md` | migrar una app existente paso a paso + problemas conocidos | si la UI ya existe |
| `references/ascii.md` | contrato ASCII para diagramas de texto | si hay cajas/flechas en `<pre>` |
| `scripts/inventory.py` | emojis, radios, degradados, sombras, colores, variables de una app | primer paso de un retrofit |
| `scripts/ascii_box.py` | genera cajas ASCII alineadas y lo verifica | en vez de contar guiones |
| `scripts/check_layout.py` | Chromium headless: errores JS, desborde horizontal, texto recortado | antes de entregar |

## Principios (y por qué)
1. **Monoespaciada como estructura.** Todo en mono: alinea columnas, hace que los datos parezcan
   datos y permite calcular anchos sin medir (0.6 em por carácter). Space Mono da personalidad a los
   títulos; JetBrains Mono, legibilidad al resto.
2. **Un solo acento con significado.** El verde `#37F712` marca estado: activo, foco, selección,
   resaltado, CTA principal, marcas de esquina. Si todo es verde, nada lo es. El resto de colores son
   semánticos (azul info/rutas, naranja aviso/decisión, rojo error/"antes", verde oscuro salida).
3. **Bordes, no sombras.** Jerarquía por tono de superficie (4 niveles casi negros), bordes de 1px y
   marcas de esquina. Radio 0. Ni degradados ni elevación.
4. **Marcadores de texto, no emojis.** `[01]`, `// sección`, `## grupo`, `<< antes`, `>> después`,
   `$ cat archivo`, `etiqueta: valor`, `+`/`-`. Los emojis rompen la grilla mono (ocupan doble) y la
   metáfora de terminal.
5. **El prompt dice dónde estás.** Cada vista muestra `usuario@app:~/ruta$ comando`: es breadcrumb y
   descripción de la vista a la vez.
6. **Movimiento con propósito.** Animar solo lo que explica algo (un paso que avanza, un agente que
   trabaja, un cursor). Respetar `prefers-reduced-motion`.
7. **Cifras desde los datos.** Contadores, índices y barras de estado se calculan; nunca se escriben a mano.
8. **Asimetría.** Grilla de 12 columnas con spans 7+5 / 5+7; evitar filas de tarjetas idénticas.

## Flujo A — UI nueva
1. Copiá `assets/theme.css` y `assets/fonts/` al proyecto; poné `class="t-root"` en `<body>` (o en el
   contenedor del módulo si convive con otro estilo).
2. Abrí `assets/components.html` y armá la página con esas piezas: brand + tabs + pathbar arriba;
   status-bar y hero en la home; secciones `// 01..` con paneles asimétricos.
3. Para diagramas con nodos de tamaño fijo, dimensioná con las métricas de `tokens.md` §7 y verificá
   que ninguna etiqueta quede a menos de 6px de un nodo.
4. Si hay figuras de texto, generalas con `scripts/ascii_box.py`.
5. Escribí la copia siguiendo "Voz" (abajo).
6. Copiá `assets/DESIGN.template.md` como `DESIGN.md` en la raíz del proyecto, y `theme.css`,
   `components.html` y `fonts/` a `design/` (sus referencias `@design/...` apuntan ahí). Reemplazá lo
   marcado **COMPLETAR** / *(ejemplo)*: nombre, descripción, vistas, idioma y terminología. Así cualquier
   agente futuro mantiene el estilo. Validalo con `npx -y @google/design.md lint DESIGN.md`: lo esperado
   es 0 errores y 1 aviso sobre `motion` (la especificación lo define, pero el CLI 0.4.0 aún no lo exporta).
7. Verificá (checklist).

## Flujo B — re-tematizar una app existente
Seguí `references/retrofit.md`. Resumen:
1. `python3 scripts/inventory.py <archivos>`.
2. Capa de tema al final de la hoja: redefinir las variables existentes con los tokens, fuente mono
   global, radio 0, sin sombras ni degradados, marcas de esquina en contenedores.
3. Reemplazar emojis de la interfaz por marcadores; quitar los de los datos al renderizar.
4. Recalcular toda geometría de tamaño fijo para la fuente monoespaciada y re-validar colisiones.
5. Corregir desbordes con `minmax(0,1fr)` + `min-width:0` + `overflow-x:auto` en lo ancho.
6. Verificar en 1440/760/500 px y mirar capturas.

Hacé los reemplazos de texto con un script que afirme que cada patrón aparece la cantidad esperada de
veces antes de escribir: así ningún cambio falla en silencio y el archivo no queda a medias.

## Voz
- Copia en **minúsculas** en botones, pestañas de detalle y comandos (`[↵] empezar por el patrón 01`);
  títulos en tipo oración.
- Botones = verbo + objeto. Nada de "OK", "Enviar", "Click aquí".
- Comandos ficticios verosímiles y descriptivos: `./explorar --modo=aprendizaje`, `ls --agrupar`,
  `cat resumen.md`, `./ejecutar --paso-a-paso`.
- Tono preciso y calmo; sin signos de exclamación ni marketing. Nombres propios de técnicas, productos y
  protocolos en su idioma original.
- Estados vacíos y errores con siguiente acción concreta (`Sin resultados. Probá con otro término.`).

## Accesibilidad (verificable)
- Contraste: todo texto informativo ≥ 4.5:1 (ver tabla en `tokens.md`); `text-faint` solo decorativo.
- Foco visible: `outline: 2px solid #37F712; outline-offset: 2px` en todo elemento interactivo.
- Paneles enlazables con `tabindex="0"`, `role="link"` y activación con Enter; pestaña actual con
  `aria-current="page"`; botón de pausa con `aria-pressed`.
- Botones ≥ 44px de alto (36px solo en controles compactos de reproducción).
- `prefers-reduced-motion`: sin parpadeo ni transiciones; logs completos de entrada.

## Checklist antes de entregar
- [ ] `check_layout.py` sin errores JS, sin desborde horizontal, sin texto recortado (1440/760/500 px).
- [ ] Ningún emoji en código de interfaz (`inventory.py`); los de datos se quitan al renderizar.
- [ ] Un solo botón `is-primary` por vista; el verde solo marca estado.
- [ ] Radio 0, sin sombras ni degradados (salvo glows de LED/nodo activo).
- [ ] Cada vista tiene pathbar (salvo la home, que tiene prompt en el hero).
- [ ] Figuras ASCII generadas/verificadas; nada de `┌─│▶` donde haya que alinear columnas.
- [ ] Cifras calculadas desde los datos.
- [ ] Capturas revisadas a escritorio y móvil.
- [ ] `DESIGN.md` en la raíz del proyecto, adaptado.
