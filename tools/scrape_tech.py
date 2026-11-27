"""Descarga (con caché) las 288 páginas de técnicas de agentic-design.ai."""
import json, sys, time, urllib.request
from pathlib import Path

S = Path(sys.argv[1])
LIB = json.load(open(sys.argv[2], encoding="utf-8"))
CACHE = S / "raw" / "tech"
CACHE.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) pattern-collector/1.0"}

todo = [(c["slug"], t["slug"]) for c in LIB["agentic_design"] for t in c["techniques"]]
ok = fail = 0
for i, (cat, tech) in enumerate(todo, 1):
    f = CACHE / f"{cat}__{tech}.html"
    if f.exists() and f.stat().st_size > 10000:
        ok += 1
        continue
    url = f"https://agentic-design.ai/patterns/{cat}/{tech}"
    for attempt in range(3):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
            f.write_bytes(data)
            ok += 1
            break
        except Exception as e:
            if attempt == 2:
                print("FALLO", url, e)
                fail += 1
            time.sleep(2)
    time.sleep(0.35)
    if i % 25 == 0:
        print(f"{i}/{len(todo)}", flush=True)
print(f"OK={ok} FALLOS={fail} total={len(todo)}")
