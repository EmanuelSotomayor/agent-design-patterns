#!/usr/bin/env python3
"""Genera library_data.js (window.LIBRARY) para la Biblioteca de patrones.

Fuentes (en src/library/):
  techniques_en.json        288 técnicas de agentic-design.ai (Overview + Flow) en inglés
  production_en/*.json      41 patrones en producción de agentic-patterns.com en inglés
  es/T__*.json, es/P__*.json traducciones al español (si falta alguna, se usa el inglés y se marca)
  taxonomy_es.json          grupos -> categorías, con descripciones en español

Los diagramas (Visualización del flujo) se calculan con tools/diagrams.py.
Ejecutar:  python3 generate_library.py
"""
import html as _html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIB = ROOT / "src" / "library"
sys.path.insert(0, str(ROOT / "tools"))
from diagrams import technique_flow, mermaid_diagram  # noqa: E402
from check_diagrams import check  # noqa: E402

OUT = ROOT / "library_data.js"
U = _html.unescape

# patrón animado de la app -> técnica equivalente en agentic-design.ai (para su Resumen)
BRIDGE = {
    "chaining": ("prompt-chaining", "sequential-chaining"),
    "routing": ("routing", "llm-based-routing"),
    "parallelization": ("parallelization", "scatter-gather"),
    "orchestrator": ("multi-agent", "supervisor-worker-pattern"),
    "evaluator": ("reflection", "producer-critic"),
    "hitl": ("ui-ux-patterns", "human-in-the-loop"),
    "react": ("reasoning-techniques", "react"),
    "mapreduce": ("parallelization", "map-reduce"),
    "planthenexecute": ("planning-execution", "plan-execute-decoupling"),
    "reflexion": ("reflection", "reflexion-pattern"),
}

SEC_ES = {"Problem": "Problema", "Solution": "Solución", "How to use it": "Cómo usarlo",
          "Trade-offs": "Ventajas y desventajas", "References": "Referencias", "Evidence": "Evidencia",
          "Example": "Ejemplo", "Use Cases": "Casos de uso"}


def load_es(prefix, stem):
    f = LIB / "es" / f"{prefix}__{stem}.json"
    return json.load(open(f, encoding="utf-8")) if f.exists() else None


def split_sections(body):
    """Divide el markdown en secciones '## Título'. Devuelve [(título, md)]."""
    parts = re.split(r"^## +(.+)$", body, flags=re.M)
    out = []
    if parts[0].strip():
        out.append(("", parts[0].strip()))
    for k in range(1, len(parts) - 1, 2):
        out.append((parts[k].strip(), parts[k + 1].strip()))
    return out


MERMAID = re.compile(r"```mermaid\s*\n(.*?)```", re.S)


def build_techniques(tax):
    tech_en = json.load(open(LIB / "techniques_en.json", encoding="utf-8"))
    by_cat = {}
    stats = {"es": 0, "en": 0, "diag_fallback": 0, "diag_issues": 0}
    for t in tech_en:
        es = load_es("T", f"{t['cat']}__{t['slug']}")
        src = es or t
        stats["es" if es else "en"] += 1
        diag = technique_flow(src["flow"])
        ends = {e["id"]: (e["s"], e["t"]) for e in src["flow"]["edges"]}
        if check(diag, ends):
            stats["diag_issues"] += 1
        by_cat.setdefault(t["cat"], []).append({
            "slug": t["slug"], "name": U(t["name"]), "icon": t["icon"], "complexity": t["complexity"],
            "lang": "es" if es else "en",
            "description": src["description"], "features": src["features"], "tldr": src["tldr"],
            "overview": src["overview"], "references": t["references"],
            "flowTitle": src["flow"]["title"], "flowDesc": src["flow"]["description"],
            "diagram": diag,
        })
    old = json.load(open(ROOT / "src" / "library_data.json", encoding="utf-8"))
    names = {c["slug"]: U(c["name"]) for c in old["agentic_design"]}
    groups = []
    for g in tax["agentic_design_groups"]:
        groups.append({"name": g["name"], "es": g["es"], "cats": [
            {"slug": c, "name": names[c], "desc": tax["agentic_design_categories"][c], "techniques": by_cat[c]}
            for c in g["cats"]]})
    return groups, stats


def build_production(tax):
    pats = []
    stats = {"es": 0, "en": 0, "diagram": 0, "diag_from_en": 0}
    for f in sorted((LIB / "production_en").glob("*.json")):
        en = json.load(open(f, encoding="utf-8"))
        es = load_es("P", en["slug"])
        src = es or en
        stats["es" if es else "en"] += 1
        body = src["body"]
        # diagrama: el primero de la versión traducida; si no parsea igual que el original, usa el original
        diag, dsrc = None, None
        m_es, m_en = MERMAID.findall(body), MERMAID.findall(en["body"])
        if m_en:
            d_en = mermaid_diagram(m_en[0])
            d_es = mermaid_diagram(m_es[0]) if m_es else None
            ok = d_es and d_en and len(d_es["nodes"]) == len(d_en["nodes"]) and len(d_es["edges"]) == len(d_en["edges"])
            diag = d_es if ok else d_en
            if not ok:
                stats["diag_from_en"] += 1
            stats["diagram"] += 1
        sections = []
        for title, md in split_sections(MERMAID.sub("", body, count=1) if m_es or m_en else body):
            if not md.strip():
                continue
            base = re.sub(r"\s*\(.*\)$", "", title)
            if not es and base in SEC_ES:
                title = SEC_ES[base] + title[len(base):]
            sections.append({"title": title, "md": md})
        pats.append({"slug": en["slug"], "title": en["title"], "category": en["category"],
                     "lang": "es" if es else "en", "summary": src["summary"],
                     "signals": src.get("signals", []), "anti_signals": src.get("anti_signals", []),
                     "tags": en.get("tags", []), "source": en.get("source", ""), "based_on": en.get("based_on", []),
                     "sections": sections, "diagram": diag})
    cats = []
    for name, desc in tax["agentic_patterns_categories"].items():
        lst = [p for p in pats if p["category"] == name]
        if lst:
            cats.append({"name": name, "desc": desc, "patterns": lst})
    return cats, stats


def main():
    tax = json.load(open(LIB / "taxonomy_es.json", encoding="utf-8"))
    groups, ts = build_techniques(tax)
    prod, ps = build_production(tax)
    lib = {"groups": groups, "production": prod, "bridge": {k: list(v) for k, v in BRIDGE.items()}}
    js = "window.LIBRARY = " + json.dumps(lib, ensure_ascii=False, separators=(",", ":")) + ";\n"
    OUT.write_text(js, encoding="utf-8")
    nt = sum(len(c["techniques"]) for g in groups for c in g["cats"])
    print(f"OK library_data.js ({OUT.stat().st_size // 1024} KB)")
    print(f"  técnicas: {nt} (es={ts['es']}, en={ts['en']}), diagramas con avisos={ts['diag_issues']}")
    print(f"  producción: {sum(len(c['patterns']) for c in prod)} (es={ps['es']}, en={ps['en']}), "
          f"con diagrama={ps['diagram']}, diagrama desde original={ps['diag_from_en']}")


if __name__ == "__main__":
    main()
