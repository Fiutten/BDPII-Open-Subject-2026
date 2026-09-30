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

El inventario actual contiene la guía docente oficial, los temas 1 a 4 y una guía de estudio específica preparada como categoría 0.

Temas 1 a 3 (procesamiento distribuido, Kafka y Spark Structured Streaming, optimización y escalabilidad):

- cuatro presentaciones, con sus fuentes LaTeX e imágenes separadas en `material_original/fuentes/teoria/`;
- dos enunciados de ejercicios de Kafka y Spark Structured Streaming;
- notebooks, productor Kafka, entorno Docker y un conjunto de datos simulado de telemetría deportiva.

Tema 4:

- tres presentaciones: prompt engineering y post-training, RAG y sistemas basados en agentes;
- tres colecciones de ejercicios, con PDF y fuentes DOCX separadas;
- fuentes editables LaTeX e imágenes de las presentaciones, extraídas del paquete original;
- ejemplos de código para RAG y agentes;

Dentro de `material_original/`, los documentos finales se organizan por temas en `teoria/` y `practica/`; los editables quedan centralizados en `fuentes/`. No se mantienen ZIP redundantes en esta zona de trabajo.

El detalle y la procedencia se documentan en `material_original/INVENTARIO_MATERIALES.md`. Las presentaciones y fuentes de los temas 5 y 6 están pendientes de incorporación.

## Criterios de publicación

Este repositorio es público. Los materiales permanecen en `material_original/` hasta completar la revisión de autoría, derechos, licencias, fuentes y atribuciones. Solo después se copiarán y adaptarán en `material_abierto/`. La guía de estudio ya ha superado esta revisión y está disponible en `material_abierto/00_guias/`.

Se mantendrá un único PDF canónico por material, junto con sus fuentes editables cuando proceda. La entrega de BURJC se generará mediante copias, sin mover ni alterar los originales.
