# Práctica: Text-to-SQL Agent con LangGraph y Apache Spark

## 📚 Descripción

Esta práctica te guiará en la implementación de un **agente de IA conversacional** que puede responder preguntas en lenguaje natural sobre datos deportivos usando **Apache Spark SQL**. El agente traduce preguntas en español o inglés a consultas SQL, las ejecuta en Spark, y devuelve respuestas en lenguaje natural.

Este ejercicio demuestra:
- Integración de LLMs con sistemas de big data (Spark)
- Patrón ReAct (Reasoning + Acting) usando LangGraph
- Text-to-SQL usando modelos generativos
- Procesamiento de datos deportivos a escala

## 🎯 Objetivos de Aprendizaje

Al completar esta práctica, serás capaz de:

1. **Integrar Apache Spark con LangGraph** para crear agentes que trabajan con big data
2. **Implementar el patrón ReAct** usando `create_react_agent`
3. **Crear herramientas (tools)** personalizadas para agentes de LangGraph
4. **Diseñar prompts efectivos** que documenten esquemas de datos y guíen al LLM
5. **Manejar streaming de respuestas** de agentes conversacionales
6. **Trabajar con DataFrames de Spark** y registrarlos como vistas SQL

## 📋 Requisitos Previos

- Python 3.10, 3.11 o 3.12
- Java 11 o superior (requerido por Spark)
- Clave de API de OpenAI
- Conocimientos básicos de:
  - SQL
  - Python
  - Conceptos de LLMs y agentes

## 🚀 Configuración Inicial

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Crea un archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

Edita `.env` y añade tu clave de API de OpenAI:

```
OPENAI_API_KEY=tu-clave-aqui
```

### 3. Generar Datos de Prueba

Ejecuta el script para generar datos del partido:

```bash
python generate_data.py
```

Esto creará:
- `data/players.csv` - 22 jugadores (11 por equipo)
- `data/events.csv` - ~2000 eventos del partido

**NOTA**: Este script está completo y NO necesitas modificarlo. Solo ejecútalo para generar los datos.

## ✏️ TODOs a Completar

### Archivo: `agent.py`

Este archivo define el agente LangGraph con la herramienta Spark SQL.

#### **TODO 1**: Verificar Sesión de Spark
- **Ubicación**: Función `execute_spark_sql()`, línea ~45
- **Tarea**: Verificar si `spark_session` es `None` y retornar mensaje de error
- **Dificultad**: ⭐ Fácil

#### **TODO 2**: Ejecutar Consulta SQL
- **Ubicación**: Función `execute_spark_sql()`, bloque try-except
- **Tarea**: Implementar la ejecución de consultas SQL con manejo de errores
- **Subtareas**:
  - 2.1: Ejecutar query con `spark_session.sql(query)`
  - 2.2: Convertir resultado a Pandas con `.toPandas()`
  - 2.3: Verificar si el DataFrame está vacío
  - 2.4: Retornar resultados como string (máximo 50 filas)
  - 2.5: Manejar excepciones y retornar mensaje de error
- **Dificultad**: ⭐⭐ Intermedio

#### **TODO 3**: Inicializar el LLM
- **Ubicación**: Función `create_agent()`
- **Tarea**: Crear instancia de `ChatOpenAI` con modelo "gpt-5-mini"
- **Dificultad**: ⭐ Fácil

#### **TODO 4**: Definir Lista de Herramientas
- **Ubicación**: Función `create_agent()`
- **Tarea**: Crear lista con la herramienta `execute_spark_sql`
- **Dificultad**: ⭐ Fácil

#### **TODO 5**: Crear System Prompt (¡MÁS IMPORTANTE!)
- **Ubicación**: Función `create_agent()`
- **Tarea**: Diseñar un prompt comprensivo que documente el sistema
- **Debe incluir**:
  - Descripción del rol del agente
  - Documentación de la tabla `players` (columnas: player_id, player_name, team, position, dorsal)
  - Documentación de la tabla `events` (columnas: event_id, player_id, team, event_type, timestamp, x, y, success, minute, presion, zone)
  - Los 21 tipos de eventos con descripciones en español
  - Instrucciones de uso de la herramienta SQL
  - Ejemplos de consultas SQL
  - Directrices: usar datos reales, responder en el idioma del usuario, usar JOINs
- **Dificultad**: ⭐⭐⭐ Avanzado
- **Pista**: Estudia el esquema en `generate_data.py` para entender las tablas

#### **TODO 6**: Crear Agente ReAct
- **Ubicación**: Función `create_agent()`
- **Tarea**: Usar `create_react_agent(llm, tools, state_modifier=system_message)`
- **Dificultad**: ⭐ Fácil

#### **TODO 7**: Retornar el Agente
- **Ubicación**: Función `create_agent()`
- **Tarea**: Retornar la instancia del agente creado
- **Dificultad**: ⭐ Fácil

### Archivo: `main.py`

Este archivo carga los datos y ejecuta el agente en modo interactivo.

#### **TODO 1**: Cargar CSV de Jugadores
- **Ubicación**: Función `load_data()`, línea ~32
- **Tarea**: Usar `spark.read.csv()` para cargar `data/players.csv`
- **Parámetros**: `header=True`, `inferSchema=True`
- **Dificultad**: ⭐ Fácil

#### **TODO 2**: Registrar Tabla de Jugadores
- **Ubicación**: Función `load_data()`, línea ~38
- **Tarea**: Registrar el DataFrame como vista SQL con nombre "players"
- **Método**: `.createOrReplaceTempView("players")`
- **Dificultad**: ⭐ Fácil

#### **TODO 3**: Cargar CSV de Eventos
- **Ubicación**: Función `load_data()`, línea ~42
- **Tarea**: Usar `spark.read.csv()` para cargar `data/events.csv`
- **Parámetros**: `header=True`, `inferSchema=True`
- **Dificultad**: ⭐ Fácil

#### **TODO 4**: Registrar Tabla de Eventos
- **Ubicación**: Función `load_data()`, línea ~48
- **Tarea**: Registrar el DataFrame como vista SQL con nombre "events"
- **Método**: `.createOrReplaceTempView("events")`
- **Dificultad**: ⭐ Fácil

#### **TODO 5**: Implementar Loop de Invocación del Agente
- **Ubicación**: Función `run_agent()`, bloque try-except
- **Tarea**: Invocar el agente y mostrar respuestas en streaming
- **Subtareas**:
  - 5.1: Usar `agent.stream()` con mensajes y modo de streaming
  - 5.2: Extraer el último mensaje de cada chunk
  - 5.3: Filtrar y mostrar solo respuestas del agente (no tool calls)
  - 5.4: Manejar errores gracefully
- **Dificultad**: ⭐⭐⭐ Avanzado

## 🧪 Pruebas y Validación

### 1. Ejecutar el Agente

```bash
python main.py
```

### 2. Preguntas de Prueba

Prueba el agente con estas preguntas (en español o inglés):

**Estadísticas Generales:**
- ¿Cuántos goles marcó cada equipo?
- ¿Cuál fue el resultado final del partido?
- How many yellow cards were there?

**Análisis por Jugador:**
- ¿Qué jugador hizo más pases?
- ¿Qué delanteros marcaron goles?
- Who had the most interceptions?

**Análisis por Equipo:**
- ¿Cuál fue la tasa de éxito de pases del Real Madrid?
- ¿Cuántos disparos tuvo el FC Barcelona?

**Análisis Temporal y Espacial:**
- ¿Cuántos eventos ocurrieron en los primeros 10 minutos?
- ¿Cuántos pases fueron bajo presión?

### 3. Salida Esperada

El agente debe:
- ✅ Traducir tu pregunta a una consulta SQL válida
- ✅ Ejecutar la consulta en Spark
- ✅ Interpretar los resultados
- ✅ Responder en lenguaje natural en el mismo idioma que la pregunta
- ✅ Basar todas las respuestas en datos reales (NUNCA inventar números)

**Ejemplo de Interacción:**

```
Tu pregunta: ¿Cuántos goles marcó el Real Madrid?

Analizando...

El Real Madrid marcó 3 goles en este partido.
```

## 📊 Esquema de Datos

### Tabla: `players`
| Columna       | Tipo   | Descripción                                    |
|---------------|--------|------------------------------------------------|
| player_id     | int    | ID único del jugador (1-22)                    |
| player_name   | string | Nombre completo del jugador                    |
| team          | string | "Real Madrid" o "FC Barcelona"                 |
| position      | string | "Portero", "Defensa", "Centrocampista", "Delantero" |
| dorsal        | int    | Número de camiseta (1-11)                      |

### Tabla: `events`
| Columna    | Tipo    | Descripción                                      |
|------------|---------|--------------------------------------------------|
| event_id   | int     | ID único del evento                              |
| player_id  | int     | ID del jugador que realizó el evento             |
| team       | string  | "Real Madrid" o "FC Barcelona"                   |
| event_type | string  | Tipo de evento (ver lista abajo)                 |
| timestamp  | string  | Marca de tiempo del evento                       |
| x          | float   | Coordenada X en metros (0-105)                   |
| y          | float   | Coordenada Y en metros (0-68)                    |
| success    | boolean | Si el evento fue exitoso                         |
| minute     | int     | Minuto del partido (0-90)                        |
| presion    | boolean | Si el jugador estaba bajo presión                |
| zone       | string  | "defensivo", "medio", "ofensivo"                 |

### 21 Tipos de Eventos

| event_type        | Descripción en Español      | % Aprox |
|-------------------|-----------------------------|---------|
| pase              | Pase del balón              | 40%     |
| disparo           | Disparo a puerta            | 10%     |
| gol               | Gol marcado                 | 1.5%    |
| entrada           | Entrada o tackle            | 8%      |
| intercepción      | Intercepción del balón      | 7%      |
| regate            | Regate o dribbling          | 5%      |
| falta             | Falta cometida              | 4%      |
| córner            | Córner o tiro de esquina    | 2.5%    |
| saque_de_banda    | Saque de banda              | 5%      |
| despeje           | Despeje del balón           | 3%      |
| centro            | Centro al área              | 2%      |
| parada            | Parada del portero          | 1.5%    |
| fuera_de_juego    | Fuera de juego (offside)    | 2%      |
| tarjeta_amarilla  | Tarjeta amarilla            | 1%      |
| tarjeta_roja      | Tarjeta roja                | 0.2%    |
| tiro_libre        | Tiro libre                  | 1.5%    |
| penalti           | Penalti                     | 0.3%    |
| saque_de_meta     | Saque de meta               | 4%      |
| cabezazo          | Remate de cabeza            | 2.5%    |
| remate            | Remate a puerta             | 8%      |
| asistencia        | Asistencia de gol           | 1.5%    |

## 💡 Consejos y Buenas Prácticas

### Para el System Prompt (TODO 5):

1. **Sé específico**: Documenta cada columna con su tipo y significado
2. **Proporciona ejemplos**: Incluye 3-5 consultas SQL de ejemplo
3. **Define el comportamiento**: Instrucciones claras sobre cómo responder
4. **Prevén errores**: Indica qué hacer si no hay resultados
5. **Multiidioma**: Especifica que debe responder en el idioma de la pregunta

### Para el Streaming (TODO 5 en main.py):

1. **Filtra tool calls**: No imprimas las llamadas internas a herramientas
2. **Verifica contenido**: Asegúrate de que el mensaje tenga contenido antes de imprimir
3. **Maneja errores**: Usa try-except para capturar excepciones del LLM

### Debugging:

- Si el agente no responde, verifica tu clave de API de OpenAI
- Si hay errores SQL, revisa que las tablas estén registradas correctamente
- Si las respuestas son incorrectas, mejora el system prompt con más ejemplos
- Usa `print()` para inspeccionar variables durante el desarrollo

## 📚 Recursos Adicionales

- [Documentación de LangGraph](https://langchain-ai.github.io/langgraph/)
- [Apache Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [ReAct Pattern Paper](https://arxiv.org/abs/2210.03629)

## ✅ Criterios de Éxito

Tu implementación está completa cuando:

- ✅ El script genera datos correctamente con `python generate_data.py`
- ✅ El agente se inicializa sin errores con `python main.py`
- ✅ Puedes hacer preguntas en español e inglés
- ✅ El agente traduce preguntas a SQL correctamente
- ✅ Las respuestas se basan en datos reales (no inventados)
- ✅ Los errores se manejan gracefully
- ✅ El streaming de respuestas funciona sin mostrar tool calls

## 🎓 Desafíos Adicionales (Opcionales)

Si terminas temprano, intenta estos desafíos:

1. **Añadir más herramientas**: Crea una herramienta para visualizar eventos en el campo
2. **Optimizar consultas**: Mejora el prompt para generar consultas SQL más eficientes
3. **Memoria conversacional**: Añade memoria al agente para recordar preguntas anteriores
4. **Validación de SQL**: Añade validación para prevenir consultas peligrosas
5. **Exportar resultados**: Añade capacidad de exportar análisis a CSV o PDF

¡Buena suerte con tu práctica! 🚀⚽
