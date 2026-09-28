from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from pathlib import Path
from dotenv import load_dotenv
import os

# 1️⃣ Ruta explícita al archivo .env (muy importante)
env_path = Path(__file__).resolve().parent / ".env"

print(f"Buscando .env en: {env_path}")

if not env_path.exists():
    raise FileNotFoundError(".env no encontrado en la carpeta del proyecto")

# 2️⃣ Cargar variables
load_dotenv(dotenv_path=env_path)

# 3️⃣ Comprobar que se ha cargado
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY no está definida en el .env")

print("API key cargada correctamente ✅")


# LLM (elige UNA opción)
# --- OpenAI ---
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# --- Ollama local ---
# from langchain_ollama import ChatOllama
# llm = ChatOllama(model="llama3.2", temperature=0)

DATA_DIR = Path("data")
PERSIST_DIR = Path("chroma_db")

# 1) Cargar documentos
docs = []
for fp in DATA_DIR.glob("*.txt"):
    loaded = TextLoader(str(fp), encoding="utf-8").load()
    for d in loaded:
        d.metadata["source"] = fp.name
    docs.extend(loaded)

# 2) Chunking
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
splits = splitter.split_documents(docs)

# 3) Embeddings (local)
emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# 4) Vector store (persistente)
vs = Chroma.from_documents(
    documents=splits,
    embedding=emb,
    persist_directory=str(PERSIST_DIR),
    collection_name="pln_rag_demo",
)

retriever = vs.as_retriever(search_kwargs={"k": 4})

# --- Prompt (como en el ejercicio) ---
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Eres un asistente cuidadoso. Responde SOLO usando el contexto proporcionado. "
     "Si el contexto es insuficiente, responde exactamente: "
     "'No puedo responder con la información disponible.' "
     "Siempre termina con una sección final 'Fuentes:' listando las fuentes únicas "
     "usadas (metadata 'source')."),
    ("human", "Pregunta: {question}\n\nContexto:\n{context}")
])

def format_docs_with_sources(docs):
    """Convierte los docs recuperados en texto y extrae fuentes únicas."""
    # Contexto (texto)
    context = "\n\n".join([d.page_content for d in docs])

    # Fuentes (únicas)
    sources = []
    for d in docs:
        src = d.metadata.get("source", "desconocido")
        if src not in sources:
            sources.append(src)

    sources_text = "\n".join([f"- {s}" for s in sources])
    return context, sources_text

# Cadena RAG con LCEL:
# 1) Recuperar docs
# 2) Formatear contexto + fuentes
# 3) Llamar al LLM con prompt
# 4) Añadir fuentes al final (si el modelo no las incluye perfectamente)
def rag_answer(question: str) -> str:
    docs = retriever.invoke(question)  # <-- API nueva
    context, sources_text = format_docs_with_sources(docs)

    answer = (prompt | llm | StrOutputParser()).invoke(
        {"question": question, "context": context}
    )

    if "Fuentes:" not in answer:
        answer = answer.rstrip() + "\n\nFuentes:\n" + sources_text

    return answer


# Preguntas que ahora el RAG puede responder:
# ¿Es obligatorio aprobar el proyecto final?
#
# ¿Qué ocurre en la convocatoria extraordinaria?
#
# ¿Se pueden recuperar prácticas no entregadas?
#
# ¿La asistencia es obligatoria?
#
# ¿Cuáles son los porcentajes de evaluación?

# ---- Prueba ----
q = "¿Cuál es la política de evaluación continua?"
print(rag_answer(q))
