"""
Talker-Reasoner (Dual-Speed Realtime) — "responder ya, pensar en segundo plano"
Un Talker rápido responde al instante; un Reasoner lento planifica y llama
herramientas en background; comparten un belief state como único acoplamiento.

Implementación de referencia (ilustrativa).
"""


belief = {}                      # estado compartido entre Talker y Reasoner


def call_llm(messages, model="fast"):
    """Una llamada al modelo. `fast` (Talker) vs `slow` (Reasoner)."""
    raise NotImplementedError


def talker(user_msg):
    """TALKER: responde de inmediato con lo que se sabe hasta ahora."""
    return call_llm([
        {"role": "user", "content": user_msg},
        {"role": "system", "content": f"Belief: {belief}"},
    ], model="fast")


def reasoner(user_msg):
    """REASONER: descompone, llama herramientas y escribe el belief state."""
    plan = call_llm([{"role": "user", "content": user_msg}], model="slow")
    for step in plan["steps"]:
        belief[step["key"]] = execute(step)       # escribe hallazgos


def execute(step):
    """Ejecuta una herramienta y devuelve su resultado."""
    raise NotImplementedError


def run(user_msg):
    # 1) TALKER: responder al instante (baja latencia)
    answer = talker(user_msg)

    # 2) REASONER: trabajar en segundo plano (no bloquea la respuesta)
    reasoner(user_msg)            # en producción: thread/worker separado

    # 3) TALKER: refinar la respuesta con el belief ya actualizado
    return talker(user_msg)
