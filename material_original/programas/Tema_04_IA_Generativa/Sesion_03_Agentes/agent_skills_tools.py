"""
agent_skills_tools.py
====================================================================
Sesión 3 — Agentes, Skills y Tools con LangGraph
====================================================================

OBJETIVO DEL SCRIPT
--------------------------------------------------------------------
Este programa muestra una arquitectura agéntica sencilla, pero mucho
más rica que un flujo lineal.

En lugar de hacer siempre los mismos pasos, el sistema:

1. Analiza la intención de la pregunta
2. Decide si necesita una herramienta externa
3. Ejecuta esa herramienta si hace falta
4. Selecciona una "skill" de salida adecuada
5. Devuelve una respuesta con trazabilidad

Esto representa una idea central en sistemas modernos con LLM:

    el modelo no es el sistema;
    el modelo es un componente dentro de una arquitectura.

--------------------------------------------------------------------
QUÉ APRENDE EL ALUMNADO CON ESTE SCRIPT
--------------------------------------------------------------------
- Qué diferencia hay entre:
    * un flujo lineal
    * un agente con routing
- Qué es una tool
- Qué es una skill
- Cómo un grafo puede bifurcarse según el estado
- Cómo usar el LLM para tomar decisiones estructurales
- Cómo combinar:
    clasificación + selección de herramienta + generación final

--------------------------------------------------------------------
ARQUITECTURA GENERAL DEL FLUJO
--------------------------------------------------------------------

              ┌─────────────────┐
              │ intent_router   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ tool_router     │
              └───────┬─────────┘
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
 ┌─────────┐     ┌─────────┐       ┌─────────┐
 │ calc    │     │ rag     │       │  none   │
 └────┬────┘     └────┬────┘       └────┬────┘
      │               │                │
      └───────────────┴────────────────┘
                      ▼
               ┌─────────────┐
               │ skills_node │
               └──────┬──────┘
                      ▼
                     END

En otras palabras:
- primero se entiende la pregunta
- luego se decide si hace falta una herramienta
- por último se elige cómo responder

====================================================================
"""

# ------------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------------

# TypedDict permite definir la estructura del estado compartido.
# Literal restringe ciertos campos a un conjunto finito de valores.
from typing import TypedDict, Literal

# StateGraph permite construir un grafo de ejecución.
# END indica el final del flujo.
from langgraph.graph import StateGraph, END

# ChatPromptTemplate se usa para definir prompts parametrizados.
# StrOutputParser convierte la salida del modelo en texto plano.
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ------------------------------------------------------------------
# CONFIGURACIÓN DEL LLM
# ------------------------------------------------------------------
"""
Como en el ejemplo anterior, aquí usamos OpenAI por simplicidad.
También se deja comentada la opción local con Ollama.

temperature=0:
- favorece respuestas más estables
- es especialmente útil cuando el LLM se usa para routing
  o clasificación, no para creatividad
"""

# from langchain_ollama import ChatOllama
# llm = ChatOllama(model="llama3.2", temperature=0)

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ------------------------------------------------------------------
# PLACEHOLDER SOBRE RAG
# ------------------------------------------------------------------
"""
Este comentario es muy importante.

Aquí el script usa una "tool RAG" de mentira (placeholder)
para que el ejemplo funcione siempre, aunque no exista un retriever real.

Eso es útil en clase porque:
- simplifica el ejemplo
- evita depender de una base documental previa
- permite centrarse en la arquitectura del agente

Después, en una práctica más avanzada, este placeholder
puede sustituirse por un RAG real.
"""


# ------------------------------------------------------------------
# DEFINICIÓN DEL ESTADO
# ------------------------------------------------------------------
"""
Este estado ya es bastante más rico que el del flujo lineal.

Campos:

- question:
    pregunta original del usuario

- intent:
    intención detectada:
    * explain -> quiere explicación conceptual
    * procedure -> pide pasos o procedimiento
    * other -> cualquier otro caso

- tool_needed:
    herramienta requerida:
    * none -> no hace falta herramienta
    * rag -> hace falta recuperar documentos
    * calc -> hace falta un cálculo

- context:
    contexto externo producido por la tool
    (por ejemplo, resultado de RAG o de una operación)

- sources:
    fuentes asociadas a ese contexto

- answer:
    respuesta final del sistema

- steps:
    contador de pasos; sirve como control rudimentario
    para evitar crecimientos descontrolados
"""

class State(TypedDict):
    question: str
    intent: Literal["explain", "procedure", "other"]
    tool_needed: Literal["none", "rag", "calc"]
    context: str
    sources: str
    answer: str
    steps: int


# ------------------------------------------------------------------
# PROMPT 1: CLASIFICACIÓN DE INTENCIÓN
# ------------------------------------------------------------------
"""
Este prompt le pide al LLM que clasifique la intención
de la pregunta en UNA sola palabra.

Esto es importante porque el LLM aquí no está generando una respuesta final,
sino actuando como clasificador.

Las tres clases posibles son:
- explain
- procedure
- other

Este tipo de uso del LLM es muy habitual en agentes:
se le usa para tomar pequeñas decisiones estructurales.
"""

intent_prompt = ChatPromptTemplate.from_template(
    "Clasifica intención en UNA palabra: explain, procedure, other.\n"
    "- explain: definir y explicar un concepto.\n"
    "- procedure: pedir pasos o procedimiento.\n"
    "- other: resto.\n\n"
    "Pregunta: {q}\nIntent:"
)


# ------------------------------------------------------------------
# PROMPT 2: SELECCIÓN DE HERRAMIENTA
# ------------------------------------------------------------------
"""
Este segundo prompt hace otra tarea de routing:
decidir qué herramienta haría falta.

Posibles salidas:
- rag
- calc
- none

Idea muy importante:
el agente no usa siempre herramientas.
Primero decide si son necesarias.
"""

tool_prompt = ChatPromptTemplate.from_template(
    "Decide herramienta en UNA palabra: rag, calc, none.\n"
    "- rag: si necesitas normativa/documentos.\n"
    "- calc: si hay operación numérica.\n"
    "- none: si no.\n\n"
    "Pregunta: {q}\nTool:"
)


# ------------------------------------------------------------------
# NODO 1: intent_router
# ------------------------------------------------------------------
"""
Este nodo:

1. incrementa el contador de pasos
2. llama al modelo con el prompt de intención
3. valida que la salida sea una de las etiquetas permitidas
4. guarda la intención en el estado

Observación:
aunque el LLM pueda generar cualquier cosa, aquí se fuerza
una validación mínima:
si sale algo raro -> se cae a "other"
"""

def intent_router(state: State) -> State:
    # Incrementamos el contador de pasos
    state["steps"] += 1

    # Ejecutamos el clasificador de intención
    label = (
        intent_prompt | llm | StrOutputParser()
    ).invoke({"q": state["question"]}).strip().lower()

    # Validamos la etiqueta
    state["intent"] = label if label in ("explain", "procedure", "other") else "other"

    print("[intent_router]", state["intent"])
    return state


# ------------------------------------------------------------------
# NODO 2: tool_router
# ------------------------------------------------------------------
"""
Este nodo decide si hace falta una herramienta.

No produce todavía la respuesta final.
Solo actualiza el campo state["tool_needed"].

Observación:
aquí el LLM está actuando como "selector de herramientas".
Esto es un patrón central en arquitecturas agénticas.
"""

def tool_router(state: State) -> State:
    t = (
        tool_prompt | llm | StrOutputParser()
    ).invoke({"q": state["question"]}).strip().lower()

    if "rag" in t:
        state["tool_needed"] = "rag"
    elif "calc" in t:
        state["tool_needed"] = "calc"
    else:
        state["tool_needed"] = "none"

    print("[tool_router]", state["tool_needed"])
    return state


# ------------------------------------------------------------------
# TOOL 1: calc_tool
# ------------------------------------------------------------------
"""
Esta tool intenta resolver operaciones numéricas simples.

Qué hace:
1. Limpia la pregunta dejando solo caracteres matemáticos
2. Evalúa la expresión
3. Guarda el resultado en el campo context
4. Añade una fuente simbólica

Observación crítica para clase:
- esto NO es una calculadora segura en producción real
- se usa aquí como ejemplo mínimo
- eval() está encapsulado con __builtins__ vacíos para reducir riesgos,
  pero en sistemas reales se debería usar una librería matemática segura

Ejemplo:
Pregunta: "¿Cuánto es (8+2)*3?"
Resultado:
context = "Resultado cálculo: 30"
"""

def calc_tool(state: State) -> State:
    import re

    # Nos quedamos solo con caracteres matemáticos básicos
    expr = re.sub(r"[^0-9\+\-\*\/\.\(\) ]", "", state["question"])

    try:
        # Evaluamos la expresión en un entorno muy restringido
        val = eval(expr, {"__builtins__": {}})

        state["context"] = f"Resultado cálculo: {val}"
        state["sources"] = "- calc_tool"

    except:
        # Si algo falla, dejamos el contexto vacío
        state["context"] = ""
        state["sources"] = "- calc_tool (fallo)"

    return state


# ------------------------------------------------------------------
# TOOL 2: rag_tool
# ------------------------------------------------------------------
"""
Esta tool es un placeholder.

No hace RAG real, solo simula que ha recuperado contexto.

Esto permite:
- mantener la arquitectura del agente
- enseñar el patrón sin complicar el ejemplo
- sustituir después esta función por un retriever real

Si más adelante quieres integrarlo con la práctica de RAG,
aquí es donde lo harías.
"""

def rag_tool(state: State) -> State:
    # Placeholder: sustituye por RAG real (retriever.invoke + fuentes) cuando quieras.
    state["context"] = "Contexto recuperado (placeholder). Sustituye por tu RAG real."
    state["sources"] = "- (placeholder)"
    return state


# ------------------------------------------------------------------
# PROMPTS DE LAS SKILLS
# ------------------------------------------------------------------
"""
Aquí aparece un concepto muy importante:
una tool y una skill NO son lo mismo.

- Tool:
    obtiene o produce información externa
    (por ejemplo, un cálculo o un retrieval)

- Skill:
    define cómo convertir esa información en una respuesta útil

En este script hay tres skills:
1. explain -> explicación pedagógica
2. procedure -> checklist paso a paso
3. other -> respuesta general

Esto es muy pedagógico porque muestra que:
la respuesta final no depende solo de “tener contexto”,
sino también del formato y del propósito.
"""

explainer_prompt = ChatPromptTemplate.from_template(
    "Genera una explicación pedagógica en español con este formato:\n"
    "Definición: ...\n"
    "Ejemplo: ...\n"
    "Advertencia: ...\n\n"
    "Usa el contexto si existe.\n"
    "Pregunta: {q}\nContexto: {ctx}\n\nRespuesta:"
)

checklist_prompt = ChatPromptTemplate.from_template(
    "Genera una checklist (máx. 6 pasos) para el procedimiento solicitado.\n"
    "Usa el contexto si existe.\n"
    "Pregunta: {q}\nContexto: {ctx}\n\nChecklist:"
) 

other_prompt = ChatPromptTemplate.from_template(
    "Responde de forma clara y breve. Usa el contexto si existe.\n"
    "Pregunta: {q}\nContexto: {ctx}\n\nRespuesta:"
)


# ------------------------------------------------------------------
# NODO FINAL: skills_node
# ------------------------------------------------------------------
"""
Este nodo es el que realmente formula la respuesta final.

Qué hace:
1. comprueba si hay demasiados pasos
2. mira la intención detectada
3. elige el prompt/skill correspondiente
4. genera la respuesta usando el contexto si existe
5. añade fuentes si el modelo no las ha incluido

Esto es un punto clave:
el agente no responde “siempre igual”.
Adapta su salida al tipo de pregunta.

Por ejemplo:
- una pregunta conceptual -> explicación estructurada
- una pregunta procedimental -> checklist
"""

def skills_node(state: State) -> State:
    # Control rudimentario del número de pasos
    if state["steps"] > 8:
        state["answer"] = "max_steps alcanzado. Reformula la pregunta o reduce el alcance."
        return state

    # Selección de skill según la intención
    if state["intent"] == "explain":
        out = (
            explainer_prompt | llm | StrOutputParser()
        ).invoke({"q": state["question"], "ctx": state["context"]})

    elif state["intent"] == "procedure":
        out = (
            checklist_prompt | llm | StrOutputParser()
        ).invoke({"q": state["question"], "ctx": state["context"]})

    else:
        out = (
            other_prompt | llm | StrOutputParser()
        ).invoke({"q": state["question"], "ctx": state["context"]})

    # Añadimos fuentes si el modelo no las escribió
    if "Fuentes:" not in out:
        out = out.rstrip() + "\n\nFuentes:\n" + (state["sources"] if state["sources"] else "- (ninguna)")

    state["answer"] = out
    return state


# ------------------------------------------------------------------
# FUNCIÓN DE ROUTING CONDICIONAL
# ------------------------------------------------------------------
"""
Esta función es muy pequeña, pero conceptualmente importante.

Devuelve el valor de state["tool_needed"] para que LangGraph
sepa qué rama tomar.

Es decir:
- si tool_needed == "calc" -> ir al nodo calc
- si tool_needed == "rag"  -> ir al nodo rag
- si tool_needed == "none" -> ir directamente a skills
"""

def route_tool(state: State):
    return state["tool_needed"]


# ------------------------------------------------------------------
# CONSTRUCCIÓN DEL GRAFO
# ------------------------------------------------------------------
"""
Primero se crea el grafo.
Después se añaden nodos.
Luego se define el flujo.

Este ejemplo ya no es lineal:
tiene una bifurcación condicional después de tool_router.
"""

g = StateGraph(State)

g.add_node("intent_router", intent_router)
g.add_node("tool_router", tool_router)
g.add_node("calc", calc_tool)
g.add_node("rag", rag_tool)
g.add_node("skills", skills_node)


# ------------------------------------------------------------------
# DEFINICIÓN DEL FLUJO
# ------------------------------------------------------------------
"""
Orden de ejecución:

1. intent_router
2. tool_router
3. según tool_needed:
   - calc -> calc
   - rag  -> rag
   - none -> skills
4. si se pasó por calc o rag, luego skills
5. skills -> END

Esto ilustra por primera vez un verdadero routing.
"""

g.set_entry_point("intent_router")
g.add_edge("intent_router", "tool_router")

g.add_conditional_edges(
    "tool_router",
    route_tool,
    {
        "calc": "calc",
        "rag": "rag",
        "none": "skills"
    }
)

g.add_edge("calc", "skills")
g.add_edge("rag", "skills")
g.add_edge("skills", END)


# ------------------------------------------------------------------
# COMPILACIÓN DEL GRAFO
# ------------------------------------------------------------------
"""
compile() transforma la definición del grafo
en una aplicación ejecutable.
"""
app = g.compile()


# ------------------------------------------------------------------
# BLOQUE DE PRUEBAS
# ------------------------------------------------------------------
"""
Probamos tres tipos de preguntas:

1. explain:
   "Explica qué es RAG y para qué sirve."

2. procedure:
   "¿Cómo entregar las prácticas paso a paso?"

3. calc:
   "¿Cuánto es (8+2)*3?"

Esto es excelente para clase porque permite mostrar
cómo cambia el recorrido del grafo según la pregunta.
"""

if __name__ == "__main__":
    tests = [
        "Explica qué es RAG y para qué sirve.",
        "¿Cómo entregar las prácticas paso a paso?",
        "¿Cuánto es (8+2)*3?"
    ]

    for t in tests:
        print("\n========================")
        print("Q:", t)

        out = app.invoke({
            "question": t,
            "intent": "other",
            "tool_needed": "none",
            "context": "",
            "sources": "",
            "answer": "",
            "steps": 0
        })

        print("A:", out["answer"])