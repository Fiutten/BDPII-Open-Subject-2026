"""
flow_lineal.py
====================================================================
Ejemplo docente de flujo lineal con LangGraph
====================================================================

OBJETIVO DEL SCRIPT
--------------------------------------------------------------------
Este programa muestra la forma más sencilla de construir un flujo
de trabajo con LangGraph.

La idea pedagógica es que el alumnado vea que:

1. Un sistema con LLM no tiene por qué ser una sola llamada al modelo.
2. Podemos dividir el proceso en etapas bien definidas.
3. Cada etapa transforma un estado compartido.
4. LangGraph permite representar ese proceso como un grafo de nodos.

En este ejemplo el flujo es completamente lineal:

    pregunta del usuario
            ↓
       preprocess
            ↓
       llm_answer
            ↓
       postprocess
            ↓
            END

Esto es útil porque permite introducir conceptos clave de agentes y
arquitecturas compuestas sin empezar todavía con bifurcaciones,
tools, memoria avanzada o reintentos.

--------------------------------------------------------------------
QUÉ APRENDE EL ALUMNADO CON ESTE SCRIPT
--------------------------------------------------------------------
- Qué es un "estado" en LangGraph
- Cómo se definen nodos
- Cómo cada nodo modifica el estado
- Cómo se conectan los nodos
- Cómo se compila y ejecuta el grafo
- Cómo separar preprocesado, generación y postprocesado

====================================================================
"""

# ------------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------------

# TypedDict se usa para definir la estructura del estado compartido.
# Es una forma muy útil de documentar qué campos debe tener el estado.
from typing import TypedDict

# StateGraph permite construir el grafo de ejecución.
# END es un marcador especial que indica final del flujo.
from langgraph.graph import StateGraph, END

# ChatPromptTemplate sirve para construir prompts parametrizados.
# StrOutputParser convierte la salida del modelo en un string normal.
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ------------------------------------------------------------------
# CONFIGURACIÓN DEL LLM
# ------------------------------------------------------------------
"""
En esta parte elegimos el modelo que se encargará de generar la respuesta.

Hay dos opciones planteadas:

1. Ollama local
   - útil si queremos ejecutar el laboratorio sin depender de una API externa
   - interesante en entornos docentes donde se busca autonomía local

2. OpenAI
   - más sencillo si ya tenemos clave API y queremos estabilidad rápida

En este ejemplo queda activada la opción OpenAI.
"""

# ===== LLM (Ollama por defecto) =====
# Si se quisiera usar un modelo local con Ollama, bastaría con
# descomentar estas líneas y comentar las de OpenAI.
#
# from langchain_ollama import ChatOllama
# llm = ChatOllama(model="llama3.2", temperature=0)

# Si prefieres OpenAI:
# load_dotenv() carga automáticamente las variables del archivo .env
# situado en el directorio de trabajo.
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

# temperature=0 reduce la variabilidad de las respuestas.
# En docencia y en sistemas analíticos esto suele ser conveniente,
# porque queremos comportamiento más estable y menos "creativo".
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ------------------------------------------------------------------
# DEFINICIÓN DEL ESTADO
# ------------------------------------------------------------------
"""
El estado es el objeto central del grafo.

En LangGraph, cada nodo recibe el estado actual, lo modifica y
devuelve la nueva versión del estado.

Aquí definimos un estado muy simple con tres campos:

- question:
    pregunta original introducida por el usuario

- normalized_question:
    versión normalizada de la pregunta (minúsculas, espacios limpiados)

- answer:
    respuesta final generada por el sistema

Es importante remarcar al alumnado que el estado:
- no es una variable suelta
- no es solo “memoria”
- es la representación explícita del proceso en ejecución
"""

class State(TypedDict):
    question: str
    normalized_question: str
    answer: str


# ------------------------------------------------------------------
# NODO 1: PREPROCESS
# ------------------------------------------------------------------
"""
Este nodo hace un preprocesado mínimo de la entrada.

¿Qué hace exactamente?

1. Recupera la pregunta original
2. Elimina espacios al inicio y al final con strip()
3. Convierte a minúsculas
4. Normaliza espacios internos:
   si el usuario ha puesto varios espacios seguidos, se reducen a uno

¿Por qué hacerlo?
- para homogenizar la entrada
- para evitar pequeñas variaciones superficiales
- para ilustrar que un flujo con LLM suele empezar con preparación del input

Muy importante didácticamente:
este nodo NO llama al modelo.
Es una etapa separada, determinista y controlable.
"""

def preprocess(state: State) -> State:
    # Recuperamos la pregunta original
    q = state["question"].strip()

    # lower() pasa todo a minúsculas
    # split() divide por espacios
    # " ".join(...) vuelve a unir con un solo espacio entre palabras
    state["normalized_question"] = " ".join(q.lower().split())

    # Print de depuración para ver cómo queda la pregunta transformada
    print("[preprocess] normalized_question:", state["normalized_question"])

    # Devolvemos el estado ya modificado
    return state


# ------------------------------------------------------------------
# PROMPT DEL SISTEMA
# ------------------------------------------------------------------
"""
Aquí definimos el prompt que usará el nodo generativo.

Se pide explícitamente un formato:

    Título: <una línea>
    - bullet 1
    - bullet 2
    - bullet 3

Esto es importante porque:
- restringe la salida
- facilita evaluar el resultado
- muestra al alumnado que el prompt no es solo “preguntar algo”
- convierte la llamada al modelo en una tarea más estructurada

Observación docente:
el prompt usa {q}, que será reemplazado por la pregunta normalizada.
"""

prompt = ChatPromptTemplate.from_template(
    "Responde con este formato exacto:\n"
    "Título: <una línea>\n"
    "- bullet 1\n"
    "- bullet 2\n"
    "- bullet 3\n\n"
    "Pregunta: {q}"
)


# ------------------------------------------------------------------
# NODO 2: LLM_ANSWER
# ------------------------------------------------------------------
"""
Este nodo es el núcleo generativo del flujo.

¿Qué hace?

1. Toma la pregunta ya normalizada desde el estado
2. La inserta en el prompt
3. Llama al modelo
4. Convierte la salida a string
5. Guarda la respuesta en state["answer"]

Línea clave:
    (prompt | llm | StrOutputParser()).invoke(...)

Esto usa LCEL (LangChain Expression Language), que permite
encadenar componentes con el operador |.

Interpretación:
- prompt construye el mensaje
- llm genera la respuesta
- StrOutputParser la convierte en texto plano
"""

def llm_answer(state: State) -> State:
    out = (prompt | llm | StrOutputParser()).invoke(
        {"q": state["normalized_question"]}
    )

    # Guardamos la salida en el estado
    state["answer"] = out

    # Print de depuración: longitud de la respuesta generada
    print("[llm_answer] chars:", len(out))

    return state


# ------------------------------------------------------------------
# NODO 3: POSTPROCESS
# ------------------------------------------------------------------
"""
Este nodo realiza un postprocesado muy simple.

No mejora “inteligentemente” la respuesta, pero sí añade una
pequeña capa de evaluación.

¿Qué hace?

1. Limpia espacios sobrantes de la respuesta
2. Construye una mini-lista de indicadores de calidad
3. Añade esos indicadores al final

Esto es útil porque enseña algo muy importante:
después de generar texto, muchas veces el sistema necesita
hacer verificaciones, validaciones o enriquecimiento.

Aquí la evaluación es mínima, pero conceptualmente abre la puerta a:
- validación de longitud
- validación de formato
- chequeos semánticos
- puntuaciones de calidad
"""

def postprocess(state: State) -> State:
    # Recuperamos la respuesta; si no existe, usamos cadena vacía
    a = state.get("answer", "").strip()

    # Lista donde guardaremos indicadores simples de calidad
    quality = []

    # Comprobación 1: ¿hay respuesta?
    quality.append("✅ hay respuesta" if a else "❌ sin respuesta")

    # Comprobación 2: ¿tiene un tamaño razonable?
    # Aquí se considera "clara" si no está vacía y no supera 900 caracteres
    quality.append("✅ es clara" if (0 < len(a) < 900) else "⚠️ demasiado larga o vacía")

    # Sobrescribimos el campo answer añadiendo el bloque de calidad
    state["answer"] = a + "\n\nCalidad:\n- " + "\n- ".join(quality)

    print("[postprocess] done")
    return state


# ------------------------------------------------------------------
# CONSTRUCCIÓN DEL GRAFO
# ------------------------------------------------------------------
"""
Aquí montamos el flujo en LangGraph.

Primero se crea un grafo basado en el tipo de estado definido:
    g = StateGraph(State)

Después añadimos nodos:
- preprocess
- llm_answer
- postprocess

Cada nodo tiene:
- un nombre dentro del grafo
- una función Python asociada
"""

g = StateGraph(State)

g.add_node("preprocess", preprocess)
g.add_node("llm_answer", llm_answer)
g.add_node("postprocess", postprocess)


# ------------------------------------------------------------------
# DEFINICIÓN DEL FLUJO
# ------------------------------------------------------------------
"""
Aquí definimos el orden de ejecución.

1. El punto de entrada es preprocess
2. preprocess -> llm_answer
3. llm_answer -> postprocess
4. postprocess -> END

Esto convierte el grafo en un pipeline lineal.

Observación docente:
aunque usemos LangGraph, este ejemplo no explota todavía
su capacidad de branching o routing. Precisamente por eso es
un buen primer ejemplo: permite entender la mecánica básica.
"""

g.set_entry_point("preprocess")
g.add_edge("preprocess", "llm_answer")
g.add_edge("llm_answer", "postprocess")
g.add_edge("postprocess", END)


# ------------------------------------------------------------------
# COMPILACIÓN DEL GRAFO
# ------------------------------------------------------------------
"""
compile() transforma la definición del grafo en una aplicación
ejecutable.

A partir de aquí, `app` ya se puede invocar con un estado inicial.
"""

app = g.compile()


# ------------------------------------------------------------------
# BLOQUE PRINCIPAL DE EJECUCIÓN
# ------------------------------------------------------------------
"""
Este bloque solo se ejecuta si lanzamos el script directamente.

Se construye un estado inicial con:
- una pregunta original
- normalized_question vacío
- answer vacío

Eso es importante:
aunque algunos campos estén vacíos al principio,
deben existir porque forman parte del esquema del estado.
"""

if __name__ == "__main__":
    result = app.invoke({
        "question": "  ¿Qué es RAG?  ",
        "normalized_question": "",
        "answer": ""
    })

    print("\n=== OUTPUT ===\n", result["answer"])