# BDPII - Material docente en abierto (URJC)

Repositorio de trabajo para preparar la publicación en abierto de **Big Data Processing II**, asignatura del **Máster Universitario en Análisis de Datos Deportivos**, durante el curso **2026-2027**.

## Equipo docente

- **Alberto Fernández Isabel** - profesor responsable.
- **Natalia Madrueño Sierro**.
- **Rubén Rodríguez Fernández**.

## Organización

- `material_original/`: materiales de trabajo, organizados por tipo y por tema del programa.
- `material_abierto/00_guias/`: guía de estudio de categoría 0 y documentación de referencia.
- `material_abierto/01_apuntes/`: apuntes de apoyo (categoría 1).
- `material_abierto/02_presentaciones/`: presentaciones, atribuciones y fuentes editables (categoría 2).
- `material_abierto/03_practicas/`: prácticas, fuentes editables y soluciones orientativas (categoría 3).
- `material_abierto/06_programas/`: programas y notebooks reutilizables de forma autónoma (categoría 6).
- `material_abierto/08_otros_materiales/`: infografías u otros materiales complementarios (categoría 8).
- `material_abierto/99_burjc_package/`: área de construcción y respaldo del paquete final.
- `BURJC/01_SUBIR/`: copias de los ficheros definitivos que se adjuntarán al depósito.
- `BURJC/02_APOYO/`: instrucciones, metadatos y sumas de comprobación; no se sube al depósito.
- `scripts/`: automatización de construcción y validación.

## Material incorporado

El inventario actual contiene la guía docente oficial, materiales teóricos de los seis temas, actividades prácticas y una guía de estudio específica preparada como categoría 0.

Temas 1 a 3 (procesamiento distribuido, Kafka y Spark Structured Streaming, optimización y escalabilidad):

- cuatro presentaciones, con sus fuentes LaTeX e imágenes separadas en `material_original/fuentes/teoria/`;
- dos enunciados de ejercicios de Kafka y Spark Structured Streaming;
- notebooks, productor Kafka, entorno Docker y un conjunto de datos simulado de telemetría deportiva.

Tema 4:

- tres presentaciones: prompt engineering y post-training, RAG y sistemas basados en agentes;
- tres colecciones de ejercicios, con PDF y fuentes DOCX separadas;
- fuentes editables LaTeX e imágenes de las presentaciones, extraídas del paquete original;
- ejemplos de código para RAG y agentes;

Temas 5 y 6:

- una presentación de 46 diapositivas para el tema 5, centrada en arquitecturas integradas, análisis automatizado, RAG multimodal y visualización conversacional;
- un ejercicio de seguimiento del tema 5 para construir un agente Text-to-SQL con Spark y LangGraph;
- una presentación de 40 diapositivas para el tema 6 sobre tendencias, infraestructura emergente, analítica prescriptiva y gobernanza;
- fuentes LaTeX editables de ambos temas, verificadas mediante compilación;
- el enunciado de la práctica final, separado del tema 5 porque es una actividad evaluable transversal que integra el temario completo.

Dentro de `material_original/`, los documentos finales se organizan por temas en `teoria/` y `practica/`; los editables quedan centralizados en `fuentes/`. No se mantienen ZIP redundantes en esta zona de trabajo.

El detalle y la procedencia se documentan en `material_original/INVENTARIO_MATERIALES.md`.

## Edición abierta y entrega

La edición revisada se encuentra en `material_abierto/` y presenta las categorías 0, 2, 3 y 6. Los documentos se publican bajo CC BY-SA 4.0 y el código bajo MIT. Los logotipos y marcas institucionales quedan expresamente fuera de la licencia. Las imágenes de la versión de trabajo cuya reutilización no podía acreditarse se han retirado de la edición abierta y sustituido por esquemas originales.

`material_original/` conserva las versiones de trabajo y sus fuentes sin alterarlas. `BURJC/01_SUBIR/` se genera mediante copias de los tres ficheros previstos para el depósito único: libro principal, editables y código. `BURJC/02_APOYO/` contiene metadatos, justificación de criterios, declaraciones y comprobaciones.

El libro y los paquetes se consideran candidatos hasta incorporar el SWHID verificado de la versión pública del software y cerrar los porcentajes de autoría del Anexo V.
