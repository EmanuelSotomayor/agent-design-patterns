#!/usr/bin/env python3
"""Inyecta el código fuente completo de cada patrón en index.html,
junto con el mapeo de líneas resaltadas (hl) por paso.

Lee las fuentes desde ./src y escribe el resultado en ./index.html.
Es idempotente: elimina cualquier inyección previa antes de volver a inyectar.

Ejecutar:  python3 build.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"

# Archivo fuente y nombre a mostrar por cada patrón
SOURCES = {
    "chaining":       ("src/01_prompt_chaining.py",        "01_prompt_chaining.py"),
    "routing":        ("src/01_routing.py",                "01_routing.py"),
    "parallelization":("src/01_parallelization.py",        "01_parallelization.py"),
    "orchestrator":   ("src/01_orchestrator_workers.py",   "01_orchestrator_workers.py"),
    "evaluator":      ("src/01_evaluator_optimizer.py",    "01_evaluator_optimizer.py"),
    "hitl":           ("src/01_human_in_the_loop.py",      "01_human_in_the_loop.py"),
    "contentwriter":  ("src/content_writer_agent.py",      "content_writer/agent.py"),
    "react":          ("src/ref/08_react.py",              "08_react.py"),
    "mapreduce":      ("src/ref/09_map_reduce.py",         "09_map_reduce.py"),
    "planthenexecute":("src/ref/10_plan_then_execute.py",  "10_plan_then_execute.py"),
    "talkerreasoner": ("src/ref/11_talker_reasoner.py",    "11_talker_reasoner.py"),
    "reflexion":      ("src/ref/12_reflexion.py",          "12_reflexion.py"),
}

# Rangos de líneas (1-based, inclusivos) resaltados en cada paso.
# El orden de las sub-listas coincide con el orden de `steps` de cada patrón.
HL = {
    "chaining": [
        [[151, 153], [172, 178]],                       # Outline
        [[111, 149], [155, 162], [180, 185]],           # Write (+ agentic loop)
        [[164, 166], [187, 191]],                       # Edit
        [[242, 246]],                                   # Salida
    ],
    "routing": [
        [[159, 175], [275, 281]],                       # Classify
        [[283, 297]],                                   # Route
        [[179, 184], [209, 214], [241, 246]],           # cadena paso 1
        [[186, 192], [217, 223], [249, 255]],           # cadena paso 2
        [[194, 199], [225, 230], [257, 262]],           # cadena paso 3
        [[356, 360]],                                   # Salida
    ],
    "parallelization": [
        [[129, 147]],                                   # Fan-out
        [[137, 147]],                                   # Fan-in
        [[256, 263]],                                   # Combinar
        [[149, 165]],                                   # Votación candidatos
        [[115, 122], [167, 171]],                       # Evaluar
        [[173, 174]],                                   # Ganador
    ],
    "orchestrator": [
        [[144, 162], [191, 197]],                       # Planificar
        [[199, 206]],                                   # Delegar
        [[164, 174], [203, 215]],                       # Investigar
        [[176, 185], [218, 222]],                       # Sintetizar
        [[285, 288]],                                   # Salida
    ],
    "evaluator": [
        [[183, 196], [242, 246]],                       # Research
        [[198, 201], [248, 251]],                       # Write
        [[218, 236], [253, 269]],                       # Evaluate
        [[271, 280]],                                   # Decisión
        [[203, 216], [275, 278]],                       # Refine
        [[282, 282]],                                   # Salida
    ],
    "hitl": [
        [[69, 71], [82, 85]],                           # Redactar
        [[87, 98], [122, 148]],                         # Checkpoint 1
        [[73, 76], [100, 104]],                         # Revisar
        [[106, 117]],                                   # Checkpoint 2
        [[118, 119]],                                   # Salida
    ],
    "contentwriter": [
        [[241, 247], [462, 465]],                       # Classify
        [[467, 482]],                                   # HC1
        [[249, 264], [484, 489]],                       # Plan
        [[161, 217], [277, 286], [491, 514]],           # Research (+ agentic loop)
        [[288, 329], [521, 527]],                       # Write
        [[331, 340], [529, 532]],                       # Evaluate
        [[534, 563]],                                   # Decisión
        [[536, 560]],                                   # Refine
        [[565, 624]],                                   # HC3
        [[368, 386], [643, 651]],                       # Social
        [[409, 433], [653, 658]],                       # SEO
        [[626, 638], [660, 673]],                       # Complete
    ],
    "react": [
        [[30, 34]],                                     # Pensar (Thought)
        [[40, 44]],                                     # Actuar (Action)
        [[46, 47]],                                     # Observar (Observation)
        [[25, 49]],                                     # Loop completo
        [[36, 38]],                                     # Responder (Final Answer)
    ],
    "mapreduce": [
        [[17, 18], [33, 34]],                           # Split
        [[22, 24], [36, 38]],                           # Map (paralelo)
        [[27, 29], [40, 41]],                           # Reduce
        [[32, 41]],                                     # Pipeline completo / Salida
    ],
    "planthenexecute": [
        [[16, 18], [39, 40]],                           # Planificar
        [[22, 24], [42, 43]],                           # Ejecutar
        [[31, 32], [45, 46]],                           # Verificar
        [[45, 48]],                                     # Re-planificar si falla
        [[50, 50]],                                     # Salida
    ],
    "talkerreasoner": [
        [[18, 23], [39, 40]],                           # Talker responde
        [[26, 29], [42, 43]],                           # Reasoner planifica (background)
        [[26, 30], [10, 10]],                           # Reasoner actualiza belief
        [[18, 23], [45, 46]],                           # Talker refina
    ],
    "reflexion": [
        [[18, 21], [33, 34]],                           # Act
        [[24, 28], [36, 37]],                           # Self-reflect (evaluar)
        [[10, 10], [41, 42]],                           # Memorizar
        [[31, 32], [44, 45]],                           # Reintentar (loop)
        [[38, 39]],                                     # Salida
    ],
}


def strip_injections(html: str) -> str:
    """Elimina bloques de código fuente y script de datos inyectados previamente."""
    # bloques de código fuente (type=text/plain)
    html = re.sub(
        r'\n?<script type="text/plain" id="src-[^"]*">.*?</script>',
        "", html, flags=re.S,
    )
    # scripts de asignación de datos (con marcadores)
    html = re.sub(
        r'\n?<script>\s*/\*__HL_DATA_BEGIN__\*/.*?/\*__HL_DATA_END__\*/\s*</script>',
        "", html, flags=re.S,
    )
    # scripts de asignación antiguos (sin marcadores): cualquier <script> con CODE_FILES
    html = re.sub(
        r'\n?<script>\s*\(function\(\)\{\s*var CODE_FILES\s*=.*?</script>',
        "", html, flags=re.S,
    )
    return html


def main():
    html = INDEX.read_text(encoding="utf-8")
    html = strip_injections(html)

    code_files = {}
    blocks = []
    for pid, (rel, display) in SOURCES.items():
        src = (ROOT / rel).read_text(encoding="utf-8")
        src = src.lstrip("\ufeff").rstrip("\n") + "\n"
        code_files[pid] = display
        blocks.append(f'<script type="text/plain" id="src-{pid}">{src}</script>')

    src_injection = "\n".join(blocks) + "\n"
    data_injection = (
        "<script>\n"
        "/*__HL_DATA_BEGIN__*/\n"
        "(function(){\n"
        f"  var CODE_FILES = {json.dumps(code_files)};\n"
        f"  var CODE_HL = {json.dumps(HL)};\n"
        "  PATTERNS.forEach(function(p){\n"
        "    p.codeFile = CODE_FILES[p.id];\n"
        "    p.srcId = 'src-' + p.id;\n"
        "    var hl = CODE_HL[p.id] || [];\n"
        "    p.steps.forEach(function(s,i){ s.hl = hl[i] || []; });\n"
        "  });\n"
        "})();\n"
        "/*__HL_DATA_END__*/\n"
        "</script>\n"
    )

    assert '<div id="main"></div>' in html, "no se encontró #main"
    html = html.replace('<div id="main"></div>', '<div id="main"></div>\n' + src_injection, 1)
    assert "</body>" in html, "no se encontró </body>"
    html = html.replace("</body>", data_injection + "</body>", 1)

    INDEX.write_text(html, encoding="utf-8")
    total = sum(len((ROOT / rel).read_text(encoding="utf-8").splitlines()) for rel, _ in SOURCES.values())
    print(f"OK: {len(blocks)} bloques de código inyectados ({total} líneas totales).")


if __name__ == "__main__":
    main()
