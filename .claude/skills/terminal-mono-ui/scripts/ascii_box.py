#!/usr/bin/env python3
"""Genera filas de cajas ASCII alineadas (contrato ASCII de terminal-mono-ui).

Por qué existe: las fuentes monoespaciadas auto-hospedadas suelen venir en subset "latin",
que NO incluye caracteres de dibujo de cajas (┌ ─ │ ▶). El navegador los toma de otra
fuente con otro ancho y las cajas quedan desalineadas. Con ASCII puro (+ - | >) el
ancho es siempre exacto.

Uso:
  python3 ascii_box.py "ANTES=topic: \\"Async\\";sin estructura" "ACCIÓN=Outliner;_call_llm()" "DESPUÉS=outline: título"
    - cada argumento es TÍTULO=línea1;línea2;...
  Opciones:
    --sep " ---> "     conector entre cajas (en la fila de la primera línea de contenido)
    --pad N            ancho interior extra
    --html             escapa < > & y envuelve los títulos en <span class="t-acc">

Salida: texto listo para un <pre>. Verifica que todas las filas midan lo mismo.
"""
import html
import sys


def box(title, lines, inner):
    top = f"+-- {title} " + "-" * max(1, inner - len(title) - 3) + "+"
    width = len(top) - 2
    body = [f"| {l.ljust(width - 2)} |" for l in lines]
    return [top] + body + ["+" + "-" * width + "+"]


def main(argv):
    sep, pad, as_html, specs = " ---> ", 2, False, []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--sep": sep = argv[i + 1]; i += 2; continue
        if a == "--pad": pad = int(argv[i + 1]); i += 2; continue
        if a == "--html": as_html = True; i += 1; continue
        specs.append(a); i += 1
    if not specs:
        print(__doc__); return 2
    boxes = []
    for s in specs:
        title, _, rest = s.partition("=")
        lines = rest.split(";") if rest else [""]
        inner = max(len(title) + 5, max(len(l) for l in lines) + pad)
        boxes.append(box(title, lines, inner))
    height = max(len(b) for b in boxes)
    for b in boxes:                       # iguala alturas con filas vacías antes del borde inferior
        while len(b) < height:
            b.insert(-1, "| " + " " * (len(b[0]) - 4) + " |")
    blank = " " * len(sep)
    rows = []
    for r in range(height):
        joint = sep if r == 1 else blank
        rows.append(joint.join(b[r] for b in boxes))
    widths = {len(r) for r in rows}
    if len(widths) != 1:
        print(f"ERROR: filas con anchos distintos {widths}", file=sys.stderr); return 1
    out = "\n".join(rows)
    if as_html:
        out = html.escape(out)
        for s in specs:
            t = html.escape(s.partition("=")[0])
            out = out.replace(f"-- {t} ", f'-- <span class="t-acc">{t}</span> ', 1)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
