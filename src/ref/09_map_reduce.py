"""
Map-Reduce — procesar documentos largos
Divide el input en chunks, procesa cada chunk con un LLM en paralelo (map)
y agrega los resultados (reduce) con código determinista o un LLM final.

Implementación de referencia (ilustrativa).
"""

from concurrent.futures import ThreadPoolExecutor


def call_llm(messages, system):
    """Una llamada al modelo con salida restringida."""
    raise NotImplementedError


def chunk_text(text, max_chars=4000):
    """SPLIT: divide el texto en trozos que caben en la ventana de contexto."""
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]


def map_chunk(chunk, system):
    """MAP: procesa UN chunk con una llamada LLM de salida restringida."""
    return call_llm([{"role": "user", "content": chunk}], system=system)


def reduce_results(partials):
    """REDUCE: agrega los resultados parciales (código determinista o un LLM)."""
    return "\n\n".join(p.get("summary", "") for p in partials)


def map_reduce(document, map_prompt):
    # 1) SPLIT: dividir el documento en chunks independientes
    chunks = chunk_text(document)

    # 2) MAP: procesar cada chunk en paralelo (sin dependencias entre sí)
    with ThreadPoolExecutor(max_workers=len(chunks)) as pool:
        partials = list(pool.map(lambda c: map_chunk(c, map_prompt), chunks))

    # 3) REDUCE: agregar todos los resultados en una salida única
    return reduce_results(partials)
