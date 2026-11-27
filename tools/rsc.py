"""Decodifica el payload RSC de Next.js (self.__next_f.push) y extrae objetos JSON."""
import json, re


def rsc_text(html):
    parts = []
    for m in re.finditer(r'self\.__next_f\.push\(\[1,"((?:[^"\\]|\\.)*)"\]\)', html, re.S):
        parts.append(json.loads('"' + m.group(1) + '"'))
    return "".join(parts)


def extract_object(text, start):
    """Devuelve el objeto JSON balanceado que empieza en text[start] == '{'."""
    depth, i, in_str, esc = 0, start, False, False
    while i < len(text):
        c = text[i]
        if in_str:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == '"': in_str = False
        else:
            if c == '"': in_str = True
            elif c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(text[start:i + 1])
        i += 1
    raise ValueError("objeto sin cerrar")


def find_enclosing_with_key(text, key, must=()):
    """Busca el objeto más chico que contiene `"key":` y todas las claves en `must`."""
    k = text.find(f'"{key}":')
    if k < 0:
        return None
    # retrocede hasta encontrar un '{' cuyo objeto contenga la clave y las requeridas
    i = k
    while i > 0:
        i = text.rfind("{", 0, i)
        if i < 0:
            return None
        try:
            obj = extract_object(text, i)
        except Exception:
            continue
        if key in obj and all(m in obj for m in must):
            return obj
    return None
