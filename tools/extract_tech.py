"""Extrae Overview + Flow Visualization de las 288 páginas de técnicas (caché local)."""
import html as H, json, re, sys
from pathlib import Path

S = Path(sys.argv[1])
sys.path.insert(0, str(S))
from rsc import rsc_text, find_enclosing_with_key

LIB = json.load(open(sys.argv[2], encoding="utf-8"))
OUT = Path(sys.argv[3])

REF = re.compile(r"^\$[0-9a-zA-Z]+(:|$)")
def clean(v):
    return None if isinstance(v, str) and REF.match(v) else v

def text_lines(h):
    t = re.sub(r"<script.*?</script>", " ", h, flags=re.S)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    return [l.strip() for l in H.unescape(re.sub(r"<[^>]+>", "\n", t)).split("\n") if l.strip()]

def between(lines, a, b):
    i = lines.index(a) + 1
    j = lines.index(b, i)
    return lines[i:j]

def parse_overview30(lines):
    if "30-Second Overview" not in lines:
        return None
    L = lines[lines.index("30-Second Overview"):]
    def after(label):
        return L[L.index(label) + 1]
    o = {"pattern": after("Pattern:"), "why": after("Why:"), "insight": after("Key Insight:")}
    impl, seg = [], between(L, "Quick Implementation", "Example:")
    k = 0
    while k < len(seg):
        if seg[k].isdigit() and k + 3 < len(seg) and seg[k + 2] == ":":
            impl.append({"t": seg[k + 1], "d": seg[k + 3]}); k += 4
        else:
            k += 1
    o["impl"] = impl
    o["example"] = " ".join(between(L, "Example:", "Do's & Don'ts"))
    dd = between(L, "Do's & Don'ts", "When to Use")
    o["dos"] = [dd[k + 1] for k in range(len(dd) - 1) if dd[k] == "✅"]
    o["donts"] = [dd[k + 1] for k in range(len(dd) - 1) if dd[k] == "❌"]
    uw = between(L, "Use When", "Avoid When")
    o["use"] = [uw[k + 1] for k in range(len(uw) - 1) if uw[k] == "•"]
    aw = between(L, "Avoid When", "Key Metrics")
    o["avoid"] = [aw[k + 1] for k in range(len(aw) - 1) if aw[k] == "•"]
    km = between(L, "Key Metrics", "Top Use Cases")
    o["metrics"] = [{"n": km[k], "d": km[k + 1]} for k in range(0, len(km) - 1, 2)]
    uc = []
    for l in L[L.index("Top Use Cases") + 1:]:
        if ":" not in l or l.startswith("References"):
            break
        n, d = l.split(":", 1)
        uc.append({"n": n.strip(), "d": d.strip()})
    o["usecases"] = uc
    return o

def parse_flow(fs):
    nodes = []
    for n in fs.get("initialNodes") or []:
        st = n.get("style") if isinstance(n.get("style"), dict) else {}
        data = n.get("data") if isinstance(n.get("data"), dict) else {}
        pos = n.get("position") if isinstance(n.get("position"), dict) else {}
        w = st.get("width") or st.get("minWidth") or 180
        nodes.append({"id": n["id"], "label": clean(data.get("label")) or n["id"],
                      "x": pos.get("x", 0), "y": pos.get("y", 0), "w": w if isinstance(w, (int, float)) else 180})
    edges = []
    for e in fs.get("initialEdges") or []:
        edges.append({"id": e["id"], "s": e["source"], "t": e["target"], "label": clean(e.get("label")) or ""})
    steps = []
    for s in fs.get("steps") or []:
        steps.append({"title": clean(s.get("title")) or "", "description": clean(s.get("description")) or "",
                      "input": clean(s.get("input")) or "",
                      "nodes": [x for x in (s.get("activeNodes") or []) if isinstance(x, str)],
                      "edges": [x for x in (s.get("activeEdges") or []) if isinstance(x, str)]})
    return {"title": clean(fs.get("title")) or "", "description": clean(fs.get("description")) or "",
            "nodes": nodes, "edges": edges, "steps": steps}

out, problems = [], []
for cat in LIB["agentic_design"]:
    for t in cat["techniques"]:
        h = (S / "raw" / "tech" / f"{cat['slug']}__{t['slug']}.html").read_text(encoding="utf-8")
        o = find_enclosing_with_key(rsc_text(h), "flowScenario") or {}
        st = o.get("selectedTechnique") or {}
        tl = o.get("tldr") if isinstance(o.get("tldr"), dict) else {}
        try:
            ov = parse_overview30(text_lines(h))
        except Exception as e:
            ov = None; problems.append(f"{t['slug']}: overview {e}")
        flow = parse_flow(o.get("flowScenario") or {})
        out.append({
            "cat": cat["slug"], "slug": t["slug"], "name": H.unescape(t["name"]),
            "icon": st.get("icon", ""), "complexity": t["complexity"],
            "description": clean(st.get("description")) or H.unescape(t["desc"]),
            "features": [x for x in (st.get("features") or []) if isinstance(x, str) and not REF.match(x)],
            "tldr": {k: clean(tl.get(k)) or "" for k in ("what", "when", "watchOut")},
            "overview": ov, "flow": flow,
            "references": [x for x in (st.get("references") or []) if isinstance(x, str) and not REF.match(x)],
        })
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
words = len(re.findall(r"\w+", json.dumps([{k: v for k, v in x.items() if k != "references"} for x in out], ensure_ascii=False)))
print(f"técnicas={len(out)} con overview30={sum(1 for x in out if x['overview'])} "
      f"flows con pasos={sum(1 for x in out if x['flow']['steps'])} palabras aprox={words}")
print("problemas:", problems[:10])
