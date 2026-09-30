"""
Agente LangGraph con herramienta Spark SQL para consultas en lenguaje natural.
Usa el patrón moderno create_react_agent.

EJERCICIO PARA ESTUDIANTES: Completa los TODOs para implementar el agente Text-to-SQL.
"""
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# Sesión global de Spark (se configurará desde main.py)
spark_session = None

def set_spark_session(spark):
    """Configura la sesión global de Spark."""
    global spark_session
    spark_session = spark

@tool
def execute_spark_sql(query: str) -> str:
    """
    Ejecuta una consulta Spark SQL y devuelve los resultados.

    Esta herramienta permite ejecutar consultas SQL sobre los datos del partido de fútbol.

    Tablas disponibles:
    - players: Contiene player_id, player_name, team (Real Madrid o FC Barcelona),
               position (Portero, Defensa, Centrocampista, Delantero), dorsal
    - events: Contiene event_id, player_id, team, event_type, timestamp, x, y,
              success, minute, presion, zone

    Tipos de eventos (event_type):
    - pase, disparo, gol, entrada, intercepción, regate, falta, córner,
    - saque_de_banda, despeje, centro, parada, fuera_de_juego,
    - tarjeta_amarilla, tarjeta_roja, tiro_libre, penalti,
    - saque_de_meta, cabezazo, remate, asistencia

    Args:
        query: Consulta SQL válida de Spark

    Returns:
        Resultados de la consulta en formato string
    """
    # TODO 1: Verificar si spark_session es None y retornar mensaje de error apropiado


    # TODO 2: Ejecutar la consulta SQL dentro de un bloque try-except
    # Debes:
    #   - Ejecutar la query con spark_session.sql()
    #   - Convertir el resultado a pandas DataFrame
    #   - Verificar si está vacío y retornar mensaje apropiado
    #   - Retornar los primeros 50 resultados como string
    #   - Capturar excepciones y retornar mensaje de error
    try:
        pass  # Reemplaza esto con tu implementación

    except Exception as e:
        return f"Error al ejecutar la consulta: {str(e)}"



def create_agent():
    """
    Crea y devuelve el agente LangGraph usando create_react_agent.

    Este agente puede responder preguntas sobre datos de partidos de fútbol
    en español e inglés, usando Spark SQL para consultar los datos.
    """
    # TODO 3: Inicializar el LLM de OpenAI con el modelo "gpt-5-mini". Valdrian otros como ChatOllama, u otros modelos
    llm = ChatOpenAI(name="gpt-5-mini")

    # TODO 4: Definir la lista de herramientas (tools) que incluya execute_spark_sql (un array con la función que define la herramienta)


    # System prompt - Este es el "cerebro" del agente
    # Documenta las tablas, tipos de eventos y proporciona ejemplos de consultas SQL
    system_message = """Eres un asistente experto en análisis de datos de fútbol que puede responder preguntas sobre partidos usando Spark SQL.

DATOS DISPONIBLES:

Tabla: players
--------------
Columnas:
- player_id (int): ID único del jugador
- player_name (string): Nombre del jugador (ej: "Carlos García", "Miguel López")
- team (string): Equipo - "Real Madrid" o "FC Barcelona"
- position (string): Posición - "Portero", "Defensa", "Centrocampista", o "Delantero"
- dorsal (int): Número de camiseta (1-11)

Tabla: events
-------------
Columnas:
- event_id (int): ID único del evento
- player_id (int): ID del jugador que realizó el evento
- team (string): Equipo del jugador - "Real Madrid" o "FC Barcelona"
- event_type (string): Tipo de evento (ver lista abajo)
- timestamp (string): Marca de tiempo del evento
- x (float): Coordenada X en el campo (0-105 metros)
- y (float): Coordenada Y en el campo (0-68 metros)
- success (boolean): Si el evento fue exitoso
- minute (int): Minuto del partido (0-90)
- presion (boolean): Si el jugador estaba bajo presión
- zone (string): Zona del campo - "defensivo", "medio", "ofensivo"

TIPOS DE EVENTOS (event_type):
===============================
- pase: Pase del balón
- disparo: Disparo a puerta
- gol: Gol marcado
- entrada: Entrada o tackle
- intercepción: Intercepción del balón
- regate: Regate o dribbling
- falta: Falta cometida
- córner: Córner o tiro de esquina
- saque_de_banda: Saque de banda
- despeje: Despeje del balón
- centro: Centro al área
- parada: Parada del portero
- fuera_de_juego: Fuera de juego (offside)
- tarjeta_amarilla: Tarjeta amarilla
- tarjeta_roja: Tarjeta roja
- tiro_libre: Tiro libre
- penalti: Penalti
- saque_de_meta: Saque de meta
- cabezazo: Remate de cabeza
- remate: Remate a puerta
- asistencia: Asistencia de gol

INSTRUCCIONES:
==============
1. Cuando el usuario haga una pregunta, tradúcela a una consulta Spark SQL
2. Usa la herramienta execute_spark_sql para ejecutar la consulta
3. Interpreta los resultados y responde en lenguaje natural
4. Siempre usa datos reales de la consulta - NUNCA inventes números
5. Puedes responder en español o inglés según el idioma de la pregunta
6. Para unir datos de jugadores y eventos, usa JOIN con player_id

EJEMPLOS DE CONSULTAS:
======================
- "¿Cuántos goles marcó el Real Madrid?"
  SELECT COUNT(*) FROM events WHERE event_type = 'gol' AND team = 'Real Madrid'

- "¿Qué jugador hizo más pases?"
  SELECT p.player_name, COUNT(*) as num_pases
  FROM events e JOIN players p ON e.player_id = p.player_id
  WHERE e.event_type = 'pase'
  GROUP BY p.player_name ORDER BY num_pases DESC LIMIT 1

- "¿Cuántas faltas hubo en total?"
  SELECT COUNT(*) FROM events WHERE event_type = 'falta'

Sé preciso, analítico y siempre basa tus respuestas en los datos reales."""

    # TODO 5: Crear el agente ReAct usando create_react_agent
    # Parámetros: llm, tools, state_modifier=system_message


    # TODO 6: Retornar el agente creado
