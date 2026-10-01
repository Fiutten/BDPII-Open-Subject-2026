from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "material_original" / "fuentes" / "guias" / "Guia_de_estudio_Big_Data_Processing_II_2026-2027.docx"
OPEN_OUT = ROOT / "material_abierto" / "00_guias" / "editables" / "Guia_de_estudio_Big_Data_Processing_II_2026-2027.docx"
CC_BADGE = ROOT / "material_abierto" / "assets" / "cc_by_sa_4_0.png"

NAVY = "17365D"
BLUE = "1F4E79"
TEAL = "008C95"
LIGHT_BLUE = "DDEBF7"
LIGHT_TEAL = "DDEFEF"
LIGHT_GRAY = "F2F2F2"
DARK = "222222"
MID = "666666"
WHITE = "FFFFFF"


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=100, start=120, bottom=100, end=120):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def keep_paragraph(paragraph, keep_next=False):
    p_pr = paragraph._p.get_or_add_pPr()
    if keep_next:
        keep = OxmlElement("w:keepNext")
        p_pr.append(keep)
    widow = OxmlElement("w:widowControl")
    p_pr.append(widow)


def add_field(paragraph, instruction):
    run = paragraph.add_run()
    fld_char_begin = OxmlElement("w:fldChar")
    fld_char_begin.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = instruction
    fld_char_end = OxmlElement("w:fldChar")
    fld_char_end.set(qn("w:fldCharType"), "end")
    run._r.extend([fld_char_begin, instr_text, fld_char_end])


def add_hyperlink(paragraph, text, url, color=TEAL):
    part = paragraph.part
    rel_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), rel_id)
    run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    c = OxmlElement("w:color")
    c.set(qn("w:val"), color)
    r_pr.append(c)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    r_pr.append(underline)
    run.append(r_pr)
    t = OxmlElement("w:t")
    t.text = text
    run.append(t)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def page_break(doc):
    p = doc.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)


def add_title(doc, text, subtitle=None):
    p = doc.add_paragraph(style="Title")
    p.add_run(text)
    if subtitle:
        p2 = doc.add_paragraph(style="Subtitle")
        p2.add_run(subtitle)


def add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    keep_paragraph(p, True)
    return p


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.add_run(item)
        keep_paragraph(p)


def add_numbered(doc, items):
    for number, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.55)
        p.paragraph_format.first_line_indent = Cm(-0.55)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.0
        p.add_run(f"{number}. ").bold = True
        p.add_run(item)
        keep_paragraph(p)


def add_callout(doc, title, body, fill=LIGHT_TEAL):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    cell = table.cell(0, 0)
    set_cell_shading(cell, fill)
    set_cell_margins(cell, 150, 180, 150, 180)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(title)
    r.bold = True
    r.font.color.rgb = RGBColor.from_string(NAVY)
    p2 = cell.add_paragraph(body)
    p2.paragraph_format.space_after = Pt(0)
    keep_paragraph(p2)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_topic_page(doc, number, title, description, objectives, materials, plan, personal, availability=None):
    add_heading(doc, f"Tema {number}. {title}", 1)
    p = doc.add_paragraph(description)
    p.paragraph_format.space_after = Pt(8)
    if availability:
        add_callout(doc, availability[0], availability[1], availability[2])
    add_heading(doc, "Objetivos de trabajo", 2)
    add_bullets(doc, objectives)
    add_heading(doc, "Materiales", 2)
    add_bullets(doc, materials)
    add_heading(doc, "Plan de trabajo recomendado", 2)
    add_numbered(doc, plan)
    add_heading(doc, "Trabajo personal recomendado", 2)
    doc.add_paragraph(personal)


doc = Document()
section = doc.sections[0]
section.top_margin = Cm(1.8)
section.bottom_margin = Cm(1.7)
section.left_margin = Cm(2.0)
section.right_margin = Cm(2.0)

styles = doc.styles
normal = styles["Normal"]
normal.font.name = "Aptos"
normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Aptos")
normal.font.size = Pt(10.5)
normal.font.color.rgb = RGBColor.from_string(DARK)
normal.paragraph_format.space_after = Pt(5)
normal.paragraph_format.line_spacing = 1.08

for name, size, color in (("Title", 30, DARK), ("Subtitle", 15, MID), ("Heading 1", 20, NAVY), ("Heading 2", 13, BLUE), ("Heading 3", 11, TEAL)):
    st = styles[name]
    st.font.name = "Aptos Display" if name in ("Title", "Heading 1") else "Aptos"
    st._element.rPr.rFonts.set(qn("w:eastAsia"), st.font.name)
    st.font.size = Pt(size)
    st.font.color.rgb = RGBColor.from_string(color)
    if name.startswith("Heading"):
        st.font.bold = True
        st.paragraph_format.space_before = Pt(10)
        st.paragraph_format.space_after = Pt(5)

styles["List Bullet"].font.name = "Aptos"
styles["List Bullet"].font.size = Pt(10.5)
styles["List Number"].font.name = "Aptos"
styles["List Number"].font.size = Pt(10.5)

# Header and footer.
header = section.header
hp = header.paragraphs[0]
hp.text = "UNIVERSIDAD REY JUAN CARLOS  ·  MATERIAL DOCENTE EN ABIERTO"
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
for r in hp.runs:
    r.font.name = "Aptos"
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor.from_string(MID)

fp = section.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
rr = fp.add_run("Big Data Processing II · Guía de estudio  |  ")
rr.font.name = "Aptos"
rr.font.size = Pt(8)
rr.font.color.rgb = RGBColor.from_string(MID)
add_field(fp, "PAGE")

# Cover.
band = doc.add_table(rows=1, cols=1)
band.alignment = WD_TABLE_ALIGNMENT.CENTER
band.cell(0, 0).text = "MATERIAL DOCENTE EN ABIERTO"
set_cell_shading(band.cell(0, 0), NAVY)
set_cell_margins(band.cell(0, 0), 170, 180, 170, 180)
bp = band.cell(0, 0).paragraphs[0]
bp.alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in bp.runs:
    r.bold = True
    r.font.name = "Aptos"
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor.from_string(WHITE)

doc.add_paragraph().paragraph_format.space_after = Pt(55)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Big Data Processing II")
r.font.name = "Aptos Display"
r.font.size = Pt(32)
r.bold = True
r.font.color.rgb = RGBColor.from_string(DARK)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Guía de estudio")
r.font.name = "Aptos Display"
r.font.size = Pt(22)
r.font.color.rgb = RGBColor.from_string(BLUE)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(14)
r = p.add_run("Máster Universitario en Análisis de Datos Deportivos")
r.font.size = Pt(13)
r.bold = True
p2 = doc.add_paragraph("Curso 2026–2027 · 3 ECTS · segundo semestre")
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p2.runs[0].font.size = Pt(11)
p2.runs[0].font.color.rgb = RGBColor.from_string(MID)

doc.add_paragraph().paragraph_format.space_after = Pt(45)
authors = doc.add_table(rows=4, cols=1)
authors.alignment = WD_TABLE_ALIGNMENT.CENTER
authors.autofit = True
for cell in authors.column_cells(0):
    set_cell_margins(cell, 70, 180, 70, 180)
names = [
    ("Equipo docente", True),
    ("Alberto Fernández Isabel · profesor responsable", False),
    ("Natalia Madrueño Sierro", False),
    ("Rubén Rodríguez Fernández", False),
]
for cell, (text, bold) in zip(authors.column_cells(0), names):
    cell.text = text
    pp = cell.paragraphs[0]
    pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in pp.runs:
        run.bold = bold
        run.font.size = Pt(10.5 if not bold else 11)
        run.font.color.rgb = RGBColor.from_string(NAVY if bold else DARK)

doc.add_paragraph().paragraph_format.space_after = Pt(28)
lic = doc.add_table(rows=1, cols=1)
lic.alignment = WD_TABLE_ALIGNMENT.CENTER
cell = lic.cell(0, 0)
set_cell_shading(cell, LIGHT_BLUE)
set_cell_margins(cell, 140, 170, 140, 170)
p = cell.paragraphs[0]
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("© 2026 Alberto Fernández Isabel, Natalia Madrueño Sierro y Rubén Rodríguez Fernández. Algunos derechos reservados.")
r.bold = True
p2 = cell.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p2.add_run("Licencia: ")
add_hyperlink(p2, "Creative Commons Atribución–CompartirIgual 4.0 Internacional (CC BY-SA 4.0)", "https://creativecommons.org/licenses/by-sa/4.0/deed.es")
p3 = cell.add_paragraph()
p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
p3.add_run("Depósito institucional: ")
add_hyperlink(p3, "BURJC Digital", "https://burjcdigital.urjc.es")

if CC_BADGE.exists():
    badge = doc.add_paragraph()
    badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    badge.add_run().add_picture(str(CC_BADGE), width=Inches(2.05))

page_break(doc)

add_heading(doc, "Información de publicación", 1)
doc.add_paragraph("Material docente en abierto de la Universidad Rey Juan Carlos.")
doc.add_paragraph(
    "© 2026 Alberto Fernández Isabel, Natalia Madrueño Sierro y Rubén Rodríguez Fernández. "
    "Algunos derechos reservados. Esta obra se distribuye bajo la licencia Creative Commons "
    "Atribución–CompartirIgual 4.0 Internacional, disponible en "
    "https://creativecommons.org/licenses/by-sa/4.0/deed.es."
)
doc.add_paragraph(
    "La licencia se aplica al contenido original de la obra. Los logotipos, marcas y materiales de terceros "
    "conservan su régimen jurídico propio y quedan excluidos de la licencia, salvo indicación expresa."
)
add_heading(doc, "Declaración sobre herramientas de inteligencia artificial generativa", 2)
doc.add_paragraph(
    "En la preparación de esta guía se emplearon herramientas generativas de texto como apoyo para la "
    "organización editorial, la redacción inicial de determinados textos de enlace y la comprobación de "
    "coherencia. No se utilizaron para sustituir el diseño docente, los contenidos técnicos de las "
    "presentaciones ni la autoría de los ejercicios. Todo el contenido ha sido revisado, editado, validado "
    "y aprobado por el equipo autor, que asume plena responsabilidad sobre la versión final."
)

page_break(doc)

# Purpose and material map.
add_heading(doc, "1. Finalidad y alcance", 1)
doc.add_paragraph(
    "Esta guía organiza el trabajo recomendado para seguir Big Data Processing II mediante los materiales docentes del repositorio. "
    "Traduce el temario oficial en una secuencia de estudio que integra teoría, ejercicios, programas y trabajo personal, sin sustituir la guía docente ni las indicaciones del equipo docente."
)
doc.add_paragraph(
    "La asignatura profundiza en el procesamiento distribuido y en tiempo real de datos deportivos, la optimización de pipelines y la integración responsable de inteligencia artificial generativa. Su enfoque es aplicado: cada bloque culmina en decisiones de diseño, implementación, evaluación o comunicación técnica."
)
add_callout(
    doc,
    "Edición y estado de los materiales",
    "Esta edición se basa en la guía docente oficial publicada el 7 de julio de 2026 y en los materiales disponibles en el repositorio a 30 de septiembre de 2026. Las presentaciones de los seis temas están incorporadas. Las fuentes LaTeX de los temas 5 y 6 son reconstrucciones documentadas a partir de sus PDF, no los originales de autor.",
    LIGHT_BLUE,
)

add_heading(doc, "2. Mapa general de materiales", 1)
rows = [
    ("1", "Procesamiento distribuido", "Presentación · 66 diapositivas", "Notebook de streaming y solución"),
    ("2", "Streaming en tiempo real", "Kafka · 44; Spark · 60 diapositivas", "2 enunciados; Kafka, Docker, PySpark y datos"),
    ("3", "Optimización y escalabilidad", "Presentación · 36 diapositivas", "Análisis y diseño de pipelines"),
    ("4", "IA generativa", "3 presentaciones · 120 diapositivas", "3 hojas de ejercicios; RAG y agentes"),
    ("5", "Proyectos integrados", "Presentación · 46 diapositivas", "Ejercicio Text-to-SQL con Spark y LangGraph"),
    ("6", "Tendencias y futuro", "Presentación · 40 diapositivas", "Análisis crítico, ético y legal"),
]
table = doc.add_table(rows=1, cols=4)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.style = "Table Grid"
hdr = table.rows[0]
set_repeat_table_header(hdr)
for i, text in enumerate(("Tema", "Bloque", "Teoría", "Práctica / aplicación")):
    hdr.cells[i].text = text
    set_cell_shading(hdr.cells[i], NAVY)
    hdr.cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    for run in hdr.cells[i].paragraphs[0].runs:
        run.bold = True
        run.font.color.rgb = RGBColor.from_string(WHITE)
        run.font.size = Pt(9)
for row in rows:
    cells = table.add_row().cells
    for i, text in enumerate(row):
        cells[i].text = text
        set_cell_margins(cells[i], 75, 80, 75, 80)
        if int(row[0]) % 2 == 0:
            set_cell_shading(cells[i], LIGHT_GRAY)
        for run in cells[i].paragraphs[0].runs:
            run.font.size = Pt(8.7)

page_break(doc)

# Results and method.
add_heading(doc, "3. Resultados de aprendizaje y método de uso", 1)
doc.add_paragraph(
    "La guía docente vincula la asignatura con resultados de aprendizaje relacionados con el trabajo interdisciplinar, el autoaprendizaje, la comunicación técnica, la implantación y optimización de tecnologías Big Data, la automatización y la adaptación de tendencias como el análisis en tiempo real y la inteligencia artificial."
)
add_heading(doc, "Resultados que vertebran el itinerario", 2)
result_rows = [
    ("COM1 · COM4", "Colaborar y comunicar", "Trabajo en equipo, memoria técnica y exposición oral."),
    ("COM3", "Aprender de forma autónoma", "Contrastar documentación y fuentes científicas actuales."),
    ("COM6 · COM7", "Construir soluciones Big Data", "Ingesta, procesamiento, almacenamiento y optimización."),
    ("COM11 · COM12", "Automatizar y adaptar tendencias", "Streaming, IA generativa, RAG y agentes."),
    ("CON4 · CON8", "Seleccionar tecnologías", "Comparar plataformas, arquitecturas y metodologías a escala."),
    ("HAB1 · HAB4", "Resolver problemas deportivos", "Diseñar soluciones aplicadas, innovadoras y justificadas."),
]
table = doc.add_table(rows=1, cols=3)
table.style = "Table Grid"
table.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, text in enumerate(("Resultados", "Eje", "Evidencia esperada")):
    table.rows[0].cells[i].text = text
    set_cell_shading(table.rows[0].cells[i], BLUE)
    for run in table.rows[0].cells[i].paragraphs[0].runs:
        run.bold = True
        run.font.color.rgb = RGBColor.from_string(WHITE)
        run.font.size = Pt(9)
for row in result_rows:
    cells = table.add_row().cells
    for i, text in enumerate(row):
        cells[i].text = text
        set_cell_margins(cells[i], 80, 90, 80, 90)
        for run in cells[i].paragraphs[0].runs:
            run.font.size = Pt(9)

add_heading(doc, "Secuencia recomendada para cada bloque", 2)
add_numbered(doc, [
    "Leer los objetivos del tema y activar los conocimientos previos necesarios.",
    "Estudiar la presentación o material teórico, anotando conceptos, decisiones y dudas.",
    "Ejecutar o inspeccionar los ejemplos de código antes de modificar sus parámetros o entradas.",
    "Resolver la actividad práctica y justificar las decisiones adoptadas con evidencias reproducibles.",
    "Sintetizar lo aprendido en un esquema, informe breve o explicación técnica dirigida a un stakeholder.",
    "Comprobar la lista de autoevaluación y registrar los aspectos que requieren tutoría o repaso.",
])
add_callout(
    doc,
    "Integridad académica y uso de IA",
    "En actividades evaluables, las herramientas basadas en inteligencia artificial solo pueden utilizarse cuando el enunciado o el profesorado lo autoricen expresamente y dentro de los usos indicados. En el estudio autónomo deben emplearse de forma ética, legal, honesta y transparente.",
    "FFF2CC",
)

page_break(doc)

add_topic_page(
    doc,
    1,
    "Procesamiento de Big Data en entornos distribuidos",
    "Bloque introductorio que conecta el análisis deportivo en vivo con la evolución desde el procesamiento batch hacia arquitecturas distribuidas y orientadas a eventos.",
    [
        "Comprender la transición de batch a streaming en analítica deportiva.",
        "Distinguir mensajería distribuida, motores de procesamiento y almacenamiento.",
        "Relacionar arquitecturas Lambda y Kappa con requisitos de latencia y consistencia.",
        "Justificar decisiones de diseño para casos de uso deportivos en vivo.",
    ],
    [
        "BDPII_Tema_01_Procesamiento_Big_Data_Distribuido.pdf.",
        "streaming.ipynb y streaming_soluciones.ipynb.",
        "Bibliografía básica de la guía docente: Gama (2010) y Marz & Warren (2015).",
    ],
    [
        "Revisar la evolución del análisis deportivo y distinguir dato histórico, microbatch y streaming.",
        "Construir un mapa de fuentes, broker, procesamiento y destinos para un caso deportivo.",
        "Comparar arquitecturas Lambda y Kappa atendiendo a complejidad, latencia y reprocesamiento.",
        "Ejecutar o inspeccionar el notebook y contrastar el procesamiento directo con el incremental.",
        "Redactar una decisión de arquitectura indicando requisitos, supuestos y riesgos.",
    ],
    "Proponer una arquitectura de alto nivel para monitorizar carga o fatiga durante una competición y explicar por qué la información pierde valor si llega tarde.",
)

page_break(doc)

add_topic_page(
    doc,
    2,
    "Procesamiento de flujos de datos en tiempo real",
    "Bloque aplicado a la ingestión y al procesamiento continuo con Apache Kafka y Spark Structured Streaming, utilizando telemetría deportiva simulada.",
    [
        "Explicar productores, consumidores, topics, particiones, offsets y grupos de consumo en Kafka.",
        "Diseñar un flujo tolerante a fallos y escalable para eventos deportivos.",
        "Aplicar Structured Streaming con DataFrames, ventanas y tiempo de evento.",
        "Razonar sobre latencia, estado, watermarks y modos de salida.",
    ],
    [
        "BDPII_Tema_02_Apache_Kafka.pdf.",
        "BDPII_Tema_02_Spark_Structured_Streaming.pdf.",
        "Enunciados de Apache Kafka y Spark Structured Streaming.",
        "producer.py, sensores_deportivos_fatiga.csv, docker-compose.yml y spark_streaming.ipynb.",
    ],
    [
        "Estudiar Kafka y representar el recorrido de un evento desde el productor hasta sus consumidores.",
        "Resolver el enunciado de Kafka utilizando la descripción del conjunto de datos de sensores.",
        "Estudiar Structured Streaming y distinguir tiempo de proceso de tiempo de evento.",
        "Levantar o inspeccionar el entorno Docker y completar el notebook de streaming.",
        "Probar ventanas, agregaciones y tolerancia a datos tardíos; documentar las salidas observadas.",
        "Comparar los resultados con los requisitos del caso y proponer ajustes de particionado y recursos.",
    ],
    "Entregar una traza reproducible de un flujo Kafka–Spark y explicar cómo se preservan orden, escalabilidad y utilidad temporal de la información.",
)

page_break(doc)

add_topic_page(
    doc,
    3,
    "Optimización y escalabilidad de pipelines deportivos",
    "Bloque centrado en diagnosticar cuellos de botella y convertir un prototipo funcional en un pipeline eficiente, observable y desplegable.",
    [
        "Identificar costes de particionado, shuffle, serialización, estado y almacenamiento.",
        "Aplicar paralelización, caching y elección de particiones con criterio.",
        "Utilizar métricas y herramientas de monitorización para formular hipótesis.",
        "Comparar alternativas de despliegue on-premises y cloud.",
    ],
    [
        "BDPII_Tema_03_Optimizacion_Escalabilidad.pdf.",
        "Pipelines y ejercicios construidos en los temas 1 y 2.",
        "Bibliografía básica: Karau, Polak & Warren (2026), High Performance Spark.",
    ],
    [
        "Representar el pipeline de ingestión, procesamiento, almacenamiento y consumo.",
        "Localizar operaciones costosas y proponer métricas antes de modificar la configuración.",
        "Evaluar particionado, skew, shuffles, caching y paralelismo con ejemplos concretos.",
        "Definir un experimento controlado con línea base, cambio aislado y criterio de éxito.",
        "Documentar el compromiso entre coste, latencia, rendimiento y mantenibilidad.",
    ],
    "Preparar una ficha de diagnóstico con síntoma, evidencia, hipótesis, intervención y métrica de verificación para un pipeline deportivo en streaming.",
)

page_break(doc)

add_topic_page(
    doc,
    4,
    "Inteligencia Artificial Generativa aplicada a Big Data Deportivo",
    "Bloque en tres sesiones: control del comportamiento mediante prompting y post-training; control de la información mediante RAG; y control del flujo y la acción mediante agentes, tools y arquitecturas cognitivas.",
    [
        "Explicar las capacidades y límites de un LLM en un sistema de datos deportivo.",
        "Diseñar prompts evaluables y reconocer cuándo el prompting no resuelve la falta de información.",
        "Construir conceptualmente un flujo RAG y evaluar recuperación y respuesta.",
        "Distinguir workflow, agente, skill y tool; controlar coste, seguridad y trazabilidad.",
    ],
    [
        "Sesión 1: Prompt Engineering y Post-training; ejercicios asociados.",
        "Sesión 2: Retrieval-Augmented Generation (RAG); ejercicios y RAG_1.py / RAG_1_comentado.py.",
        "Sesión 3: Sistemas basados en agentes; ejercicios y tres programas de workflows/agentes.",
        "requirements.txt y bibliografía básica: Hu et al. (2025), Hands-on LLM-based Agents.",
    ],
    [
        "Separar generación lingüística, acceso a información, cálculo y ejecución de acciones.",
        "Resolver los ejercicios de la sesión 1 y definir criterios de calidad para las respuestas.",
        "Estudiar la arquitectura RAG; ejecutar o inspeccionar los ejemplos y analizar el efecto del chunking y la recuperación.",
        "Estudiar agentes, estados, tools y patrones de orquestación; comparar flujo lineal y decisión autónoma.",
        "Diseñar un caso deportivo indicando datos, controles humanos, registros, costes y riesgos.",
        "Revisar privacidad, propiedad intelectual, sesgos y necesidad de validación experta.",
    ],
    "Diseñar una solución que genere un informe deportivo trazable a partir de datos autorizados, separando claramente hechos recuperados, cálculos, inferencias y texto generado.",
)

page_break(doc)

add_topic_page(
    doc,
    5,
    "Proyectos integrados: del dato en tiempo real al análisis automatizado",
    "Bloque de integración tecnológica sobre sistemas que combinan ingestión continua, cómputo en streaming, recuperación de información, agentes e interfaces conversacionales. El ejercicio Text-to-SQL aplica estos contenidos; la práctica final es una actividad evaluable transversal sobre el temario completo.",
    [
        "Comprender la transición desde el Business Intelligence retrospectivo hacia la analítica prescriptiva en tiempo real.",
        "Relacionar Kafka y Spark Structured Streaming dentro de una arquitectura completa de ingestión y procesamiento.",
        "Explicar cómo los flujos agénticos, las tools y el patrón ReAct conectan lenguaje natural con datos deportivos.",
        "Analizar el papel de RAG multimodal, la generación de narrativas y las interfaces conversacionales.",
    ],
    [
        "BDPII_Tema_05_Proyecto_Integrado.pdf · 46 diapositivas.",
        "Ejercicio Text-to-SQL Agent con LangGraph y Apache Spark: README, código inicial, generador de datos y dependencias.",
        "Materiales de los temas 1–4 como base conceptual y técnica.",
    ],
    [
        "Estudiar el recorrido completo desde la telemetría hasta la decisión y representar los componentes del sistema.",
        "Revisar particiones, semántica exactly-once, estado y watermarks en la integración Kafka-Spark.",
        "Comparar workflows deterministas y agentes que consultan datos mediante tools.",
        "Analizar cómo RAG multimodal y la generación de narrativas añaden contexto sin sustituir los cálculos deterministas.",
        "Completar el ejercicio Text-to-SQL: generar los datos, registrar las vistas de Spark y construir el agente ReAct.",
        "Validar el agente con consultas deportivas y comprobar que las respuestas se apoyan en los datos ejecutados.",
    ],
    "Elaborar un diagrama razonado del sistema y una memoria breve del ejercicio Text-to-SQL que documente arquitectura, consultas probadas, resultados y límites del agente.",
)

page_break(doc)

add_topic_page(
    doc,
    6,
    "Tendencias y futuro del procesamiento masivo de datos en el deporte",
    "Bloque final de análisis crítico sobre tecnologías emergentes, analítica predictiva y prescriptiva, y los retos éticos y legales del uso masivo de datos e inteligencia artificial.",
    [
        "Evaluar tendencias sin confundir novedad con adecuación al problema.",
        "Distinguir analítica descriptiva, predictiva y prescriptiva.",
        "Identificar impactos sobre privacidad, equidad, seguridad y responsabilidad.",
        "Formular recomendaciones técnicas justificadas con fuentes fiables y actuales.",
    ],
    [
        "BDPII_Tema_06_Tendencias_Futuro.pdf · 40 diapositivas.",
        "Guía docente oficial y bibliografía básica y complementaria.",
        "Documentación técnica oficial y literatura científica seleccionada por el equipo docente.",
    ],
    [
        "Seleccionar una tendencia relevante para el análisis deportivo y delimitar el problema que pretende resolver.",
        "Contrastar al menos una fuente técnica primaria y una referencia científica.",
        "Analizar madurez, datos requeridos, coste, integración, explicabilidad y riesgos.",
        "Distinguir predicción de recomendación y explicitar los supuestos de cualquier intervención prescriptiva.",
        "Preparar una recomendación de adopción, piloto limitado o rechazo razonado.",
    ],
    "Elaborar una nota de decisión breve para un responsable deportivo que incluya oportunidad, evidencia, riesgos ético-legales, salvaguardas y próximos pasos.",
)

page_break(doc)

# 15 study units.
add_heading(doc, "4. Planificación orientativa por unidades de trabajo", 1)
doc.add_paragraph(
    "La guía docente sitúa las clases, los ejercicios, los trabajos colectivos y las tutorías entre las semanas 1 y 15. La siguiente secuencia distribuye el aprendizaje en quince unidades; cada unidad puede ocupar una o más sesiones según el calendario oficial del grupo."
)
units = [
    ("1", "T1 · Del batch al streaming", "Valor temporal del dato, arquitectura distribuida y caso deportivo."),
    ("2", "T1 · Mensajería y arquitecturas", "Broker, motores y comparación Lambda/Kappa; notebook de streaming."),
    ("3", "T2 · Fundamentos de Kafka", "Topics, particiones, productores, consumidores y contratos de eventos."),
    ("4", "T2 · Kafka aplicado", "Enunciado, productor y telemetría deportiva; escalabilidad y tolerancia a fallos."),
    ("5", "T2 · Structured Streaming", "DataFrames, ventanas, estado, watermarks y notebook PySpark."),
    ("6", "T3 · Diagnóstico", "Pipeline completo, métricas, particionado, shuffles y skew."),
    ("7", "T3 · Producción", "Caching, recursos, observabilidad y opciones on-premises/cloud."),
    ("8", "T4 · Prompting", "Capacidades y límites del LLM; especificación y evaluación de prompts."),
]
table = doc.add_table(rows=1, cols=3)
table.style = "Table Grid"
for i, text in enumerate(("Unidad", "Foco", "Actividad y evidencia")):
    table.rows[0].cells[i].text = text
    set_cell_shading(table.rows[0].cells[i], NAVY)
    for run in table.rows[0].cells[i].paragraphs[0].runs:
        run.bold = True
        run.font.color.rgb = RGBColor.from_string(WHITE)
        run.font.size = Pt(9)
for idx, row in enumerate(units):
    cells = table.add_row().cells
    for i, text in enumerate(row):
        cells[i].text = text
        set_cell_margins(cells[i], 95, 90, 95, 90)
        if idx % 2:
            set_cell_shading(cells[i], LIGHT_GRAY)
        for run in cells[i].paragraphs[0].runs:
            run.font.size = Pt(9)
add_callout(doc, "Carga de trabajo", "La guía docente establece 75 horas totales: 30 horas presenciales/relacionadas y 45 horas de preparación autónoma. Esta planificación debe ajustarse a las fechas y actividades concretas comunicadas por el profesorado.", LIGHT_BLUE)

page_break(doc)
add_heading(doc, "4. Planificación orientativa por unidades de trabajo (continuación)", 1)
units2 = [
    ("9", "T4 · RAG", "Recuperación, chunking, vectores, trazabilidad y evaluación de respuestas."),
    ("10", "T4 · Agentes", "Estados, tools, workflows, costes, seguridad y supervisión humana."),
    ("11", "T5 · Arquitectura integrada", "Kafka, Spark, estado, RAG y agentes en un flujo de extremo a extremo."),
    ("12", "T5 · Text-to-SQL", "Datos sintéticos, vistas Spark SQL, tools y construcción del agente ReAct."),
    ("13", "T5 · Narrativas e interfaces", "RAG multimodal, validación de respuestas y visualización conversacional."),
    ("14", "T6 · Tendencias", "Fuentes fiables, madurez, integración, predicción y prescripción."),
    ("15", "T6 · Ética, legalidad y síntesis", "Privacidad, equidad, responsabilidad, límites y decisión final."),
]
table = doc.add_table(rows=1, cols=3)
table.style = "Table Grid"
for i, text in enumerate(("Unidad", "Foco", "Actividad y evidencia")):
    table.rows[0].cells[i].text = text
    set_cell_shading(table.rows[0].cells[i], NAVY)
    for run in table.rows[0].cells[i].paragraphs[0].runs:
        run.bold = True
        run.font.color.rgb = RGBColor.from_string(WHITE)
        run.font.size = Pt(9)
for idx, row in enumerate(units2):
    cells = table.add_row().cells
    for i, text in enumerate(row):
        cells[i].text = text
        set_cell_margins(cells[i], 105, 90, 105, 90)
        if idx % 2:
            set_cell_shading(cells[i], LIGHT_GRAY)
        for run in cells[i].paragraphs[0].runs:
            run.font.size = Pt(9)

session_plan = [
    ("1", "Tema 1", "Del procesamiento por lotes al streaming; valor temporal del dato.", "Presentación del tema 1, diapositivas 1–18.", "Distinguir batch, microbatch y streaming y relacionarlos con decisiones deportivas.", "Mapa conceptual y discusión de un caso de monitorización en vivo.", "Resumir requisitos de latencia, consistencia y disponibilidad del caso elegido."),
    ("2", "Tema 1", "Mensajería, motores distribuidos y arquitecturas Lambda y Kappa.", "Presentación del tema 1, diapositivas 19–66; notebook streaming.ipynb.", "Comparar alternativas de arquitectura y justificar sus compromisos.", "Inspección del notebook y diseño de una arquitectura de alto nivel.", "Completar el notebook y redactar una decisión arquitectónica razonada."),
    ("3", "Tema 2", "Fundamentos de Kafka: broker, topics, particiones y offsets.", "Presentación Apache Kafka; documentación oficial de Apache Kafka.", "Explicar el recorrido de un evento y la función de cada componente.", "Representación del flujo productor-broker-consumidor.", "Preparar un esquema de topics, claves y particiones para telemetría deportiva."),
    ("4", "Tema 2", "Productores, consumidores, grupos, replicación y tolerancia a fallos.", "Presentación Apache Kafka; enunciado Kafka; producer.py y datos de sensores.", "Construir una ingesta reproducible y analizar escalabilidad y fallos.", "Ejecución guiada del productor y resolución del enunciado.", "Documentar configuración, pruebas, resultados y tratamiento de errores."),
    ("5", "Tema 2", "Spark Structured Streaming: DataFrames, ventanas, estado y watermarks.", "Presentación Spark Structured Streaming; enunciado; docker-compose.yml y notebook PySpark.", "Procesar eventos con semántica temporal y manejar datos tardíos.", "Construcción de consultas, ventanas y agregaciones sobre Kafka.", "Completar el notebook y comparar modos de salida y políticas de watermark."),
    ("6", "Tema 3", "Diagnóstico de rendimiento: particionado, shuffle, skew y serialización.", "Presentación del tema 3; pipelines desarrollados en los temas 1 y 2.", "Identificar cuellos de botella a partir de evidencias y métricas.", "Lectura de planes de ejecución y formulación de hipótesis.", "Elaborar una ficha de diagnóstico con línea base y criterio de éxito."),
    ("7", "Tema 3", "Optimización, recursos, observabilidad y despliegue.", "Presentación del tema 3; interfaces de monitorización de Spark y Kafka.", "Proponer mejoras medibles y distinguir opciones locales y cloud.", "Experimento controlado con un cambio aislado.", "Comparar resultados y justificar coste, latencia y mantenibilidad."),
    ("8", "Tema 4", "Prompt engineering y límites de los modelos de lenguaje.", "Presentación sesión 1; hoja de ejercicios de prompting.", "Diseñar prompts evaluables y reconocer límites y riesgos.", "Revisión de prompts y definición de criterios de calidad.", "Resolver los ejercicios y registrar iteraciones, fallos y mejoras."),
    ("9", "Tema 4", "RAG: ingesta, fragmentación, embeddings, recuperación y respuesta.", "Presentación sesión 2; ejercicios; RAG_1.py y RAG_1_comentado.py.", "Construir un flujo RAG trazable y evaluar recuperación y respuesta.", "Ejecución y análisis del ejemplo RAG con corpus deportivo.", "Comparar configuraciones de recuperación y documentar evidencias y límites."),
    ("10", "Tema 4", "Agentes, tools, skills, estado y supervisión humana.", "Presentación sesión 3; ejercicios; programas de workflows y agentes.", "Distinguir workflow y agente y controlar coste, seguridad y bucles.", "Comparación de flujo lineal y flujo agéntico.", "Implementar una variante controlada y justificar guardas y criterios de parada."),
    ("11", "Tema 5", "Arquitectura integrada Kafka-Spark-RAG-agentes.", "Presentación del tema 5; materiales de los temas 1 a 4.", "Integrar ingestión, cómputo, recuperación y decisión en un sistema coherente.", "Diseño de un diagrama de extremo a extremo.", "Documentar contratos, estado, observabilidad y puntos de validación humana."),
    ("12", "Tema 5", "Agente Text-to-SQL con Spark y LangGraph.", "README, agent.py, main.py y generate_data.py del ejercicio Text-to-SQL.", "Conectar lenguaje natural con consultas SQL ejecutadas sobre datos deportivos.", "Generación de datos, registro de vistas y construcción de tools.", "Completar los TODO, probar consultas y conservar evidencias de ejecución."),
    ("13", "Tema 5", "RAG multimodal, narrativas e interfaces conversacionales.", "Presentación del tema 5; resultado del ejercicio Text-to-SQL.", "Separar cálculo determinista, recuperación, inferencia y generación narrativa.", "Diseño de una respuesta trazable para distintos perfiles de usuario.", "Preparar una memoria breve con resultados, limitaciones y riesgos del sistema."),
    ("14", "Tema 6", "Tecnologías emergentes, predicción y prescripción.", "Presentación del tema 6; documentación técnica y literatura seleccionada.", "Evaluar madurez, ajuste al problema e impacto de una tendencia tecnológica.", "Análisis comparativo de una tendencia aplicada al deporte.", "Contrastar una fuente técnica primaria y una referencia científica."),
    ("15", "Tema 6", "Ética, privacidad, legalidad, gobernanza y síntesis.", "Presentación del tema 6; guía docente; normativa y documentación institucional.", "Formular recomendaciones responsables y justificar salvaguardas.", "Debate y elaboración de una nota de decisión final.", "Entregar una síntesis con oportunidad, evidencia, riesgos y próximos pasos."),
]

page_break(doc)
add_heading(doc, "4.1 Calendario detallado por sesión", 1)
doc.add_paragraph(
    "La secuencia siguiente concreta, para cada sesión orientativa, los contenidos, los materiales, los objetivos, "
    "la actividad prevista y el trabajo personal. Las fechas exactas se ajustarán al calendario oficial y a las "
    "indicaciones publicadas en Aula Virtual."
)
for idx, (number, topic, contents, materials, objectives, activity, personal) in enumerate(session_plan):
    if idx and idx % 3 == 0:
        page_break(doc)
        add_heading(doc, "4.1 Calendario detallado por sesión", 1)
    add_heading(doc, f"Sesión {number}  {topic}", 2)
    for label, value in (
        ("Contenidos", contents),
        ("Materiales", materials),
        ("Objetivos de aprendizaje", objectives),
        ("Actividad planificada", activity),
        ("Trabajo personal recomendado", personal),
    ):
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(2)
        paragraph.add_run(f"{label}: ").bold = True
        paragraph.add_run(value)

add_heading(doc, "Uso de tutorías", 2)
add_bullets(doc, [
    "Llevar una pregunta concreta, el contexto mínimo y la evidencia del intento realizado.",
    "Diferenciar dudas conceptuales, errores de entorno, problemas de datos y decisiones arquitectónicas.",
    "Registrar la conclusión y convertirla en una prueba, una mejora documental o una decisión de diseño.",
])

add_heading(doc, "Trabajo en equipo", 2)
doc.add_paragraph(
    "En las prácticas y en el proyecto final se recomienda distribuir responsabilidades sin fragmentar el conocimiento: cada integrante debe poder explicar el problema, la arquitectura, los datos, el código, las pruebas, los resultados y las limitaciones."
)

page_break(doc)

# Assessment.
add_heading(doc, "5. Relación con la evaluación", 1)
doc.add_paragraph(
    "La evaluación oficial es continua. La guía docente establece tres componentes revaluables y exige una nota mínima de 5 en cada actividad. El proyecto final evalúa el temario completo y no constituye el contenido del tema 5. Las fechas concretas y cualquier ajuste deberán confirmarse siempre en Aula Virtual y con el equipo docente."
)
eval_rows = [
    ("Prácticas 1 y 2", "40 %", "P1: temas 1–3 · P2: temas 4–6", "Memoria y código", "Semanas 5 y 10"),
    ("Exposición oral", "20 %", "Temario completo", "Presentación y preguntas", "Fecha oficial"),
    ("Proyecto final", "40 %", "Temario completo", "Memoria y código", "Semanas 13–15"),
]
table = doc.add_table(rows=1, cols=5)
table.style = "Table Grid"
for i, text in enumerate(("Actividad", "Peso", "Contenido", "Evidencia", "Referencia temporal")):
    table.rows[0].cells[i].text = text
    set_cell_shading(table.rows[0].cells[i], BLUE)
    for run in table.rows[0].cells[i].paragraphs[0].runs:
        run.bold = True
        run.font.color.rgb = RGBColor.from_string(WHITE)
        run.font.size = Pt(8.5)
for idx, row in enumerate(eval_rows):
    cells = table.add_row().cells
    for i, text in enumerate(row):
        cells[i].text = text
        set_cell_margins(cells[i], 80, 75, 80, 75)
        if idx % 2:
            set_cell_shading(cells[i], LIGHT_GRAY)
        for run in cells[i].paragraphs[0].runs:
            run.font.size = Pt(8.5)

add_heading(doc, "Lista de comprobación de una entrega técnica", 2)
check_items = [
    "El problema, los usuarios y los criterios de éxito están definidos.",
    "La procedencia, el significado y las limitaciones de los datos están documentados.",
    "La arquitectura y las decisiones tecnológicas se justifican frente a alternativas.",
    "El entorno y los pasos de ejecución son reproducibles.",
    "Las pruebas cubren comportamiento, rendimiento y fallos relevantes.",
    "Los resultados se apoyan en evidencias y separan hechos, inferencias y limitaciones.",
    "La memoria y la presentación citan fuentes y atribuyen correctamente contenidos de terceros.",
    "El equipo puede defender oralmente el trabajo y responder sobre código, datos y decisiones.",
]
for item in check_items:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.45)
    p.add_run("☐ ").bold = True
    p.add_run(item)

page_break(doc)

# Repository map and status.
add_heading(doc, "6. Localización y estado de los materiales", 1)
doc.add_paragraph(
    "La carpeta material_original conserva los documentos de trabajo y sus fuentes. La carpeta material_abierto contiene exclusivamente versiones preparadas para publicación o documentación de su estado de revisión."
)
repo_rows = [
    ("Guía docente", "material_original/guias", "Referencia institucional", "Disponible"),
    ("Guía de estudio", "material_abierto/00_guias", "Categoría 0", "Disponible"),
    ("Presentaciones", "material_original/teoria", "Candidatas a categoría 2", "Temas 1–6; auditoría pendiente"),
    ("Fuentes de teoría", "material_original/fuentes/teoria", "Editables", "Temas 1–6; las de T5–T6 son reconstrucciones desde PDF"),
    ("Prácticas", "material_original/practica", "Candidatas a categoría 3", "Temas 2, 4 y 5; proyecto final separado"),
    ("Fuentes de práctica", "material_original/fuentes/practica", "Editables", "Temas 2 y 4; proyecto final"),
    ("Código y notebooks", "material_original/programas", "Candidatos a categoría 6", "Temas 1, 2, 4 y 5; revisión pendiente"),
]
table = doc.add_table(rows=1, cols=4)
table.style = "Table Grid"
for i, text in enumerate(("Material", "Ubicación", "Destino", "Estado")):
    table.rows[0].cells[i].text = text
    set_cell_shading(table.rows[0].cells[i], NAVY)
    for run in table.rows[0].cells[i].paragraphs[0].runs:
        run.bold = True
        run.font.color.rgb = RGBColor.from_string(WHITE)
        run.font.size = Pt(9)
for idx, row in enumerate(repo_rows):
    cells = table.add_row().cells
    for i, text in enumerate(row):
        cells[i].text = text
        set_cell_margins(cells[i], 90, 85, 90, 85)
        if idx % 2:
            set_cell_shading(cells[i], LIGHT_GRAY)
        for run in cells[i].paragraphs[0].runs:
            run.font.size = Pt(8.8)

add_heading(doc, "Qué significa «pendiente de publicación»", 2)
add_bullets(doc, [
    "El contenido puede utilizarse en la docencia, pero aún debe cerrarse su versión canónica.",
    "Deben verificarse autoría, licencia, atribuciones, fuentes de imágenes y materiales de terceros.",
    "Los editables y el software requieren documentación suficiente para reutilización autónoma.",
    "Solo las copias validadas pasarán al paquete definitivo de BURJC Digital.",
])
doc.add_paragraph(
    "Los PDF de los seis temas y el enunciado de la práctica final están incorporados. Las fuentes de los temas 5 y 6 son reconstrucciones fieles desde PDF, están identificadas como tales y han sido validadas mediante compilación y comparación textual con los documentos de trabajo."
)

page_break(doc)

# Sources and license.
add_heading(doc, "7. Referencias y licencia", 1)
add_heading(doc, "Documento de referencia", 2)
doc.add_paragraph(
    "Universidad Rey Juan Carlos (2026). Guía docente de Big Data Processing II, Máster Universitario en Análisis de Datos Deportivos, curso 2026–2027. Fecha de publicación indicada en el documento: 7 de julio de 2026."
)

add_heading(doc, "Bibliografía recogida en la guía docente", 2)
add_bullets(doc, [
    "Gama, J. (2010). Knowledge Discovery from Data Streams.",
    "Marz, N., & Warren, J. (2015). Big Data: Principles and Best Practices of Scalable Real-Time Data Systems.",
    "Hu, S., Ren, S., Chen, Y., Mu, C., Liu, J., Cui, Z., et al. (2025). Hands-on LLM-based Agents: A Tutorial for General Audiences.",
    "Karau, H., Polak, A., & Warren, R. (2026). High Performance Spark: Best Practices for Scaling and Optimizing Apache Spark. O’Reilly Media.",
    "Recursos complementarios: documentación de Apache Kafka y Apache Flink; bases de datos NoSQL; herramientas de procesamiento de texto.",
])

add_heading(doc, "Licencia de esta guía", 2)
doc.add_paragraph(
    "© 2026 Alberto Fernández Isabel, Natalia Madrueño Sierro y Rubén Rodríguez Fernández. Algunos derechos reservados."
)
p = doc.add_paragraph()
p.add_run("Esta guía se distribuye bajo la licencia ")
add_hyperlink(p, "Creative Commons Atribución–CompartirIgual 4.0 Internacional (CC BY-SA 4.0)", "https://creativecommons.org/licenses/by-sa/4.0/deed.es")
p.add_run(".")
doc.add_paragraph(
    "La licencia se aplica exclusivamente al contenido original de esta guía. No se extiende a materiales de terceros citados, enlazados o reproducidos, que conservan su licencia o régimen jurídico propio."
)

add_heading(doc, "Atribución recomendada", 2)
add_callout(
    doc,
    "Forma breve",
    "Fernández Isabel, A.; Madrueño Sierro, N.; y Rodríguez Fernández, R. (2026). Big Data Processing II: Guía de estudio. Universidad Rey Juan Carlos. CC BY-SA 4.0.",
    LIGHT_TEAL,
)

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUT)
OPEN_OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OPEN_OUT)
print(OUT)
print(OPEN_OUT)
