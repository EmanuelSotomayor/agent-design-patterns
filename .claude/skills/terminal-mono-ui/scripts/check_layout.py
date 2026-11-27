#!/usr/bin/env python3
"""Verificación en navegador (Chromium headless) de una página con terminal-mono-ui.

Detecta los tres problemas que más aparecen al pasar una UI a fuente monoespaciada:
  1. errores de JavaScript,
  2. desborde horizontal de la página (algo empuja el ancho más allá de la ventana),
  3. texto recortado dentro de cajas de tamaño fijo (nodos de diagramas, tarjetas).

Uso:
  python3 check_layout.py index.html
  python3 check_layout.py index.html --widths 1440,760,500 \\
      --view "home:" --view "detalle:openItem('x')" \\
      --clip ".t-node,.node,.dnode,[data-check-clip]"

  --view NOMBRE:JS   código JS que deja la página en la vista a revisar (se repite).
                     Sin --view se revisa el estado inicial.
  --clip SELECTOR    elementos donde el texto no debe desbordar (por defecto el de arriba).
  --widths LISTA     anchos de ventana. Chromium headless no baja de ~500 px.

Sale con código 1 si encuentra problemas. Requiere chromium / chromium-browser / google-chrome.
Nota: Chromium instalado como snap no puede leer /tmp; por eso la copia temporal se crea
junto al archivo original y se borra al terminar.
"""
import html as H
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_CLIP = ".t-node,.node,.dnode,[data-check-clip]"


def find_chrome():
    for b in ("chromium-browser", "chromium", "google-chrome", "google-chrome-stable"):
        if shutil.which(b):
            return b
    sys.exit("No se encontró Chromium/Chrome en el PATH.")


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        print(__doc__); sys.exit(2)
    src = Path(args[0]).resolve()
    widths, views, clip = [1440, 760, 500], [], DEFAULT_CLIP
    i = 1
    while i < len(args):
        if args[i] == "--widths": widths = [int(x) for x in args[i + 1].split(",")]; i += 2
        elif args[i] == "--view": name, _, js = args[i + 1].partition(":"); views.append((name, js)); i += 2
        elif args[i] == "--clip": clip = args[i + 1]; i += 2
        else: sys.exit(f"argumento desconocido: {args[i]}")
    if not views:
        views = [("inicial", "")]

    harness = "<script>window.__errs=[];addEventListener('error',e=>__errs.push(String(e.message)));</script>"
    runner = """<script>
(async function(){
  const views = %s, clip = %s, R = {errors:[], views:{}};
  for (const [name, js] of views){
    try { if (js) (0, eval)(js); } catch(e){ R.errors.push(name + ': ' + e.message); }
    await new Promise(r => setTimeout(r, 150));
    const de = document.documentElement;
    const clipped = [];
    document.querySelectorAll(clip).forEach(el => {
      if (el.offsetParent === null && getComputedStyle(el).position !== 'fixed') return;
      if (el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1)
        clipped.push((el.innerText || '').trim().split('\\n')[0].slice(0, 50));
    });
    const wide = [];
    if (de.scrollWidth > de.clientWidth + 1){
      const W = de.clientWidth;
      document.querySelectorAll('body *').forEach(el => {
        const r = el.getBoundingClientRect(), p = el.parentElement && el.parentElement.getBoundingClientRect();
        if (r.width && r.right > W + 1 && p && p.right <= W + 1 && wide.length < 8)
          wide.push((el.className || el.tagName) + ' -> ' + Math.round(r.right) + 'px');
      });
    }
    R.views[name] = {pageWidth: de.scrollWidth, viewport: de.clientWidth, clipped, overflowCulprits: wide};
  }
  R.errors = R.errors.concat(window.__errs);
  const pre = document.createElement('pre'); pre.id = '__check'; pre.textContent = JSON.stringify(R);
  document.body.appendChild(pre);
})();
</script>""" % (json.dumps(views), json.dumps(clip))

    page = src.read_text(encoding="utf-8")
    page = re.sub(r"<head([^>]*)>", lambda m: m.group(0) + harness, page, count=1)
    page = page.replace("</body>", runner + "</body>", 1) if "</body>" in page else page + runner
    tmp = src.with_name(f"_check_{src.stem}.html")
    tmp.write_text(page, encoding="utf-8")
    chrome, problems = find_chrome(), 0
    try:
        for w in widths:
            out = subprocess.run([chrome, "--headless=new", "--disable-gpu", f"--window-size={w},1100",
                                  "--virtual-time-budget=8000", "--dump-dom", tmp.as_uri()],
                                 capture_output=True, text=True, timeout=300).stdout
            m = re.search(r'<pre id="__check">(.*?)</pre>', out, re.S)
            if not m:
                print(f"[{w}px] sin resultado (¿la página no terminó de cargar?)"); problems += 1; continue
            R = json.loads(H.unescape(m.group(1)))
            if R["errors"]:
                problems += len(R["errors"])
                print(f"[{w}px] errores JS: {R['errors'][:5]}")
            for name, v in R["views"].items():
                over = v["pageWidth"] > v["viewport"] + 1
                flag = "OK" if not over and not v["clipped"] else "PROBLEMA"
                print(f"[{w}px] {name:14s} ancho={v['pageWidth']}/{v['viewport']}  recortes={len(v['clipped'])}  {flag}")
                if over:
                    problems += 1
                    for c in v["overflowCulprits"]: print(f"      desborda: {c}")
                for c in v["clipped"][:8]:
                    problems += 1; print(f"      texto recortado: {c}")
    finally:
        tmp.unlink(missing_ok=True)
    print("TOTAL problemas:", problems)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
