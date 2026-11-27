"""Extrae/aplica las cadenas traducibles de cada archivo (por ruta JSON).

extract: tr/en/*.json -> tr/src/<archivo>.txt   (bloques numerados para traducir)
apply:   tr/en/*.json + tr/out/<archivo>.txt -> tr/es/*.json  (+ validación)
"""
import json, re, sys
from pathlib import Path

S = Path(sys.argv[2])
EN, SRC, OUT, ES = S/"tr/en", S/"tr/src", S/"tr/out", S/"tr/es"

TOP_SKIP = {"cat", "slug", "name", "icon", "complexity", "title", "category"}  # nombres e ids

def skip(path):
    """True si la ruta (sin índices) no debe traducirse."""
    keys = tuple(p for p in path if isinstance(p, str))
    if len(keys) == 1 and keys[0] in TOP_SKIP:
        return True
    if keys[:2] == ("flow", "nodes") and keys[-1] in ("id", "x", "y", "w"):
        return True
    if keys[:2] == ("flow", "edges") and keys[-1] in ("id", "s", "t"):
        return True
    if keys[:2] == ("flow", "steps") and keys[-1] in ("nodes", "edges"):
        return True
    return False

def walk(obj, path=()):
    """Genera (ruta, cadena) de los textos traducibles."""
    if path and skip(path):
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, path + (i,))
    elif isinstance(obj, str) and obj.strip() and re.search(r"[A-Za-z]{2}", obj):
        yield path, obj

def get_set(obj, path, val=None):
    for p in path[:-1]:
        obj = obj[p]
    if val is not None:
        obj[path[-1]] = val
    return obj[path[-1]]

SEP = re.compile(r"^<<<(\d+)>>>$", re.M)

def extract():
    SRC.mkdir(parents=True, exist_ok=True)
    total = 0
    for f in sorted(EN.glob("*.json")):
        d = json.load(open(f, encoding="utf-8"))
        items = list(walk(d))
        total += sum(len(s) for _, s in items)
        with open(SRC / (f.stem + ".txt"), "w", encoding="utf-8") as o:
            for i, (_, s) in enumerate(items):
                o.write(f"<<<{i}>>>\n{s}\n")
    print("caracteres a traducir:", total)

def parse_blocks(text):
    parts = SEP.split(text)
    blocks = {}
    for k in range(1, len(parts) - 1, 2):
        blocks[int(parts[k])] = parts[k + 1].strip("\n")
    return blocks

def apply():
    ES.mkdir(parents=True, exist_ok=True)
    missing, bad = [], []
    for f in sorted(EN.glob("*.json")):
        out = OUT / (f.stem + ".txt")
        if not out.exists():
            missing.append(f.stem); continue
        d = json.load(open(f, encoding="utf-8"))
        items = list(walk(d))
        blocks = parse_blocks(out.read_text(encoding="utf-8"))
        probs = []
        if set(blocks) != set(range(len(items))):
            probs.append(f"bloques {len(blocks)}/{len(items)}")
        same = 0
        for i, (path, s) in enumerate(items):
            if i not in blocks:
                continue
            tr = blocks[i]
            if tr.strip() == s.strip() and len(s) > 25 and " " in s:
                same += 1
            get_set(d, path, tr)
        if same > max(2, len(items) * 0.15):
            probs.append(f"{same} cadenas sin traducir")
        if probs:
            bad.append((f.stem, probs))
            continue
        json.dump(d, open(ES / f.name, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("faltantes:", len(missing), missing[:20])
    print("con problemas:", len(bad))
    for b in bad[:30]: print("  ", b)
    print("OK:", len(list(ES.glob("*.json"))))

{"extract": extract, "apply": apply}[sys.argv[1]]()
