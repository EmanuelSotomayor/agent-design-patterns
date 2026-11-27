"""
Plan-Then-Execute — planificar antes de ejecutar
El LLM fija el plan completo ANTES de ejecutar, y luego ejecuta los pasos
sin re-planificar (o con re-plan mínimo). Los outputs de las herramientas
solo cambian parámetros, no la secuencia.

Implementación de referencia (ilustrativa).
"""


def call_llm(messages, tool=None):
    """Una llamada al modelo con salida estructurada (tool_choice)."""
    raise NotImplementedError


def build_plan(goal):
    """PLAN: el planificador produce la secuencia completa de pasos."""
    reply = call_llm([{"role": "user", "content": f"Plan for: {goal}"}], tool="plan")
    return reply["steps"]          # -> [ {tool, args}, {tool, args}, ... ]


def execute_plan(plan, tools):
    """EXECUTE: ejecuta los pasos del plan en orden, sin re-planificar."""
    results = []
    for step in plan:
        output = tools[step["tool"]](step["args"])
        results.append(output)
    return results


def verify(goal, results):
    """VERIFY: comprueba el resultado final contra el objetivo."""
    reply = call_llm([{"role": "user",
                       "content": f"Goal: {goal}\nResults: {results}\nAchieved?"}])
    return reply.lower().startswith("yes")


def plan_then_execute(goal, tools):
    # 1) PLAN: fijar la secuencia completa de acciones
    plan = build_plan(goal)

    # 2) EXECUTE: ejecutar cada paso en orden
    results = execute_plan(plan, tools)

    # 3) VERIFY: si falla, replanificar una sola vez
    if not verify(goal, results):
        plan = build_plan(f"{goal} (retry after: {results})")
        results = execute_plan(plan, tools)

    return results
