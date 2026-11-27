"""
Reflection — autocrítica verbal con memoria episódica
El agente actúa, se autoevalúa con crítica VERBAL, guarda la reflexión
en memoria episódica, y reintenta con esa reflexión como contexto.

Implementación de referencia (ilustrativa).
"""


memory = []                      # buffer de reflexiones (memoria episódica)


def call_llm(messages):
    """Una llamada al modelo."""
    raise NotImplementedError


def act(task):
    """ACT: genera un intento condicionado por las reflexiones previas."""
    return call_llm([{"role": "user",
                      "content": f"Task: {task}\nPrior reflections: {memory}"}])


def self_reflect(task, attempt):
    """EVALUATE: crítica VERBAL (no un score) — qué falló y cómo mejorar."""
    return call_llm([{"role": "user",
                      "content": f"Task: {task}\nAttempt: {attempt}\n"
                                 "What went wrong and how to fix it?"}])


def reflexion(task, max_trials=3):
    for trial in range(max_trials):
        # 1) ACT: generar un intento
        attempt = act(task)

        # 2) EVALUATE: autocrítica verbal del intento
        critique = self_reflect(task, attempt)
        if "no issues" in critique.lower():
            return attempt

        # 3) MEMORIZE: guardar la reflexión en memoria episódica
        memory.append(critique)

    # 4) RETRY: reintentar con las reflexiones acumuladas (loop)
    return act(task)
