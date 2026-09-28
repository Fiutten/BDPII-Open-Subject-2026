"""
RAG_1.py
========================================================
Sesión 2 — Retrieval-Augmented Generation (RAG)
Big Data Processing II · Máster en Ciencia de Datos Deportivos

DESCRIPCIÓN GENERAL
--------------------------------------------------------
Este script implementa un sistema RAG sencillo pero real:

1. Lee documentos .txt desde una carpeta local
2. Los divide en fragmentos (chunking)
3. Convierte esos fragmentos en embeddings
4. Los guarda en una base vectorial persistente (Chroma)
5. Recupera los fragmentos más relevantes para una pregunta
6. Pasa esos fragmentos al modelo de lenguaje
7. Genera una respuesta basada SOLO en el contexto recuperado
8. Añade las fuentes usadas al final

OBJETIVO DOCENTE
--------------------------------------------------------
Que el alumnado entienda que un sistema RAG no consiste
en "preguntar al modelo", sino en construir un pipeline
de recuperación + generación con trazabilidad.

REQUISITOS PREVIOS
--------------------------------------------------------
- Carpeta "data/" con documentos .txt
- Archivo ".env" en la misma carpeta que este script
- OPENAI_API_KEY definida en el .env

Ejemplo de .env:
OPENAI_API_KEY=tu_clave_aqui
"""

# ======================================================
# IMPORTS PRINCIPALES
# ======================================================

# Plantillas de prompt y parser de salida
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Carga de documentos y división en fragmentos
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Embeddings y base vectorial
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Utilidades del sistema
from pathlib import Path
from dotenv import load_dotenv
import os


# ======================================================
# 1. CARGA DE VARIABLES DE ENTORNO
# ======================================================
"""
¿Por qué este bloque es importante?

Necesitamos una clave de API para usar el modelo de OpenAI.
En lugar de escribirla directamente en el código, la guardamos
en un archivo .env para que:

- no aparezca expuesta en el script
- se pueda reutilizar fácilmente
- sea más seguro trabajar en proyectos reales
"""

# Ruta explícita al archivo .env
# Usamos __file__ para localizar el .env en la misma carpeta del script
env_path = Path(__file__).resolve().parent / ".env"

print(f"Buscando .env en: {env_path}")

# Comprobamos que el archivo exista antes de continuar
if not env_path.exists():
    raise FileNotFoundError(".env no encontrado en la carpeta del proyecto")

# Cargamos variables de entorno desde el .env
load_dotenv(dotenv_path=env_path)

# Recuperamos la clave de OpenAI
api_key = os.getenv("OPENAI_API_KEY")

# Si no existe, detenemos el programa
if not api_key:
    raise ValueError("OPENAI_API_KEY no está definida en el .env")

print("API key cargada correctamente ✅")


# ======================================================
# 2. CONFIGURACIÓN DEL LLM
# ======================================================
"""
Aquí elegimos qué modelo generativo usaremos para redactar
la respuesta final.

En este ejemplo usamos OpenAI.
También se deja comentada una alternativa con Ollama local.

temperature=0:
- hace el modelo más determinista
- reduce variabilidad entre ejecuciones
- es recomendable en tareas analíticas
"""

# --- Opción OpenAI ---
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

# --- Opción local con Ollama (descomentando estas líneas) ---
# from langchain_ollama import ChatOllama
# llm = ChatOllama(model="llama3.2", temperature=0)


# ======================================================
# 3. RUTAS DE DATOS
# ======================================================
"""
DATA_DIR: carpeta con los documentos de entrada
PERSIST_DIR: carpeta donde Chroma guardará la base vectorial

La persistencia es útil porque:
- evita recomputar embeddings cada vez
- acelera iteraciones
- se parece más a un sistema real
"""
DATA_DIR = Path("data")
PERSIST_DIR = Path("chroma_db")


# ======================================================
# 4. CARGA DE DOCUMENTOS
# ======================================================
"""
En este bloque se leen todos los archivos .txt de la carpeta data/.

Cada archivo se convierte en uno o varios objetos Document de LangChain.
Además, añadimos metadata con la fuente original del documento.

¿Por qué es importante añadir metadata?
- para saber de qué fichero sale cada evidencia
- para poder citar fuentes al final
- para permitir filtros futuros (por jugador, tipo, fecha, etc.)
"""
docs = []

for fp in DATA_DIR.glob("*.txt"):
    loaded = TextLoader(str(fp), encoding="utf-8").load()

    for d in loaded:
        # Guardamos el nombre del fichero como fuente
        d.metadata["source"] = fp.name

    docs.extend(loaded)

print(f"Documentos cargados: {len(docs)}")


# ======================================================
# 5. CHUNKING (DIVISIÓN EN FRAGMENTOS)
# ======================================================
"""
Los LLM y las bases vectoriales no suelen trabajar bien con
documentos largos completos. Por eso los dividimos en chunks.

Parámetros:
- chunk_size=500
    número aproximado de caracteres por fragmento
- chunk_overlap=100
    solapamiento entre fragmentos consecutivos

¿Por qué usar overlap?
Porque si una idea importante queda justo al final de un chunk,
el solapamiento ayuda a no perder contexto en el siguiente.

Trade-off importante:
- chunks muy pequeños -> se pierde contexto
- chunks muy grandes -> retrieval menos preciso
"""
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
splits = splitter.split_documents(docs)

print(f"Fragmentos generados tras chunking: {len(splits)}")


# ======================================================
# 6. EMBEDDINGS
# ======================================================
"""
Los embeddings convierten cada fragmento de texto en un vector numérico.

Eso permite buscar por similitud semántica:
- no solo por palabras exactas
- sino por significado aproximado

Usamos un modelo local de sentence-transformers:
all-mpnet-base-v2

Ventajas:
- muy bueno para tareas generales de similitud semántica
- no necesita API externa para embeddings
- práctico para laboratorio docente
"""
emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

print("Modelo de embeddings cargado correctamente.")


# ======================================================
# 7. VECTOR STORE (CHROMA)
# ======================================================
"""
Aquí construimos la base vectorial.

Qué guarda:
- los fragmentos de texto
- los embeddings
- la metadata

Qué permite:
- búsqueda semántica eficiente
- persistencia local
- reutilización entre ejecuciones

collection_name:
- nombre interno de la colección en Chroma
- útil si en el futuro tienes varias colecciones
"""
vs = Chroma.from_documents(
    documents=splits,
    embedding=emb,
    persist_directory=str(PERSIST_DIR),
    collection_name="pln_rag_demo",
)

print("Base vectorial creada correctamente.")


# ======================================================
# 8. RETRIEVER
# ======================================================
"""
El retriever es el componente que recupera los fragmentos más
relevantes para una pregunta dada.

k=4 significa:
- devolver los 4 fragmentos más relevantes

Este valor se puede cambiar y es una decisión importante:

- k pequeño:
    menos ruido, pero riesgo de perder evidencia útil
- k grande:
    más cobertura, pero más tokens y más ruido
"""
retriever = vs.as_retriever(search_kwargs={"k": 4})


# ======================================================
# 9. PROMPT
# ======================================================
"""
El prompt es crítico para evitar alucinaciones.

Le decimos explícitamente al modelo:

- que responda SOLO con el contexto
- que si el contexto no basta, lo diga claramente
- que termine con una sección "Fuentes:"

Esto obliga al sistema a ser más trazable y prudente.
"""
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Eres un asistente cuidadoso. Responde SOLO usando el contexto proporcionado. "
        "Si el contexto es insuficiente, responde exactamente: "
        "'No puedo responder con la información disponible.' "
        "Siempre termina con una sección final 'Fuentes:' listando las fuentes únicas "
        "usadas (metadata 'source')."
    ),
    (
        "human",
        "Pregunta: {question}\n\nContexto:\n{context}"
    )
])


# ======================================================
# 10. FUNCIÓN AUXILIAR PARA FORMATEAR CONTEXTO Y FUENTES
# ======================================================
"""
El retriever devuelve una lista de objetos Document.

Esta función hace dos cosas:
1. une el contenido textual para construir el contexto del prompt
2. extrae una lista única de fuentes para citar al final

Esto es importante porque:
- el LLM necesita un bloque de texto continuo como contexto
- el usuario necesita saber de dónde sale la respuesta
"""
def format_docs_with_sources(docs):
    """
    Convierte los documentos recuperados en:
    - un bloque de texto (context)
    - una lista de fuentes únicas (sources_text)
    """

    # Unimos el contenido de todos los fragmentos recuperados
    context = "\n\n".join([d.page_content for d in docs])

    # Extraemos fuentes sin repetir
    sources = []
    for d in docs:
        src = d.metadata.get("source", "desconocido")
        if src not in sources:
            sources.append(src)

    # Formato legible de fuentes
    sources_text = "\n".join([f"- {s}" for s in sources])

    return context, sources_text


# ======================================================
# 11. FUNCIÓN PRINCIPAL DEL SISTEMA RAG
# ======================================================
"""
Esta función implementa el pipeline central:

1. recibe una pregunta
2. recupera documentos relevantes
3. construye contexto + fuentes
4. llama al LLM con ese contexto
5. comprueba si el modelo ha incluido las fuentes
6. si no lo ha hecho bien, las añade manualmente

Observación importante:
Aunque el prompt obliga al modelo a terminar con "Fuentes:",
en la práctica los modelos no siempre obedecen perfectamente.
Por eso aquí añadimos una pequeña salvaguarda.
"""
def rag_answer(question: str) -> str:
    """
    Devuelve una respuesta basada en documentos recuperados.

    Parámetro:
    - question: pregunta del usuario en lenguaje natural

    Salida:
    - string con la respuesta final y sus fuentes
    """

    # Recuperamos los fragmentos más relevantes
    docs = retriever.invoke(question)

    # Convertimos los docs en contexto + lista de fuentes
    context, sources_text = format_docs_with_sources(docs)

    # Ejecutamos la cadena prompt -> LLM -> parser
    answer = (prompt | llm | StrOutputParser()).invoke(
        {"question": question, "context": context}
    )

    # Si el modelo no incluye bien la sección de fuentes, la añadimos nosotros
    if "Fuentes:" not in answer:
        answer = answer.rstrip() + "\n\nFuentes:\n" + sources_text

    return answer


# ======================================================
# 12. PRUEBA DEL SISTEMA
# ======================================================
"""
Aquí lanzamos una pregunta de prueba.

IMPORTANTE PARA DOCENCIA:

Para pruebas deberías cambiarla por preguntas como:
- ¿Existe riesgo de fatiga para el jugador X?
- ¿Qué evidencias indican acumulación de carga?
"""
q = "¿Por qué disminuyó la presión alta del equipo?"
print(rag_answer(q))