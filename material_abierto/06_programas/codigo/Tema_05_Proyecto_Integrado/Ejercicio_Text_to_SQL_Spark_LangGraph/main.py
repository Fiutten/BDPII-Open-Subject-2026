"""
Script principal para ejecutar el agente Spark SQL.

EJERCICIO PARA ESTUDIANTES: Completa los TODOs para implementar carga de datos e interacción con el agente.
"""
import os
from pyspark.sql import SparkSession
from langchain_core.messages import HumanMessage
from agent import create_agent, set_spark_session

from dotenv import load_dotenv
load_dotenv()


def init_spark():
    """Inicializa la sesión de Spark."""
    print("Inicializando sesión de Spark...")
    spark = SparkSession.builder \
        .appName("FootballAnalysisAgent") \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    return spark

def load_data(spark):
    """Carga datos CSV en DataFrames de Spark y los registra como tablas."""
    print("Cargando datos del partido...")

    # TODO 1: Cargar players.csv en un DataFrame de Spark
    # Usa spark.read.csv() con header=True e inferSchema=True


    # TODO 2: Registrar el DataFrame de jugadores como vista SQL con nombre "players"


    print(f"  Cargados {players_df.count()} jugadores")

    # TODO 3: Cargar events.csv en un DataFrame de Spark


    # TODO 4: Registrar el DataFrame de eventos como vista SQL con nombre "events"


    print(f"  Cargados {events_df.count()} eventos")

    return players_df, events_df

def run_agent(agent):
    """Ejecuta el agente en modo interactivo."""
    print("""
AGENTE SQL DE ANÁLISIS DE FÚTBOL

Real Madrid vs FC Barcelona - Análisis de Partido

Preguntas de ejemplo:

  Estadísticas Generales:
    - ¿Cuántos goles marcó cada equipo?
    - ¿Cuál fue el resultado final del partido?
    - ¿Cuántas tarjetas amarillas y rojas hubo?

  Análisis por Jugador:
    - ¿Qué jugador hizo más pases?
    - ¿Qué delanteros marcaron goles?
    - ¿Quién tuvo más intercepciones?

  Análisis por Equipo:
    - ¿Cuál fue la tasa de éxito de pases del Real Madrid?
    - ¿Cuántos disparos tuvo el FC Barcelona?
    - ¿Cuántos córners tuvo cada equipo?

  Análisis Temporal:
    - ¿Cuántos eventos ocurrieron en los primeros 10 minutos?
    - ¿En qué minuto se marcaron los goles?
    - ¿Cuántas faltas hubo en la segunda mitad?

  Análisis Espacial:
    - ¿Cuántos eventos ocurrieron en la zona ofensiva?
    - ¿Cuántos pases fueron bajo presión?

Escribe 'quit' o 'salir' para terminar
""")

     # Run the agent with the new react agent structure
    try:
        for chunk in agent.stream(
            {"messages": [HumanMessage(content=user_input)]},
            stream_mode="values"
        ):
            # Get the last message
            last_message = chunk["messages"][-1]

            # Print AI responses (not tool calls)
            if hasattr(last_message, 'content') and last_message.content:
                # Skip if it's a tool call message
                if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
                    # Only print if it's not empty
                    content = last_message.content.strip()
                    if content:
                        print(content)

    except Exception as e:
        print(f"Error: {str(e)}")
        print("Por favor, intenta reformular tu pregunta.")


def main():
    """Punto de entrada principal."""
    print("\nSISTEMA DE ANÁLISIS DE FÚTBOL CON IA\n")

    # Verificar que existan los archivos de datos
    if not os.path.exists("data/players.csv") or not os.path.exists("data/events.csv"):
        print("Archivos de datos no encontrados.")
        print("Por favor ejecuta primero: python generate_data.py")
        return

    # Inicializar Spark y configurar sesión global
    spark = init_spark()
    set_spark_session(spark)

    # Cargar datos y registrar tablas
    load_data(spark)

    # Crear y ejecutar agente
    print("\nInicializando agente de IA...")
    agent = create_agent()
    print("Agente listo!\n")

    try:
        run_agent(agent)
    finally:
        spark.stop()
        print("\nSesión de Spark finalizada.")

if __name__ == '__main__':
    main()
