#!/usr/bin/env python3
"""Inventario previo a re-tematizar una app con terminal-mono-ui.

Cuenta lo que hay que cambiar: emojis en el código de interfaz, esquinas redondeadas,
degradados, sombras, colores hardcodeados y familias tipográficas.

Uso:
  python3 inventory.py archivo1.html [archivo2.css src/**/*.tsx ...]
  python3 inventory.py --json index.html        # salida JSON

Los emojis dentro de datos (JSON, contenido) también se listan: decidí en cada caso si
se quitan al renderizar (ver references/retrofit.md, paso 3).
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

# Rangos de pictogramas (code points). Se excluyen a propósito las flechas (U+2190-21FF)
# y las marcas U+2713-2718 (✓ ✔ ✗ ✘), que son tipografía válida en este estilo.
EMOJI_RANGES = [(0x1F300, 0x1FAFF), (0x2600, 0x26FF), (0x2700, 0x2712), (0x2719, 0x27BF), (0x2B05, 0x2B07)]
EMOJI = re.compile("[" + "".join(f"{chr(a)}-{chr(b)}" for a, b in EMOJI_RANGES) + "]")
PATTERNS = {
    "border-radius": re.compile(r"border-radius\s*:\s*([^;}\"']+)"),
    "gradient": re.compile(r"(?:linear|radial|conic)-gradient\("),
    "box-shadow": re.compile(r"box-shadow\s*:\s*(?!none)([^;}\"']+)"),
    "font-family": re.compile(r"font-family\s*:\s*([^;}\"]+)"),
    "hex-color": re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b"),
    "css-var-def": re.compile(r"(--[\w-]+)\s*:"),
}


def scan(path):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    out = {"file": str(path), "lines": text.count("\n") + 1}
    emojis = Counter(EMOJI.findall(text))
    out["emojis"] = dict(emojis.most_common())
    examples = []
    for i, line in enumerate(text.split("\n"), 1):
        if EMOJI.search(line) and len(examples) < 25:
            examples.append(f"{i}: {line.strip()[:110]}")
    out["emoji_lines"] = examples
    for k, rx in PATTERNS.items():
        found = rx.findall(text)
        out[k] = len(found)
        if k in ("font-family",):
            out["font-families"] = sorted({f.strip() for f in found})[:15]
        if k == "hex-color":
            out["top-colors"] = Counter(c.lower() for c in found).most_common(15)
        if k == "css-var-def":
            out["css-vars"] = sorted(set(found))[:60]
    return out


def main():
    args = [a for a in sys.argv[1:] if a != "--json"]
    if not args:
        print(__doc__); sys.exit(2)
    res = [scan(a) for a in args]
    if "--json" in sys.argv:
        print(json.dumps(res, ensure_ascii=False, indent=1)); return
    for r in res:
        print(f"== {r['file']} ({r['lines']} líneas)")
        print(f"  emojis distintos: {len(r['emojis'])}  -> {' '.join(r['emojis'])[:120]}")
        for ex in r["emoji_lines"][:12]:
            print(f"     {ex}")
        print(f"  border-radius: {r['border-radius']}   gradientes: {r['gradient']}   box-shadow: {r['box-shadow']}")
        print(f"  colores hex: {r['hex-color']}  más usados: {', '.join(c for c, _ in r['top-colors'][:8])}")
        print(f"  variables CSS definidas: {len(r['css-vars'])}  {' '.join(r['css-vars'][:20])}")
        print(f"  font-family: {r['font-families']}")
        if r["css-vars"]:
            print("  -> hay variables: re-tematizá con una capa que las redefina (retrofit.md, paso 2).")
        else:
            print("  -> sin variables: primero extraé los colores repetidos a custom properties.")


if __name__ == "__main__":
    main()
