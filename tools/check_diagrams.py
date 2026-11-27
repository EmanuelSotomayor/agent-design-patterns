"""Valida la geometría de los diagramas normalizados (sin navegador)."""
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from diagrams import label_w, label_h, rects_overlap, rect_hit, bezier  # noqa: E402


def sample_path(d):
    nums = list(map(float, re.findall(r"-?\d+(?:\.\d+)?", d)))
    pts = [(nums[i], nums[i + 1]) for i in range(0, len(nums), 2)]
    if " C " in d and len(pts) == 4:
        return [bezier(*pts, t=i / 60) for i in range(61)]
    out = []
    for a, b in zip(pts, pts[1:]):
        out += [(a[0] + (b[0] - a[0]) * k / 30, a[1] + (b[1] - a[1]) * k / 30) for k in range(31)]
    return out


def check(diag, ends=None):
    """ends: {edge_id: (from_node, to_node)} para no contar los nodos propios de cada flecha."""
    probs = []
    N = diag["nodes"]
    for i, a in enumerate(N):
        for b in N[i + 1:]:
            if rects_overlap((a["x"], a["y"], a["w"], a["h"]), (b["x"], b["y"], b["w"], b["h"]), 4):
                probs.append(f"nodos {a['id']} y {b['id']} superpuestos")
    plates = []
    for e in diag["edges"]:
        if e.get("lx") is None:
            continue
        w = label_w(e["label"])
        hh = label_h(e["label"])
        r = (e["lx"] - w / 2, e["ly"] - hh / 2, w, hh)
        for n in N:
            if diag["kind"] == "seq" and n["cls"] == "actor":
                continue
            if rects_overlap(r, (n["x"], n["y"], n["w"], n["h"]), 2):
                probs.append(f"etiqueta '{e['label'][:30]}' toca nodo {n['id']}")
        for p in plates:
            if rects_overlap(r, p, 1):
                probs.append(f"etiqueta '{e['label'][:30]}' superpuesta a otra")
        plates.append(r)
    if diag["kind"] == "flow" and ends:
        for e in diag["edges"]:
            f, t = ends.get(e["id"], (None, None))
            pts = sample_path(e["d"])[3:-3]
            for n in N:
                if n["id"] in (f, t):
                    continue
                if any(rect_hit(x, y, n, 2) for x, y in pts):
                    probs.append(f"flecha {e['id']} atraviesa {n['id']}")
                    break
    return probs
