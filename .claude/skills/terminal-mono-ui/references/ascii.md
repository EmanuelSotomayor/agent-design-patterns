# Contrato ASCII

Los diagramas de texto (cajas, flechas, árboles alineados en columnas) son parte de la identidad del
sistema. Para que se alineen hay que entender un detalle técnico.

## El problema
Las fuentes auto-hospedadas en subset **latin** no incluyen caracteres de dibujo de cajas
(`┌ ┐ └ ┘ ─ │ ├ ▶ ◀ ▲`). El navegador los toma de otra fuente con **otro ancho de carácter** y las
columnas dejan de coincidir: la línea superior de una caja queda más corta que las de contenido.

## La regla
En cualquier figura donde **dos o más líneas deban alinearse**, usar solo ASCII:

| En vez de | Usar |
|---|---|
| `┌─ título ──┐` / `└───┘` | `+-- título ---+` / `+------+` |
| `│` | `|` |
| `──▶` `◀──` | `-->` `<--` |
| `▲` | `^` |
| `▶152` (marcador de línea) | `>152` |

Se permiten caracteres Unicode **en líneas sueltas** donde no hay alineación vertical que romper:
`→ · ✓ ✗ │` dentro de frases, el separador `│` de la barra de estado, `├──`/`└──` como prefijo idéntico
en todas las líneas de un `tree`.

## Cómo generarlas
No contar guiones a mano. Usar `scripts/ascii_box.py`:

```bash
python3 scripts/ascii_box.py 'ANTES=topic: "Async";sin estructura' 'ACCIÓN=Outliner;_call_llm()' 'DESPUÉS=outline: título'
```

El script verifica que todas las filas tengan el mismo ancho (sale con error si no) y con `--html`
escapa el texto y colorea los títulos para pegarlo en un `<pre>`.

Para figuras de dos líneas (flecha de retorno), verificar con un assert la columna de la esquina:

```python
a = "user --> agent --> tools"
b = " ^-------- resultado --+"
assert b.index("+") == len(a) - 1
```

## Colores dentro de un `<pre>`
Envolver solo palabras (no caracteres de borde) en `<span>`: títulos de caja en `primary`/`secondary`/
`danger` según el rol, notas de evento en `warning`. El resto en `text-2`.
