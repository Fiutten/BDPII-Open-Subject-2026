# pip install -U langchain langgraph langchain-openai

from typing_extensions import TypedDict

from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.graph import StateGraph, START, END

from dotenv import load_dotenv
load_dotenv()



# =========================================================
# 1) Estado del grafo
# =========================================================

class WorkflowState(TypedDict):
    degree_name: str
    user_request: str
    data_result: str
    final_answer: str


# =========================================================
# 2) Tools
# =========================================================

@tool
def get_degree_students(degree_name: str) -> str:
    """Devuelve un número ficticio de alumnos de una titulación."""
    fake_db = {
        "grado en ia": 42,
        "máster en análisis de datos deportivos": 8,
        "grado en ciencia e ingeniería de datos": 65,
    }
    value = fake_db.get(degree_name.lower(), "desconocido")
    return f"El número de alumnos en '{degree_name}' es {value}."


@tool
def multiply(a: int, b: int) -> int:
    """Multiplica dos enteros."""
    return a * b


# =========================================================
# 3) Agentes LangChain creados con create_agent(...)
# =========================================================
# create_agent es la API recomendada actualmente para agentes,
# y se invoca pasando un estado con "messages". :contentReference[oaicite:1]{index=1}

data_agent = create_agent(
    model="openai:gpt-4.1-mini",
    tools=[get_degree_students],
    system_prompt=(
        "Eres un agente de datos académicos. "
        "Usa la tool disponible para consultar el número de alumnos. "
        "Responde de forma breve y exacta."
    ),
    name="data_agent",
)

math_agent = create_agent(
    model="openai:gpt-4.1-mini",
    tools=[multiply],
    system_prompt=(
        "Eres un agente matemático. "
        "Usa la tool disponible para hacer cálculos. "
        "Responde de forma breve y exacta."
    ),
    name="math_agent",
)


# =========================================================
# 4) Nodos de LangGraph que llaman a agentes create_agent
# =========================================================

def data_agent_node(state: WorkflowState) -> dict:
    query = (
        f"Consulta cuántos alumnos hay en esta titulación: {state['degree_name']}. "
        "Devuelve solo una frase con el dato."
    )

    result = data_agent.invoke(
        {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
    )

    return {
        "data_result": result["messages"][-1].content
    }


def math_agent_node(state: WorkflowState) -> dict:
    query = (
        f"Tengo este dato: {state['data_result']} "
        f"Y esta petición del usuario: {state['user_request']} "
        "Calcula el triple del número de alumnos usando la tool disponible "
        "y responde con una sola frase."
    )

    result = math_agent.invoke(
        {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
    )

    return {
        "final_answer": result["messages"][-1].content
    }


# =========================================================
# 5) Construcción del flujo lineal en LangGraph
# =========================================================

builder = StateGraph(WorkflowState)

builder.add_node("data_agent_node", data_agent_node)
builder.add_node("math_agent_node", math_agent_node)

builder.add_edge(START, "data_agent_node")
builder.add_edge("data_agent_node", "math_agent_node")
builder.add_edge("math_agent_node", END)

graph = builder.compile()


# =========================================================
# 6) Ejecución
# =========================================================

result = graph.invoke(
    {
        "degree_name": "grado en ia",
        "user_request": "Quiero saber cuál es el triple del número de alumnos.",
        "data_result": "",
        "final_answer": "",
    }
)

print("DATA RESULT:")
print(result["data_result"])
print()
print("FINAL ANSWER:")
print(result["final_answer"])