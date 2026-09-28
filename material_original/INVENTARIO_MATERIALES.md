# Inventario de materiales originales

## Asignatura

**Big Data Processing II**  
Máster Universitario en Análisis de Datos Deportivos  
Curso 2026-2027

## Equipo docente

- Alberto Fernández Isabel - profesor responsable.
- Natalia Madrueño Sierro.
- Rubén Rodríguez Fernández.

## Estado de las aportaciones

La primera aportación disponible corresponde al bloque de IA generativa. La segunda aportación, cubre los temas 1, 2 y 3. Falta por incorporar la parte que aportará Rubén Rodríguez Fernández.

## Material institucional

- `guias/Guia_Docente_Big_Data_Processing_II_2026-2027.pdf`: guía docente oficial, 10 páginas.

## Fuentes LaTeX de los temas 1 a 3

- Cada tema contiene, junto a su PDF, el `.tex` con el mismo nombre, el estilo `beamercolorthemeDSLAB.sty` (derivado de un tema GPL v2 de Till Tantau) y la carpeta `images/`. Compila sin configuración adicional.
- Requiere `-shell-escape` por el uso de `minted`: `latexmk -pdf -shell-escape <archivo>.tex`.

## Tema 1 - Procesamiento de Big Data en entornos distribuidos

### Presentaciones

- `teoria/01_Procesamiento_Big_Data_Distribuido/BDPII_Tema_1_Procesamiento_Big_Data_Distribuido.pdf`: 66 diapositivas. Fuente: `BDPII_Tema_1_Procesamiento_Big_Data_Distribuido.tex`.

### Programas

- `programas/01_Procesamiento_Big_Data_Distribuido/streaming.ipynb`: notebook de procesamiento naive frente a streaming sobre velocidades simuladas de Fórmula 1.
- `programas/01_Procesamiento_Big_Data_Distribuido/streaming_soluciones.ipynb`: solución del notebook anterior, con salidas ejecutadas.

## Tema 2 - Procesamiento de flujos de datos en tiempo real

### Presentaciones

- `teoria/02_Streaming_Tiempo_Real/BDPII_Tema_2_Apache_Kafka.pdf`: 44 diapositivas. Fuente: `BDPII_Tema_2_Apache_Kafka.tex`.
- `teoria/02_Streaming_Tiempo_Real/BDPII_Tema_2_Spark_Streaming.pdf`: 60 diapositivas. Fuente: `BDPII_Tema_2_Spark_Streaming.tex`.


### Enunciados

- `practica/02_Streaming_Tiempo_Real/Enunciado_Tema_2_Apache_Kafka.pdf` y su fuente `.docx`: 2 páginas.
- `practica/02_Streaming_Tiempo_Real/Enunciado_Tema_2_Spark_Structured_Streaming.pdf` y su fuente `.docx`: 3 páginas.


### Programas y datos

- `programas/02_Streaming_Tiempo_Real/recursos_kafka/producer.py`: productor Kafka que publica la telemetría del CSV.
- `programas/02_Streaming_Tiempo_Real/recursos_kafka/sensores_deportivos_fatiga.csv`: 10 800 mediciones simuladas de 15 jugadores en 3 partidos.
- `programas/02_Streaming_Tiempo_Real/recursos_kafka/descripcion_sensores_deportivos_fatiga.txt`: descripción del conjunto de datos.
- `programas/02_Streaming_Tiempo_Real/recursos_spark/docker-compose.yml`: entorno con Kafka y Jupyter con PySpark.
- `programas/02_Streaming_Tiempo_Real/recursos_spark/spark_streaming.ipynb`: notebook plantilla de Spark Structured Streaming.

## Tema 3 - Optimización y escalabilidad

### Presentaciones

- `teoria/03_Optimizacion_Escalabilidad/BDPII_Tema_3_Optimizacion_Escalabilidad.pdf`: 36 diapositivas. Fuente: `BDPII_Tema_3_Optimizacion_Escalabilidad.tex`.

## Tema 4 - Inteligencia Artificial Generativa aplicada a Big Data Deportivo

### Presentaciones

- Sesión 1: Prompt Engineering y Post-training, 54 diapositivas.
- Sesión 2: Retrieval-Augmented Generation, 30 diapositivas.
- Sesión 3: Sistemas basados en agentes, 36 diapositivas.
- `teoria/04_IA_Generativa/editables/Fuentes_LaTeX_e_Imagenes_IA_Generativa.zip`: fuentes LaTeX de las tres sesiones y recursos gráficos.

### Ejercicios

Se conservan tres colecciones de ejercicios en PDF y sus correspondientes fuentes DOCX:

- Sesión 1: Prompt Engineering aplicado al análisis deportivo.
- Sesión 2: RAG aplicado al análisis deportivo.
- Sesión 3: Agentes aplicados al análisis deportivo.

### Programas

- Sesión 2: `RAG_1.py` y `RAG_1_comentado.py`.
- Sesión 3: `flow_lineal.py`, `agent_flow_lineal.py` y `agent_skills_tools.py`.
- `programas/04_IA_Generativa/requirements.txt`: dependencias comunes.

Los cinco programas superan la comprobación sintáctica de Python. Todavía deben revisarse su documentación, datos de ejemplo, licencia y ejecución reproducible antes de publicarlos como categoría 6.

## Tema 5 - Proyecto integrado

- `practica/05_Proyecto_Integrado/Practica_Final_Big_Data_Processing_II.pdf`: práctica final de 10 páginas sobre Kafka, Spark Structured Streaming, RAG, LangGraph y generación automática de informes.

## Autoría y procedencia

Las tres presentaciones identifican en portada a Alberto Fernández Isabel, Natalia Madrueño Sierro y Rubén Rodríguez Fernández como equipo docente. Este dato no determina por sí solo los porcentajes de autoría intelectual de los materiales. La atribución definitiva y los porcentajes para la declaración de la convocatoria deberán ser confirmados por los tres docentes cuando el inventario esté completo.

Los metadatos de los tres DOCX de ejercicios indican que su última modificación fue realizada por Alberto Fernández Isabel. Se conserva este dato únicamente como información de procedencia editorial, no como determinación definitiva de autoría.

## Estado de publicación

Ninguno de estos archivos se considera todavía versión definitiva para BURJC Digital. Antes de copiarlos a `material_abierto/` deben completarse la auditoría de fuentes e imágenes, el licenciamiento, las atribuciones y la revisión de los materiales pendientes.
