"""
ReAct — "Razonar y actuar"
Bucle Reasoning + Acting: el agente alterna un paso de razonamiento (Thought)
con una llamada a herramienta (Action) y su resultado (Observation),
hasta poder dar una respuesta final.

Implementación de referencia (ilustrativa, no es código del repo original).
"""


def call_llm(messages, tools=None):
    """Una llamada al modelo. Devuelve texto + posible llamada a tool."""
    # En producción: client.messages.create(model=..., messages=..., tools=tools)
    raise NotImplementedError


def parse(reply):
    """Separa el Thought, la Action y la Final Answer de la respuesta."""
    thought = reply.split("Thought:")[-1].split("Action:")[0].strip()
    action = reply.split("Action:")[-1].split("Observation:")[0].strip()
    answer = reply.split("Final Answer:")[-1].strip() if "Final Answer:" in reply else None
    return thought, action, answer


def react(question, tools, max_steps=6):
    """Ejecuta el bucle ReAct: Thought -> Action -> Observation -> ... -> Answer."""
    trace = []                                   # historial (debug + contexto)
    context = f"Question: {question}"

    for step in range(max_steps):
        # 1) RAZONAR: el modelo produce un Thought y decide Action o Answer
        reply = call_llm([{"role": "user", "content": context}], tools=tools)
        thought, action, answer = parse(reply)
        trace.append(("thought", thought))

        # 2) TERMINAR si ya hay respuesta final
        if answer:
            return answer, trace

        # 3) ACTUAR: ejecutar la herramienta elegida
        name, arg = action.split("[", 1)[0], action.split("[", 1)[1].rstrip("]")
        observation = tools[name](arg)
        trace.append(("action", action))
        trace.append(("observation", observation))

        # 4) OBSERVAR: devolver el resultado al contexto para el siguiente paso
        context += f"\nThought: {thought}\nAction: {action}\nObservation: {observation}"

    return None, trace                            # se agotaron los pasos sin respuesta
