#!/usr/bin/env python3
"""Construye el libro y los dos paquetes del depósito único en BURJC."""

from __future__ import annotations

import hashlib
import shutil
import tarfile
import zipfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OPEN = ROOT / "material_abierto"
PACKAGE = OPEN / "99_burjc_package"
UPLOAD = ROOT / "BURJC" / "01_SUBIR"
SUPPORT = ROOT / "BURJC" / "02_APOYO"

GUIDE = OPEN / "00_guias" / "Guia_de_estudio_Big_Data_Processing_II_2026-2027.pdf"
NOTES = OPEN / "01_apuntes" / "Apuntes_Big_Data_Processing_II.pdf"
SLIDES = OPEN / "02_presentaciones" / "Presentaciones_Big_Data_Processing_II.pdf"
PRACTICES = OPEN / "03_practicas" / "Practicas_Big_Data_Processing_II.pdf"
BADGE = OPEN / "assets" / "cc_by_sa_4_0.png"

BOOK = PACKAGE / "Big_Data_Processing_II.pdf"
EDITABLES = PACKAGE / "Big_Data_Processing_II_editables.zip"
CODE = PACKAGE / "Big_Data_Processing_II_codigo.tar.gz"

AUTHORS = "Alberto Fernández Isabel · Natalia Madrueño Sierro · Rubén Rodríguez Fernández"
LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/deed.es"


def register_fonts() -> tuple[str, str]:
    regular = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    bold = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("OpenSans", str(regular)))
        pdfmetrics.registerFont(TTFont("OpenSans-Bold", str(bold)))
        return "OpenSans", "OpenSans-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleOpen", parent=base["Title"], fontName=FONT_BOLD, fontSize=25,
            leading=31, textColor=colors.HexColor("#17365D"), alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleOpen", parent=base["Normal"], fontName=FONT_BOLD, fontSize=14,
            leading=19, textColor=colors.HexColor("#1F4E79"), alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "h1": ParagraphStyle(
            "H1Open", parent=base["Heading1"], fontName=FONT_BOLD, fontSize=17,
            leading=22, textColor=colors.HexColor("#17365D"), spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "H2Open", parent=base["Heading2"], fontName=FONT_BOLD, fontSize=12,
            leading=16, textColor=colors.HexColor("#1F4E79"), spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "BodyOpen", parent=base["BodyText"], fontName=FONT, fontSize=9.5,
            leading=14, alignment=TA_LEFT, spaceAfter=8,
        ),
        "small": ParagraphStyle(
            "SmallOpen", parent=base["BodyText"], fontName=FONT, fontSize=8,
            leading=11, alignment=TA_LEFT,
        ),
        "center": ParagraphStyle(
            "CenterOpen", parent=base["BodyText"], fontName=FONT, fontSize=10,
            leading=14, alignment=TA_CENTER,
        ),
    }


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont(FONT, 7)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawCentredString(A4[0] / 2, 1.1 * cm, f"Material docente en abierto URJC · {doc.page}")
    canvas.restoreState()


def make_program_description(path: Path) -> None:
    st = styles()
    story = [
        Paragraph("Categoría 6 · Programas de ordenador", st["title"]),
        Paragraph("Big Data Processing II", st["subtitle"]),
        Paragraph(AUTHORS, st["center"]),
        Spacer(1, 0.4 * cm),
        Paragraph(
            "El paquete de software reúne notebooks, scripts Python, un productor Kafka, un entorno "
            "Docker/Spark, datos simulados y ejemplos de RAG, agentes y Text-to-SQL con Spark y "
            "LangGraph. Se organiza por temas e incluye dependencias e instrucciones para su uso autónomo.",
            st["body"],
        ),
        Paragraph("Licencia y reutilización", st["h1"]),
        Paragraph(
            "El código se distribuye bajo licencia MIT. Los documentos explicativos originales se "
            "distribuyen bajo CC BY-SA 4.0. No se incluyen credenciales; los ficheros <i>.env</i> se "
            "excluyen y solo se conserva <i>.env.example</i> cuando es necesario.",
            st["body"],
        ),
        Paragraph("Inventario funcional", st["h1"]),
        Table(
            [
                ["Bloque", "Recursos principales"],
                ["Tema 1", "Notebooks de streaming y solución"],
                ["Tema 2", "Productor Kafka, datos simulados, Docker y notebook Spark"],
                ["Tema 4", "Ejemplos RAG y sistemas basados en agentes"],
                ["Tema 5", "Agente Text-to-SQL con Spark y LangGraph"],
            ],
            colWidths=[3.2 * cm, 12.8 * cm],
            style=TableStyle([
                ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
                ("FONTNAME", (0, 1), (-1, -1), FONT),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9FBAD0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]),
        ),
        Spacer(1, 0.5 * cm),
        Paragraph("Repositorio y preservación", st["h1"]),
        Paragraph(
            "Repositorio público: https://github.com/Fiutten/BDPII-Open-Subject-2026", st["body"]
        ),
        Paragraph(
            "SWHID: pendiente de obtener y verificar después de archivar la versión pública definitiva. "
            "Este campo debe sustituirse por el identificador exacto antes del depósito.", st["body"]
        ),
        Paragraph("Declaración sobre apoyo generativo", st["h1"]),
        Paragraph(
            "Las herramientas generativas se emplearon únicamente como apoyo editorial y técnico para "
            "organización, documentación y comprobación de coherencia. El equipo autor revisó y validó "
            "la versión final y asume plena responsabilidad sobre ella.", st["body"]
        ),
    ]
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=2.2*cm, leftMargin=2.2*cm,
                            topMargin=2.1*cm, bottomMargin=2*cm)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def make_frontmatter(path: Path, starts: dict[str, int]) -> None:
    st = styles()
    story = [
        Spacer(1, 1.6 * cm),
        Paragraph("MATERIAL DOCENTE EN ABIERTO", st["subtitle"]),
        Paragraph("Big Data Processing II", st["title"]),
        Paragraph("Máster Universitario en Análisis de Datos Deportivos", st["subtitle"]),
        Paragraph("Curso 2026-2027", st["center"]),
        Spacer(1, 1.0 * cm),
        Paragraph(AUTHORS, st["center"]),
        Spacer(1, 1.0 * cm),
        Image(str(BADGE), width=8.3 * cm, height=2.4 * cm),
        Spacer(1, 0.6 * cm),
        Paragraph("Universidad Rey Juan Carlos · BURJC Digital", st["center"]),
        PageBreak(),
        Paragraph("Información de publicación", st["h1"]),
        Paragraph(
            "© 2026 Alberto Fernández Isabel, Natalia Madrueño Sierro y Rubén Rodríguez Fernández. "
            f"Algunos derechos reservados. El contenido documental original se distribuye bajo "
            f"<link href='{LICENSE_URL}'>CC BY-SA 4.0</link>; el código se distribuye bajo MIT.", st["body"]
        ),
        Paragraph(
            "Los logotipos, marcas, citas y materiales de terceros conservan su régimen jurídico propio "
            "y quedan excluidos de la licencia, salvo indicación expresa. Las imágenes sin licencia de "
            "reutilización verificada se han retirado y sustituido por esquemas originales.", st["body"]
        ),
        Paragraph("Declaración sobre herramientas de inteligencia artificial generativa", st["h1"]),
        Paragraph(
            "En la guía y la documentación editorial se utilizaron herramientas generativas de texto "
            "como apoyo parcial para organizar información aportada por el equipo docente, proponer "
            "redacciones iniciales de textos de enlace, normalizar el repositorio y comprobar coherencia. "
            "No sustituyeron el diseño docente, la selección de contenidos técnicos ni la autoría de "
            "presentaciones y ejercicios. No se conservan imágenes generadas por IA en esta edición.", st["body"]
        ),
        Paragraph(
            "Todo el contenido fue contrastado con la guía docente y los materiales fuente, revisado, "
            "corregido, validado y aprobado por el equipo autor, que asume plena responsabilidad sobre "
            "la exactitud, originalidad, integridad académica, licencias y versión final.", st["body"]
        ),
        PageBreak(),
        Paragraph("Índice general", st["h1"]),
        Table(
            [
                ["Sección", "Contenido", "Página"],
                ["Categoría 0", "Guía de estudio", str(starts["guide"])],
                ["Categoría 1", "Apuntes de la asignatura", str(starts["notes"])],
                ["Categoría 2", "Presentaciones de los temas 1 a 6", str(starts["slides"])],
                ["Categoría 3", "Prácticas, ejercicios y proyecto final", str(starts["practices"])],
                ["Categoría 6", "Descripción de programas de ordenador", str(starts["programs"])],
            ],
            colWidths=[3.2*cm, 10.8*cm, 2*cm],
            style=TableStyle([
                ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
                ("FONTNAME", (0, 1), (-1, -1), FONT),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9FBAD0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (-1, 1), (-1, -1), "RIGHT"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]),
        ),
        Spacer(1, 0.7 * cm),
        Paragraph(
            "Los editables y el código se facilitan como ficheros separados del mismo depósito. La "
            "descripción de la categoría 6 debe completarse con el SWHID verificado antes del envío.",
            st["body"],
        ),
    ]
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=2.2*cm, leftMargin=2.2*cm,
                            topMargin=2.1*cm, bottomMargin=2*cm)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def page_count(path: Path) -> int:
    return len(PdfReader(str(path)).pages)


def merge_book(front: Path, programs: Path) -> None:
    writer = PdfWriter()
    sections = [
        (front, None),
        (GUIDE, "Categoría 0 · Guía de estudio"),
        (NOTES, "Categoría 1 · Apuntes"),
        (SLIDES, "Categoría 2 · Presentaciones"),
        (PRACTICES, "Categoría 3 · Prácticas, ejercicios y problemas"),
        (programs, "Categoría 6 · Programas de ordenador"),
    ]
    for path, bookmark in sections:
        writer.append(PdfReader(str(path)), outline_item=bookmark)
    writer.add_metadata({
        "/Title": "Materiales de la asignatura Big Data Processing II",
        "/Author": "Alberto Fernández Isabel; Natalia Madrueño Sierro; Rubén Rodríguez Fernández",
        "/Subject": "Material docente en abierto de la Universidad Rey Juan Carlos",
        "/Keywords": "Big Data, Kafka, Spark, streaming, analítica deportiva, IA generativa",
    })
    with BOOK.open("wb") as stream:
        writer.write(stream)


def wanted_editable(path: Path) -> bool:
    excluded = {".aux", ".log", ".out", ".nav", ".snm", ".toc", ".fls", ".fdb_latexmk", ".pdf"}
    return path.is_file() and path.suffix.lower() not in excluded and "_minted-" not in path.as_posix()


def build_editables_zip() -> None:
    roots = [
        OPEN / "00_guias" / "editables",
        OPEN / "01_apuntes" / "editables",
        OPEN / "02_presentaciones" / "editables",
        OPEN / "03_practicas" / "editables",
    ]
    support_files = [
        OPEN / "README.md",
        OPEN / "LICENCIAS_Y_MATERIALES_TERCEROS.md",
        OPEN / "INVENTARIO_IMAGENES_Y_ATRIBUCIONES.md",
        OPEN / "02_presentaciones" / "MATRIZ_DERECHOS_IMAGENES.csv",
        OPEN / "02_presentaciones" / "FUENTES_Y_ATRIBUCIONES.txt",
        PACKAGE / "DECLARACION_USO_IA_GENERATIVA.md",
        PACKAGE / "METODOLOGIA_USO_IA_GENERATIVA.md",
    ]
    with zipfile.ZipFile(EDITABLES, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for root in roots:
            for path in sorted(root.rglob("*")):
                if wanted_editable(path):
                    archive.write(path, path.relative_to(OPEN).as_posix())
        for path in support_files:
            archive.write(path, path.relative_to(OPEN).as_posix())


def build_code_tar() -> None:
    with tarfile.open(CODE, "w:gz", compresslevel=9) as archive:
        for name in ("README.md", "LICENSE", "codigo"):
            source = OPEN / "06_programas" / name
            archive.add(source, arcname=f"Big_Data_Processing_II_codigo/{name}", recursive=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_support() -> None:
    SUPPORT.mkdir(parents=True, exist_ok=True)
    for name in (
        "METADATOS_BURJC.md",
        "CUMPLIMIENTO_RUBRICA.md",
        "DECLARACION_USO_IA_GENERATIVA.md",
        "METODOLOGIA_USO_IA_GENERATIVA.md",
        "CHECKLIST_CONVOCATORIA.md",
    ):
        shutil.copy2(PACKAGE / name, SUPPORT / name)
    shutil.copy2(OPEN / "LICENCIAS_Y_MATERIALES_TERCEROS.md", SUPPORT / "LICENCIAS_Y_MATERIALES_TERCEROS.md")
    shutil.copy2(OPEN / "INVENTARIO_IMAGENES_Y_ATRIBUCIONES.md", SUPPORT / "INVENTARIO_IMAGENES_Y_ATRIBUCIONES.md")
    shutil.copy2(OPEN / "02_presentaciones" / "MATRIZ_DERECHOS_IMAGENES.csv", SUPPORT / "MATRIZ_DERECHOS_IMAGENES.csv")


def main() -> None:
    PACKAGE.mkdir(parents=True, exist_ok=True)
    UPLOAD.mkdir(parents=True, exist_ok=True)
    SUPPORT.mkdir(parents=True, exist_ok=True)
    for required in (GUIDE, NOTES, SLIDES, PRACTICES, BADGE):
        if not required.exists():
            raise FileNotFoundError(required)

    programs = PACKAGE / "Descripcion_categoria_6_programas.pdf"
    front = PACKAGE / "Portada_indice_y_declaraciones.pdf"
    make_program_description(programs)

    front_pages = 3
    starts = {
        "guide": front_pages + 1,
        "notes": front_pages + page_count(GUIDE) + 1,
        "slides": front_pages + page_count(GUIDE) + page_count(NOTES) + 1,
        "practices": front_pages + page_count(GUIDE) + page_count(NOTES) + page_count(SLIDES) + 1,
        "programs": front_pages + page_count(GUIDE) + page_count(NOTES) + page_count(SLIDES) + page_count(PRACTICES) + 1,
    }
    make_frontmatter(front, starts)
    if page_count(front) != front_pages:
        raise RuntimeError(f"La portada tiene {page_count(front)} páginas; se esperaban {front_pages}")
    merge_book(front, programs)
    build_editables_zip()
    build_code_tar()
    copy_support()

    products = (BOOK, EDITABLES, CODE)
    for product in products:
        shutil.copy2(product, UPLOAD / product.name)
    manifest = "\n".join(f"{sha256(UPLOAD / p.name)}  {p.name}" for p in products) + "\n"
    (SUPPORT / "SHA256SUMS.txt").write_text(manifest, encoding="utf-8")

    print(f"Libro: {BOOK} ({page_count(BOOK)} páginas)")
    print(f"Editables: {EDITABLES}")
    print(f"Código: {CODE}")


if __name__ == "__main__":
    main()
