"""Normaliza diagramas a un formato único animable:

    {kind, vb:[minx,miny,W,H], nodes:[{id,title,sub,x,y,w,h,cls}],
     edges:[{id,d,lx,ly,label,dash}], deco:[...], steps:[{title,description,input,nodes,edges}]}

Fuentes:
  - flowScenario de agentic-design.ai (nodos con coordenadas + pasos)  -> technique_flow()
  - bloques ```mermaid (flowchart/graph y sequenceDiagram)             -> mermaid_diagram()

Toda la geometría (tamaños, rutas de flechas, posición de etiquetas) se calcula aquí,
para poder validar colisiones antes de renderizar.
"""
import math
import re

TITLE_CW, SUB_CW, LBL_CW = 7.3, 6.7, 6.3      # ancho por carácter en JetBrains Mono (0.6em: 12px, 11px, 10.5px)
PAD_X = 30   # = padding 12+12 + bordes 4+1.5 del CSS .dnode


# ─── utilidades de texto / geometría ────────────────────────────────────────

def vlen(s):
    """Largo visual: emojis y símbolos anchos cuentan como 2 caracteres."""
    return sum(2 if ord(c) > 0x2500 else 1 for c in s)


def wrap(text, width_px, cw):
    maxc = max(8, int(width_px / cw))
    out = []
    for para in text.split("\n"):
        line = ""
        for word in para.split():
            # palabras sin espacios más largas que la línea se parten (CSS: overflow-wrap:anywhere)
            while vlen(word) > maxc:
                if line:
                    out.append(line); line = ""
                cut = maxc
                while vlen(word[:cut]) > maxc: cut -= 1
                out.append(word[:cut]); word = word[cut:]
            if line and vlen(line) + 1 + vlen(word) > maxc:
                out.append(line)
                line = word
            else:
                line = f"{line} {word}" if line else word
        out.append(line)
    return [l for l in out if l.strip()] or [""]


LBL_MAX = 150   # ancho máximo de una línea de etiqueta (px) antes de partirla


def label_lines(text):
    return wrap(text, LBL_MAX, LBL_CW) if text else []


def label_w(text):
    return max((len(l) for l in label_lines(text)), default=0) * LBL_CW + 18


def label_h(text):
    return 8 + 13 * max(1, len(label_lines(text)))


def node_size(title, sub, w):
    tl = wrap(title, w - PAD_X, TITLE_CW)
    sl = wrap(sub, w - PAD_X, SUB_CW) if sub.strip() else []
    return 20 + 17 * len(tl) + (15 * len(sl) + 4 if sl else 0)


def rect_hit(px, py, r, m=0):
    return r["x"] - m < px < r["x"] + r["w"] + m and r["y"] - m < py < r["y"] + r["h"] + m


def rects_overlap(a, b, m=0):
    return (min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]) > -m and
            min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]) > -m)


def exit_rect(p, q, r):
    dx, dy = q[0] - p[0], q[1] - p[1]
    t = math.inf
    if dx > 0: t = min(t, (r["x"] + r["w"] - p[0]) / dx)
    if dx < 0: t = min(t, (r["x"] - p[0]) / dx)
    if dy > 0: t = min(t, (r["y"] + r["h"] - p[1]) / dy)
    if dy < 0: t = min(t, (r["y"] - p[1]) / dy)
    if t == math.inf: t = 0
    return (p[0] + dx * t, p[1] + dy * t)


def center(r):
    return (r["x"] + r["w"] / 2, r["y"] + r["h"] / 2)


def bezier(p0, c1, c2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t**3 * p3[1])


def f1(v):
    return f"{v:.1f}"


def route_edge(s, t, others, bend_pref=None):
    """Flecha entre rects s→t. Recta si no atraviesa otros nodos; si no, curva que los evita.
    Devuelve (d, puntos_muestreados)."""
    a, b = center(s), center(t)
    p0, p3 = exit_rect(a, b, s), exit_rect(b, a, t)
    straight = [(p0[0] + (p3[0] - p0[0]) * k / 40, p0[1] + (p3[1] - p0[1]) * k / 40) for k in range(41)]
    if not any(rect_hit(x, y, o, 6) for o in others for (x, y) in straight[2:-2]):
        return f"M {f1(p0[0])} {f1(p0[1])} L {f1(p3[0])} {f1(p3[1])}", straight
    # curva: desplaza los puntos de control en la perpendicular, probando ambos lados
    L = math.hypot(p3[0] - p0[0], p3[1] - p0[1]) or 1
    nx, ny = -(p3[1] - p0[1]) / L, (p3[0] - p0[0]) / L
    sides = [1, -1] if bend_pref is None else [bend_pref, -bend_pref]
    best = None
    for k in (0.35, 0.55, 0.8, 1.1, 1.5):
        for sd in sides:
            off = k * L * sd
            # los extremos salen del borde en la dirección de la curva
            ca = (a[0] + nx * off * 0.5, a[1] + ny * off * 0.5)
            cb = (b[0] + nx * off * 0.5, b[1] + ny * off * 0.5)
            q0, q3 = exit_rect(a, ca, s), exit_rect(b, cb, t)
            c1 = (q0[0] + nx * off, q0[1] + ny * off)
            c2 = (q3[0] + nx * off, q3[1] + ny * off)
            pts = [bezier(q0, c1, c2, q3, i / 60) for i in range(61)]
            hits = sum(1 for o in others for (x, y) in pts[3:-3] if rect_hit(x, y, o, 6))
            if best is None or hits < best[0]:
                best = (hits, q0, c1, c2, q3, pts)
            if hits == 0:
                break
        if best and best[0] == 0:
            break
    _, q0, c1, c2, q3, pts = best
    curve = (f"M {f1(q0[0])} {f1(q0[1])} C {f1(c1[0])} {f1(c1[1])} {f1(c2[0])} {f1(c2[1])} "
             f"{f1(q3[0])} {f1(q3[1])}"), pts
    if best[0] == 0:
        return curve
    # último recurso: carril lateral que rodea a todos los nodos intermedios
    lane = side_lane(s, t, others)
    if lane and lane[0] < best[0]:
        return lane[1], lane[2]
    return curve


def route_layered(s, t, wps, others, horizontal):
    """Arista hacia adelante en un layout por capas: sale por la cara inferior (o derecha) de s,
    pasa por los nodos virtuales y entra por la cara superior (o izquierda) de t, con tramos
    curvos de tangente vertical (u horizontal). Si aun así cruza un nodo, usa el carril lateral."""
    sc, tc = center(s), center(t)
    if not horizontal:
        p0, p3 = (sc[0], s["y"] + s["h"]), (tc[0], t["y"])
    else:
        p0, p3 = (s["x"] + s["w"], sc[1]), (t["x"], tc[1])
    chain = [p0] + list(wps or []) + [p3]
    d = f"M {f1(p0[0])} {f1(p0[1])}"
    dense = []
    for a, b in zip(chain, chain[1:]):
        if not horizontal:
            my = (a[1] + b[1]) / 2; c1, c2 = (a[0], my), (b[0], my)
        else:
            mx = (a[0] + b[0]) / 2; c1, c2 = (mx, a[1]), (mx, b[1])
        d += f" C {f1(c1[0])} {f1(c1[1])} {f1(c2[0])} {f1(c2[1])} {f1(b[0])} {f1(b[1])}"
        dense += [bezier(a, c1, c2, b, i / 30) for i in range(31)]
    hits = sum(1 for o in others for (x, y) in dense[2:-2] if rect_hit(x, y, o, 6))
    if hits:
        alt = side_lane(s, t, others)
        if alt[0] < hits:
            return alt[1], alt[2]
    return d, dense


def route_via(s, t, wps, others):
    """Arista larga: pasa por los nodos virtuales reservados en las capas intermedias."""
    p0 = exit_rect(center(s), wps[0], s)
    p3 = exit_rect(center(t), wps[-1], t)
    pts = [p0] + list(wps) + [p3]
    hits, dense = polyline_hits(pts, others)
    if hits:
        alt = side_lane(s, t, others)
        if alt[0] < hits:
            return alt[1], alt[2]
    return "M " + " L ".join(f"{f1(x)} {f1(y)}" for x, y in pts), dense


def polyline_hits(pts, others):
    dense = []
    for a, b in zip(pts, pts[1:]):
        dense += [(a[0] + (b[0] - a[0]) * k / 30, a[1] + (b[1] - a[1]) * k / 30) for k in range(31)]
    return sum(1 for o in others for (x, y) in dense[2:-2] if rect_hit(x, y, o, 6)), dense


def side_lane(s, t, others):
    """Ruta ortogonal por fuera: sale por un costado de s, recorre un carril exterior y entra por el
    mismo costado de t. Prueba derecha/izquierda (diagramas verticales) y arriba/abajo (horizontales)."""
    sc, tc = center(s), center(t)
    y0, y1 = min(s["y"], t["y"]), max(s["y"] + s["h"], t["y"] + t["h"])
    x0, x1 = min(s["x"], t["x"]), max(s["x"] + s["w"], t["x"] + t["w"])
    between_v = [o for o in others if o["y"] < y1 and o["y"] + o["h"] > y0]
    between_h = [o for o in others if o["x"] < x1 and o["x"] + o["w"] > x0]
    cands = []
    X = max([s["x"] + s["w"], t["x"] + t["w"]] + [o["x"] + o["w"] for o in between_v]) + 30
    cands.append([(s["x"] + s["w"], sc[1]), (X, sc[1]), (X, tc[1]), (t["x"] + t["w"], tc[1])])
    X = min([s["x"], t["x"]] + [o["x"] for o in between_v]) - 30
    cands.append([(s["x"], sc[1]), (X, sc[1]), (X, tc[1]), (t["x"], tc[1])])
    Y = max([s["y"] + s["h"], t["y"] + t["h"]] + [o["y"] + o["h"] for o in between_h]) + 30
    cands.append([(sc[0], s["y"] + s["h"]), (sc[0], Y), (tc[0], Y), (tc[0], t["y"] + t["h"])])
    Y = min([s["y"], t["y"]] + [o["y"] for o in between_h]) - 30
    cands.append([(sc[0], s["y"]), (sc[0], Y), (tc[0], Y), (tc[0], t["y"])])
    # variantes: salir/entrar por cara superior/inferior hacia el hueco entre filas y luego al carril
    Xr = max([s["x"] + s["w"], t["x"] + t["w"]] + [o["x"] + o["w"] for o in between_v]) + 30
    Xl = min([s["x"], t["x"]] + [o["x"] for o in between_v]) - 30
    for X in (Xr, Xl):
        for sf in ("top", "bottom"):
            for tf in ("top", "bottom"):
                ys, ys0 = (s["y"], s["y"] - 24) if sf == "top" else (s["y"] + s["h"], s["y"] + s["h"] + 24)
                yt, yt0 = (t["y"], t["y"] - 24) if tf == "top" else (t["y"] + t["h"], t["y"] + t["h"] + 24)
                cands.append([(sc[0], ys), (sc[0], ys0), (X, ys0), (X, yt0), (tc[0], yt0), (tc[0], yt)])
    Yb = max([s["y"] + s["h"], t["y"] + t["h"]] + [o["y"] + o["h"] for o in between_h]) + 30
    Yt = min([s["y"], t["y"]] + [o["y"] for o in between_h]) - 30
    for Y in (Yb, Yt):
        for sf in ("left", "right"):
            for tf in ("left", "right"):
                xs_, xs0 = (s["x"], s["x"] - 24) if sf == "left" else (s["x"] + s["w"], s["x"] + s["w"] + 24)
                xt, xt0 = (t["x"], t["x"] - 24) if tf == "left" else (t["x"] + t["w"], t["x"] + t["w"] + 24)
                cands.append([(xs_, sc[1]), (xs0, sc[1]), (xs0, Y), (xt0, Y), (xt0, tc[1]), (xt, tc[1])])
    best = None
    for pts in cands:
        hits, dense = polyline_hits(pts, others)
        length = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))
        key = (hits, length)
        if best is None or key < best[0]:
            best = (key, pts, dense)
    (hits, _), pts, dense = best
    d = "M " + " L ".join(f"{f1(x)} {f1(y)}" for x, y in pts)
    return hits, d, dense


def place_label(text, pts, node_rects, placed):
    """Ubica la placa sobre la flecha (o a su costado) en un punto libre de nodos y de otras placas."""
    if not text:
        return None
    w, h = label_w(text), label_h(text)
    n = len(pts) - 1
    offs = [(0, 0), (w / 2 + 8, 0), (-w / 2 - 8, 0), (0, -h / 2 - 8), (0, h / 2 + 8),
            (w / 2 + 8, -h / 2 - 8), (-w / 2 - 8, -h / 2 - 8), (w / 2 + 8, h / 2 + 8), (-w / 2 - 8, h / 2 + 8)]
    fracs = [0.5, 0.4, 0.6, 0.3, 0.7, 0.22, 0.78, 0.12, 0.88] + [k / 20 for k in range(1, 20)]
    for frac in fracs:
        bx, by = pts[round(frac * n)]
        for ox, oy in offs:
            x, y = bx + ox, by + oy
            r = (x - w / 2, y - h / 2, w, h)
            if any(rects_overlap(r, (o["x"], o["y"], o["w"], o["h"]), 6) for o in node_rects):
                continue
            if any(rects_overlap(r, p, 3) for p in placed):
                continue
            placed.append(r)
            return (x, y)
    x, y = pts[n // 2]
    placed.append((x - w / 2, y - h / 2, w, h))
    return (x, y)


def finish(kind, nodes, edges, deco, steps, extra_pts=()):
    xs, ys = [], []
    for n in nodes:
        xs += [n["x"], n["x"] + n["w"]]; ys += [n["y"], n["y"] + n["h"]]
    for e in edges:
        for (x, y) in e.pop("_pts", []):
            xs.append(x); ys.append(y)
        if e.get("lx") is not None:
            w, h = label_w(e["label"]) / 2, label_h(e["label"]) / 2
            xs += [e["lx"] - w, e["lx"] + w]; ys += [e["ly"] - h, e["ly"] + h]
    for (x, y) in extra_pts:
        xs.append(x); ys.append(y)
    pad = 30
    vb = [min(xs) - pad, min(ys) - pad, max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad]
    return {"kind": kind, "vb": [round(v, 1) for v in vb], "nodes": nodes, "edges": edges,
            "deco": deco, "steps": steps}


# ─── 1) flowScenario de agentic-design.ai ───────────────────────────────────

def split_label(label):
    parts = [p.strip() for p in str(label).split("\n") if p.strip()]
    if not parts:
        return "", ""
    return parts[0], "\n".join(parts[1:])


def spread(nodes, gap_x=70, gap_y=56):
    """Escala las coordenadas para que ningún par de nodos quede a menos de gap_x/gap_y."""
    sx = sy = 1.0
    for i, a in enumerate(nodes):
        for b in nodes[i + 1:]:
            ca, cb = center(a), center(b)
            dx, dy = abs(ca[0] - cb[0]), abs(ca[1] - cb[1])
            need_x = (a["w"] + b["w"]) / 2 + gap_x
            need_y = (a["h"] + b["h"]) / 2 + gap_y
            if dx < need_x and dy < need_y:          # se superponen (con margen)
                # resolver por el eje que requiera menos escala
                rx = need_x / dx if dx > 1 else math.inf
                ry = need_y / dy if dy > 1 else math.inf
                if rx <= ry: sx = max(sx, rx)
                else: sy = max(sy, ry)
    if sx > 1 or sy > 1:
        for n in nodes:
            c = center(n)
            n["x"] = c[0] * sx - n["w"] / 2
            n["y"] = c[1] * sy - n["h"] / 2
    return sx, sy


def _depth(nodes, medges):
    """Cantidad de capas (camino más largo, ignorando ciclos de forma aproximada)."""
    ids = [n["id"] for n in nodes]
    layer = {i: 0 for i in ids}
    for _ in range(len(ids)):
        ch = False
        for e in medges:
            if e["s"] != e["t"] and layer[e["t"]] < layer[e["s"]] + 1 and layer[e["s"]] < len(ids):
                layer[e["t"]] = layer[e["s"]] + 1; ch = True
        if not ch: break
    return min(max(layer.values()) + 1, len(ids))


SPACING = [(50, 0), (80, 20), (120, 40), (170, 60)]


def best_of(build, ends):
    """Construye el diagrama con espaciados crecientes y devuelve el primero sin colisiones
    (o el de menos colisiones)."""
    from check_diagrams import check   # import diferido (check_diagrams importa este módulo)
    best = None
    for gi, gl in SPACING:
        d = build(gi, gl)
        n = len(check(d, ends))
        if best is None or n < best[0]:
            best = (n, d)
        if n == 0:
            break
    return best[1]


def technique_flow(flow):
    ends = {e["id"]: (e["s"], e["t"]) for e in flow["edges"]}
    return best_of(lambda gi, gl: _technique_flow(flow, gi, gl), ends)


def _technique_flow(flow, gap_in=50, extra_layer=0):
    """Re-diagrama el flowScenario con layout por capas (las coordenadas del sitio solo
    se usan para el orden inicial y para elegir orientación vertical u horizontal)."""
    raw = flow["nodes"]
    if not raw:
        return None
    xs = [n["x"] for n in raw]; ys = [n["y"] for n in raw]
    direction = "LR" if (max(xs) - min(xs)) > 1.6 * (max(ys) - min(ys)) else "TD"
    order = sorted(raw, key=(lambda n: (n["x"], n["y"])) if direction == "LR" else (lambda n: (n["y"], n["x"])))
    nodes = []
    for n in order:
        title, sub = split_label(n["label"])
        w = max(160, min(230, len(title) * TITLE_CW + PAD_X + 6))
        if sub:
            w = max(w, 190)
        nodes.append({"id": n["id"], "title": title, "sub": sub, "w": w, "h": node_size(title, sub, w),
                      "cls": "step"})
    ids = {n["id"] for n in nodes}
    medges = [{"s": e["s"], "t": e["t"], "label": e.get("label", ""), "id": e["id"]}
              for e in flow["edges"] if e["s"] in ids and e["t"] in ids]
    if direction == "LR" and _depth(nodes, medges) > 7:
        direction = "TD"
    back, _rows, wps = layered_layout(direction, nodes, medges, gap_in, extra_layer)
    ins = {e["t"] for e in medges}; outs = {e["s"] for e in medges}
    for n in nodes:
        if n["id"] not in ins and n["id"] in outs: n["cls"] = "input"
        elif n["id"] in ins and n["id"] not in outs: n["cls"] = "output"
    edges = route_all(nodes, medges, back, wps, direction in ("LR", "RL"))
    byid = {n["id"]: n for n in nodes}
    eids = {e["id"] for e in edges}
    steps = [{"title": s["title"], "description": s["description"], "input": s.get("input", ""),
              "nodes": [x for x in s["nodes"] if x in byid],
              "edges": [x for x in s["edges"] if x in eids]}
             for s in flow["steps"]]
    return finish("flow", nodes, edges, [], steps)


def route_all(nodes, medges, back, waypoints=None, horizontal=None):
    """Rutea todas las flechas y ubica sus etiquetas (primero las que no tienen etiqueta)."""
    byid = {n["id"]: n for n in nodes}
    routed = []
    for k, e in enumerate(medges):
        s, t = byid[e["s"]], byid[e["t"]]
        others = [n for n in nodes if n["id"] not in (e["s"], e["t"])]
        if e["s"] == e["t"]:
            x, y = s["x"] + s["w"], s["y"] + s["h"] / 2
            d = f"M {f1(x)} {f1(y-10)} C {f1(x+50)} {f1(y-40)} {f1(x+50)} {f1(y+40)} {f1(x)} {f1(y+10)}"
            pts = [bezier((x, y - 10), (x + 50, y - 40), (x + 50, y + 40), (x, y + 10), i / 30) for i in range(31)]
            lw = label_w(e["label"]) / 2 if e["label"] else 0
            pts = [(x + 46 + lw, y + dy) for dy in (0, -14, 14, -28, 28)] + pts
        elif k in back:
            d, pts = route_edge(s, t, others, bend_pref=1)
            lane = side_lane(s, t, others)
            if lane[0] == 0 and any(rect_hit(x, y, o, 6) for o in others for (x, y) in pts[3:-3]):
                d, pts = lane[1], lane[2]
            if " L " in d:   # un retorno recto se confundiría con la ida: fuerza una curva
                fake = {"x": (center(s)[0] + center(t)[0]) / 2 - 1, "y": (center(s)[1] + center(t)[1]) / 2 - 1, "w": 2, "h": 2}
                d, pts = route_edge(s, t, others + [fake], bend_pref=1)
        elif horizontal is not None:
            d, pts = route_layered(s, t, (waypoints or {}).get(k), others, horizontal)
        elif waypoints and k in waypoints:
            d, pts = route_via(s, t, waypoints[k], others)
        else:
            d, pts = route_edge(s, t, others)
        routed.append((k, e, d, pts))
    placed, edges = [], []
    for k, e, d, pts in routed:
        pos = place_label(e["label"], pts, nodes, placed)
        edges.append({"id": e.get("id", f"m{k}"), "d": d, "label": e["label"], "dash": e.get("dash", False),
                      "lx": pos[0] if pos else None, "ly": pos[1] if pos else None, "_pts": pts})
    return edges


# ─── 2) Mermaid ─────────────────────────────────────────────────────────────

def clean_label(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] == '"':
        s = s[1:-1]
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</?[a-z][^>]*>", "", s, flags=re.I)
    s = s.replace("**", "").replace("&quot;", '"').replace("#quot;", '"')
    return s.strip()


SHAPES = [  # (apertura, cierre, clase)
    ("[[", "]]", "step"), ("[(", ")]", "store"), ("((", "))", "step"), ("([", "])", "step"),
    ("{{", "}}", "decision"), ("[/", "/]", "step"), ("[\\", "\\]", "step"),
    ("[", "]", "step"), ("(", ")", "step"), ("{", "}", "decision"), (">", "]", "step"),
]
NODE_ID = re.compile(r"\s*([A-Za-z0-9_À-ɏ][\w\-\.À-ɏ]*)")
LINK = re.compile(
    r"\s*(?:"
    r"(?P<t1>--|==|-\.)\s*(?P<txt>[^>|\-][^>|]*?)\s*(?P<a1>-->|==>|\.->|---|-\.-)"   # A -- texto --> B
    r"|(?P<a2><?(?:-->|==>|-\.->|---|===|-\.-|--o|--x|-->>))(?:\s*\|(?P<pipe>[^|]*)\|)?"  # A -->|texto| B
    r")\s*")


def parse_node(line, pos, nodes, order):
    m = NODE_ID.match(line, pos)
    if not m:
        return None, pos
    nid, pos = m.group(1), m.end()
    label, cls = None, None
    for op, cl, c in SHAPES:
        if line.startswith(op, pos):
            end = line.find(cl, pos + len(op))
            # etiquetas con comillas pueden contener el cierre: respétalas
            if line.startswith(op + '"', pos):
                q = line.find('"', pos + len(op) + 1)
                if q > 0:
                    end = line.find(cl, q)
            if end > 0:
                label = clean_label(line[pos + len(op):end])
                cls = c
                pos = end + len(cl)
            break
    if nid not in nodes:
        nodes[nid] = {"id": nid, "label": label or nid, "cls": cls or "step"}
        order.append(nid)
    elif label:
        nodes[nid]["label"] = label
        nodes[nid]["cls"] = cls
    return nid, pos


def parse_group(line, pos, nodes, order):
    ids = []
    while True:
        nid, pos = parse_node(line, pos, nodes, order)
        if nid is None:
            break
        ids.append(nid)
        m = re.match(r"\s*&\s*", line[pos:])
        if not m:
            break
        pos += m.end()
    return ids, pos


def parse_flowchart(src):
    lines = [l.strip() for l in src.strip().split("\n")]
    head = lines[0].split()
    direction = head[1].upper() if len(head) > 1 else "TD"
    nodes, order, edges = {}, [], []
    for raw in lines[1:]:
        if not raw or raw.startswith("%%"):
            continue
        kw = raw.split()[0]
        if kw in ("classDef", "class", "style", "linkStyle", "click", "end", "direction"):
            continue
        if kw == "subgraph":
            continue
        for stmt in raw.split(";"):
            pos = 0
            left, pos = parse_group(stmt, pos, nodes, order)
            while left:
                m = LINK.match(stmt, pos)
                if not m:
                    break
                txt = m.group("txt") or m.group("pipe") or ""
                arrow = m.group("a1") or m.group("a2") or ""
                pos = m.end()
                right, pos = parse_group(stmt, pos, nodes, order)
                for a in left:
                    for b in right:
                        edges.append({"s": a, "t": b, "label": clean_label(txt),
                                      "dash": "." in arrow, "arrow": not arrow.endswith("-")})
                left = right
    return direction, [nodes[i] for i in order], edges


def layered_layout(direction, nodes, edges, gap_in=50, extra_layer=0):
    """Layout por capas (Sugiyama): capas por camino más largo, nodos virtuales para aristas
    largas, orden por baricentro (barridos hacia abajo y hacia arriba) y coordenadas.
    Devuelve (aristas_de_retorno, filas_reales, waypoints {k: [(x,y), ...]})."""
    ids = [n["id"] for n in nodes]
    out = {i: [] for i in ids}
    for k, e in enumerate(edges):
        out[e["s"]].append((e["t"], k))
    back, state = set(), {}

    def dfs(u):
        state[u] = 1
        for v, k in out[u]:
            if state.get(v) == 1: back.add(k)
            elif v not in state: dfs(v)
        state[u] = 2

    for i in ids:
        if i not in state: dfs(i)
    fwd = [k for k, e in enumerate(edges) if k not in back and e["s"] != e["t"]]
    layer = {i: 0 for i in ids}
    for _ in range(len(ids)):
        changed = False
        for k in fwd:
            e = edges[k]
            if layer[e["t"]] < layer[e["s"]] + 1:
                layer[e["t"]] = layer[e["s"]] + 1; changed = True
        if not changed: break
    L = max(layer.values()) + 1
    horizontal = direction in ("LR", "RL")
    byid = {n["id"]: n for n in nodes}
    for n in nodes:
        if "h" in n:
            continue
        n["w"] = max(140, min(230, max(len(l) for l in n["label"].split("\n")) * TITLE_CW + PAD_X + 6))
        n["title"], n["sub"] = split_label(n["label"])
        n["h"] = node_size(n["title"], n["sub"], n["w"])
    # nodos virtuales: un eslabón por cada capa intermedia de una arista larga
    sizes = {i: (byid[i]["w"], byid[i]["h"]) for i in ids}
    up = {i: [] for i in ids}; down = {i: [] for i in ids}
    chains = {}
    for k in fwd:
        e = edges[k]
        prev = e["s"]; chain = []
        for l in range(layer[e["s"]] + 1, layer[e["t"]]):
            d = f"__d{k}_{l}"
            layer[d] = l; sizes[d] = (18, 18); up[d] = []; down[d] = []
            down[prev].append(d); up[d].append(prev)
            chain.append(d); prev = d
        down[prev].append(e["t"]); up[e["t"]].append(prev)
        chains[k] = chain
    allids = ids + [d for c in chains.values() for d in c]
    rows = [[i for i in allids if layer[i] == l] for l in range(L)]
    for _ in range(4):
        idx = {i: p for r in rows for p, i in enumerate(r)}
        for l in range(1, L):
            rows[l].sort(key=lambda i: (sum(idx[p] for p in up[i]) / len(up[i])) if up[i] else idx[i])
            idx.update({i: p for p, i in enumerate(rows[l])})
        for l in range(L - 2, -1, -1):
            rows[l].sort(key=lambda i: (sum(idx[c] for c in down[i]) / len(down[i])) if down[i] else idx[i])
            idx.update({i: p for p, i in enumerate(rows[l])})
    has_lbl = any(e["label"] for e in edges)
    max_lw = max([label_w(e["label"]) for e in edges if e["label"]] or [0])
    max_lh = max([label_h(e["label"]) for e in edges if e["label"]] or [0])
    if not horizontal:
        gap_layer = max(100, 2 * max_lh + 44) if has_lbl else 72
    else:
        gap_layer = max(100, max_lw + 40) if has_lbl else 72
    gap_layer += extra_layer
    pos = {}
    main_sz = (lambda i: sizes[i][0]) if not horizontal else (lambda i: sizes[i][1])
    cross_sz = (lambda i: sizes[i][1]) if not horizontal else (lambda i: sizes[i][0])
    spans = [sum(main_sz(i) for i in r) + gap_in * (len(r) - 1) for r in rows]
    maxspan = max(spans)
    acc = 0
    for r, span in zip(rows, spans):
        c = (maxspan - span) / 2
        depth = max(cross_sz(i) for i in r if not i.startswith("__d")) if any(not i.startswith("__d") for i in r) else 18
        for i in r:
            w, h = sizes[i]
            if not horizontal:
                pos[i] = (c, acc + (depth - h) / 2); c += w + gap_in
            else:
                pos[i] = (acc + (depth - w) / 2, c); c += h + gap_in
        acc += depth + gap_layer
    for i in ids:
        byid[i]["x"], byid[i]["y"] = pos[i]
    waypoints = {k: [(pos[d][0] + 9, pos[d][1] + 9) for d in chain] for k, chain in chains.items() if chain}
    real_rows = [[i for i in r if not i.startswith("__d")] for r in rows]
    return back, real_rows, waypoints


def mermaid_flowchart(src):
    _, _, me = parse_flowchart(src)
    if not me:
        return _mermaid_flowchart(src)
    ends = {f"m{k}": (e["s"], e["t"]) for k, e in enumerate(me)}
    return best_of(lambda gi, gl: _mermaid_flowchart(src, gi, gl), ends)


def _mermaid_flowchart(src, gap_in=50, extra_layer=0):
    direction, nodes, medges = parse_flowchart(src)
    if not nodes:
        return None
    back, rows, wps = layered_layout(direction, nodes, medges, gap_in, extra_layer)
    ins = {e["t"] for e in medges}; outs = {e["s"] for e in medges}
    for n in nodes:
        if n["cls"] == "step":
            if n["id"] not in ins and n["id"] in outs: n["cls"] = "input"
            elif n["id"] in ins and n["id"] not in outs: n["cls"] = "output"
    byid = {n["id"]: n for n in nodes}
    for k, e in enumerate(medges):
        e["id"] = f"m{k}"
    edges = route_all(nodes, medges, back, wps, direction in ("LR", "RL"))
    # pasos: recorrido por capas (BFS) — cada capa activa sus nodos y las flechas que llegan a ellos
    steps = []
    for l, r in enumerate(rows):
        inc = [f"m{k}" for k, e in enumerate(medges) if e["t"] in r and k not in back]
        names = ", ".join(byid[i]["title"] for i in r)
        steps.append({"title": names if len(r) == 1 else f"Etapa {l + 1}", "description": names,
                      "input": "", "nodes": list(r), "edges": inc})
    if back:
        steps.append({"title": "Bucle de retorno", "description": "; ".join(
            f"{byid[medges[k]['s']]['title']} → {byid[medges[k]['t']]['title']}" for k in sorted(back)),
            "input": "", "nodes": sorted({medges[k]["s"] for k in back} | {medges[k]["t"] for k in back}),
            "edges": [f"m{k}" for k in sorted(back)]})
    for n in nodes:
        n.pop("label", None)
    return finish("flow", nodes, edges, [], steps)


_PID = r"[\wÀ-ɏ](?:[\w\-À-ɏ]*[\wÀ-ɏ])?"   # un id no termina en "-"
SEQ_MSG = re.compile(r"^(" + _PID + r")\s*(-->>|->>|-->|->|--x|-x|--\)|-\))\s*([+-]?)(" + _PID + r")\s*:\s*(.*)$")


def mermaid_sequence(src):
    lines = [l.strip() for l in src.strip().split("\n")[1:]]
    parts, alias = [], {}
    events = []      # ("msg", a, b, text, dashed) | ("note", [ids], text) | ("open", kind, title) | ("else", title) | ("close",)

    def add_p(pid, lbl=None):
        if pid not in parts:
            parts.append(pid)
        if lbl: alias[pid] = clean_label(lbl)

    for l in lines:
        if not l or l.startswith("%%") or l.startswith("autonumber") or l.startswith(("activate", "deactivate")):
            continue
        m = re.match(r"^(participant|actor)\s+([\w\-À-ɏ]+)(?:\s+as\s+(.+))?$", l)
        if m:
            add_p(m.group(2), m.group(3)); continue
        m = re.match(r"^Note\s+(left of|right of|over)\s+([^:]+):\s*(.*)$", l, re.I)
        if m:
            ids = [x.strip() for x in m.group(2).split(",")]
            for i in ids: add_p(i)
            events.append(("note", ids, clean_label(m.group(3)))); continue
        m = re.match(r"^(loop|alt|opt|par|critical|break|rect)\b\s*(.*)$", l)
        if m:
            events.append(("open", m.group(1), clean_label(m.group(2)))); continue
        m = re.match(r"^(else|and)\b\s*(.*)$", l)
        if m:
            events.append(("else", clean_label(m.group(2)))); continue
        if l == "end":
            events.append(("close",)); continue
        m = SEQ_MSG.match(l)
        if m:
            add_p(m.group(1)); add_p(m.group(4))
            events.append(("msg", m.group(1), m.group(4), clean_label(m.group(5)), m.group(2).startswith("--")))
    if not parts:
        return None
    # ancho de columna según textos de los mensajes
    col = 210
    for ev in events:
        if ev[0] == "msg" and ev[1] != ev[2]:
            span = abs(parts.index(ev[1]) - parts.index(ev[2])) or 1
            col = max(col, (label_w(ev[3]) + 40) / span)
    col = min(col, 330)
    cx = {p: i * col for i, p in enumerate(parts)}
    nodes = []
    for p in parts:
        title = alias.get(p, p)
        w = min(col - 30, max(120, len(title) * TITLE_CW + PAD_X))
        h = node_size(title, "", w)
        nodes.append({"id": "p_" + p, "title": title, "sub": "", "x": cx[p] - w / 2, "y": 0, "w": w, "h": h,
                      "cls": "actor"})
    top = max(n["h"] for n in nodes)
    y = top + 50
    edges, deco, steps, frames = [], [], [], []
    for ev in events:
        if ev[0] == "open":
            frames.append({"kind": ev[1], "title": ev[2], "y0": y - 6, "elses": []}); y += 30
        elif ev[0] == "else" and frames:
            frames[-1]["elses"].append((y, ev[1])); y += 30
        elif ev[0] == "close" and frames:
            f = frames.pop()
            deco.append({"type": "frame", "kind": f["kind"], "title": f["title"], "x": -col / 2 + 12,
                         "y": f["y0"], "w": col * (len(parts) - 1) + col - 24, "h": y - f["y0"] + 4,
                         "elses": [{"y": ey, "title": et} for ey, et in f["elses"]]})
            y += 18
        elif ev[0] == "note":
            xs = [cx[i] for i in ev[1]]
            w = max(160, min(col * 1.6, max(xs) - min(xs) + 150))
            sub_lines = wrap(ev[2], w - PAD_X, SUB_CW)
            h = 16 + 15 * len(sub_lines)
            nid = f"note{len(steps)}"
            nodes.append({"id": nid, "title": "", "sub": ev[2], "x": (min(xs) + max(xs)) / 2 - w / 2, "y": y,
                          "w": w, "h": h, "cls": "note"})
            steps.append({"title": "Nota", "description": ev[2], "input": "",
                          "nodes": [nid] + ["p_" + i for i in ev[1]], "edges": []})
            nxt = events[events.index(ev) + 1] if events.index(ev) + 1 < len(events) else None
            nlh = label_h(nxt[3]) if nxt and nxt[0] == "msg" and nxt[3] else 20
            y += h + max(36, nlh + 26)
        elif ev[0] == "msg":
            _, a, b, text, dashed = ev
            eid = f"s{len(edges)}"
            if a == b:
                x = cx[a]
                d = f"M {f1(x)} {f1(y)} L {f1(x+46)} {f1(y)} L {f1(x+46)} {f1(y+24)} L {f1(x+4)} {f1(y+24)}"
                lw = label_w(text) if text else 0
                edges.append({"id": eid, "d": d, "label": text, "dash": dashed,
                              "lx": x + 56 + lw / 2 if text else None, "ly": y + 12,
                              "_pts": [(x, y), (x + 46, y + 24)]})
                y += 58 + max(0, label_h(text) - 20)
            else:
                x1, x2 = cx[a], cx[b]
                sgn = 1 if x2 > x1 else -1
                d = f"M {f1(x1 + 4*sgn)} {f1(y)} L {f1(x2 - 4*sgn)} {f1(y)}"
                lh = label_h(text) if text else 0
                edges.append({"id": eid, "d": d, "label": text, "dash": dashed,
                              "lx": (x1 + x2) / 2 if text else None, "ly": y - lh / 2 - 4,
                              "_pts": [(x1, y), (x2, y)]})
                nxt = events[events.index(ev) + 1] if events.index(ev) + 1 < len(events) else None
                nlh = label_h(nxt[3]) if nxt and nxt[0] == "msg" and nxt[3] else 20
                y += max(52, nlh + 34)
            steps.append({"title": f"{alias.get(a, a)} → {alias.get(b, b)}", "description": text, "input": "",
                          "nodes": ["p_" + a, "p_" + b], "edges": [eid]})
    bottom = y + 10
    for p in parts:
        deco.insert(0, {"type": "lifeline", "x": cx[p], "y1": top, "y2": bottom})
    return finish("seq", nodes, edges, deco, steps,
                  extra_pts=[(-col / 2 + 6, bottom), (cx[parts[-1]] + col / 2 - 6, bottom)])


def mermaid_diagram(src):
    head = src.strip().split("\n")[0].strip().split()[0]
    if head in ("flowchart", "graph"):
        return mermaid_flowchart(src)
    if head == "sequenceDiagram":
        return mermaid_sequence(src)
    return None
