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

Están incorporados los temas 1 a 6. Las fuentes LaTeX de los temas 5 y 6 se han reconstruido a partir de sus PDF.

## Material institucional

- `guias/Guia_Docente_Big_Data_Processing_II_2026-2027.pdf`: guía docente oficial, 10 páginas.

## Fuentes editables

Las fuentes se conservan separadas de los documentos finales:

- `fuentes/teoria/`: fuentes LaTeX, estilos e imágenes, organizados por tema.
- `fuentes/practica/`: fuentes DOCX de los ejercicios y enunciados, organizadas por tema.
- `fuentes/guias/Guia_de_estudio_Big_Data_Processing_II_2026-2027.docx`: fuente editable de la guía de estudio publicada en categoría 0.

Las fuentes LaTeX de cada tema se mantienen junto con sus dependencias gráficas. La compilación requiere `-shell-escape` por el uso de `minted`: `latexmk -pdf -shell-escape <archivo>.tex`.

El antiguo ZIP del tema 4 se ha extraído completamente. El archivo `images.zip` que contenía era una copia redundante de la carpeta `images/`, por lo que no se conserva.

## Tema 1 - Procesamiento de Big Data en entornos distribuidos

### Presentación

- `teoria/Tema_01_Procesamiento_Big_Data_Distribuido/BDPII_Tema_01_Procesamiento_Big_Data_Distribuido.pdf`: 66 diapositivas.

### Fuente

- `fuentes/teoria/Tema_01_Procesamiento_Big_Data_Distribuido/BDPII_Tema_01_Procesamiento_Big_Data_Distribuido.tex`, estilo Beamer e imágenes.

### Programas

- `programas/Tema_01_Procesamiento_Big_Data_Distribuido/streaming.ipynb`: notebook de procesamiento naive frente a streaming sobre velocidades simuladas de Fórmula 1.
- `programas/Tema_01_Procesamiento_Big_Data_Distribuido/streaming_soluciones.ipynb`: solución del notebook anterior, con salidas ejecutadas.

## Tema 2 - Procesamiento de flujos de datos en tiempo real

### Presentaciones

- `teoria/Tema_02_Streaming_Tiempo_Real/BDPII_Tema_02_Apache_Kafka.pdf`: 44 diapositivas.
- `teoria/Tema_02_Streaming_Tiempo_Real/BDPII_Tema_02_Spark_Structured_Streaming.pdf`: 60 diapositivas.

### Fuentes de teoría

- `fuentes/teoria/Tema_02_Streaming_Tiempo_Real/`: dos fuentes LaTeX, estilo Beamer e imágenes compartidas.

### Enunciados

- `practica/Tema_02_Streaming_Tiempo_Real/BDPII_Tema_02_Enunciado_Apache_Kafka.pdf`: 2 páginas.
- `practica/Tema_02_Streaming_Tiempo_Real/BDPII_Tema_02_Enunciado_Spark_Structured_Streaming.pdf`: 3 páginas.
- Fuentes DOCX correspondientes en `fuentes/practica/Tema_02_Streaming_Tiempo_Real/`.

### Programas y datos

- `programas/Tema_02_Streaming_Tiempo_Real/recursos_kafka/producer.py`: productor Kafka que publica la telemetría del CSV.
- `programas/Tema_02_Streaming_Tiempo_Real/recursos_kafka/sensores_deportivos_fatiga.csv`: 10 800 mediciones simuladas de 15 jugadores en 3 partidos.
- `programas/Tema_02_Streaming_Tiempo_Real/recursos_kafka/descripcion_sensores_deportivos_fatiga.txt`: descripción del conjunto de datos.
- `programas/Tema_02_Streaming_Tiempo_Real/recursos_spark/docker-compose.yml`: entorno con Kafka y Jupyter con PySpark.
- `programas/Tema_02_Streaming_Tiempo_Real/recursos_spark/spark_streaming.ipynb`: notebook plantilla de Spark Structured Streaming.

## Tema 3 - Optimización y escalabilidad

### Presentación

- `teoria/Tema_03_Optimizacion_Escalabilidad/BDPII_Tema_03_Optimizacion_Escalabilidad.pdf`: 36 diapositivas.

### Fuente

- `fuentes/teoria/Tema_03_Optimizacion_Escalabilidad/BDPII_Tema_03_Optimizacion_Escalabilidad.tex`, estilo Beamer e imágenes.

## Tema 4 - Inteligencia Artificial Generativa aplicada a Big Data Deportivo

### Presentaciones

- `teoria/Tema_04_IA_Generativa/BDPII_Tema_04_Sesion_01_Prompt_Engineering_y_Posttraining.pdf`: 54 diapositivas.
- `teoria/Tema_04_IA_Generativa/BDPII_Tema_04_Sesion_02_RAG.pdf`: 30 diapositivas.
- `teoria/Tema_04_IA_Generativa/BDPII_Tema_04_Sesion_03_Agentes.pdf`: 36 diapositivas.

Las tres fuentes LaTeX, el estilo Beamer y todas sus imágenes están extraídos y organizados en `fuentes/teoria/Tema_04_IA_Generativa/`.

### Ejercicios

- `practica/Tema_04_IA_Generativa/BDPII_Tema_04_Ejercicios_Sesion_01.pdf`.
- `practica/Tema_04_IA_Generativa/BDPII_Tema_04_Ejercicios_Sesion_02.pdf`.
- `practica/Tema_04_IA_Generativa/BDPII_Tema_04_Ejercicios_Sesion_03.pdf`.
- Fuentes DOCX correspondientes en `fuentes/practica/Tema_04_IA_Generativa/`.

### Programas

- Sesión 2: `programas/Tema_04_IA_Generativa/Sesion_02_RAG/RAG_1.py` y `RAG_1_comentado.py`.
- Sesión 3: `programas/Tema_04_IA_Generativa/Sesion_03_Agentes/flow_lineal.py`, `agent_flow_lineal.py` y `agent_skills_tools.py`.
- `programas/Tema_04_IA_Generativa/requirements.txt`: dependencias comunes.

Los cinco programas superan la comprobación sintáctica de Python. Todavía deben revisarse su documentación, datos de ejemplo, licencia y ejecución reproducible antes de publicarlos como categoría 6.

## Tema 5 - Proyectos integrados

### Presentación

- `teoria/Tema_05_Proyecto_Integrado/BDPII_Tema_05_Proyecto_Integrado.pdf`: 46 diapositivas. Subtítulo: «Del dato en tiempo real al análisis automatizado».

### Fuente

- `fuentes/teoria/Tema_05_Proyecto_Integrado/BDPII_Tema_05_Proyecto_Integrado.tex`, estilo Beamer y logotipos. Fuente reconstruida a partir del PDF: reproduce su texto diapositiva a diapositiva, pero no es el original de los autores.

## Tema 6 - Tendencias y futuro

### Presentación

- `teoria/Tema_06_Tendencias_Futuro/BDPII_Tema_06_Tendencias_Futuro.pdf`: 40 diapositivas. Subtítulo: «Procesamiento Masivo de Datos e IA en el Deporte».

### Fuente

- `fuentes/teoria/Tema_06_Tendencias_Futuro/BDPII_Tema_06_Tendencias_Futuro.tex`, estilo Beamer y logotipos. Fuente reconstruida a partir del PDF: reproduce su texto diapositiva a diapositiva, pero no es el original de los autores.

## Autoría y procedencia

Las tres presentaciones del tema 4 identifican en portada a Alberto Fernández Isabel, Natalia Madrueño Sierro y Rubén Rodríguez Fernández como equipo docente. Este dato no determina por sí solo los porcentajes de autoría intelectual de los materiales. La atribución definitiva y los porcentajes para la declaración de la convocatoria deberán ser confirmados por los tres docentes cuando el inventario esté completo.

Los metadatos de los tres DOCX de ejercicios indican que su última modificación fue realizada por Alberto Fernández Isabel. Se conserva este dato únicamente como información de procedencia editorial, no como determinación definitiva de autoría.

## Estado de publicación

Ninguno de estos archivos se considera todavía versión definitiva para BURJC Digital. Antes de copiarlos a `material_abierto/` deben completarse la auditoría de fuentes e imágenes, el licenciamiento, las atribuciones y la revisión de los materiales pendientes.
