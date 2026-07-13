from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generar_pdf(ruta_salida, cliente_nombre, campo_nombre, fecha_vuelo,
                 estadisticas, texto_analisis, ruta_mapa_ndvi):

    doc = SimpleDocTemplate(ruta_salida, pagesize=A4,
                             topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        "TituloCustom", parent=styles["Title"], fontSize=18, spaceAfter=6
    )
    subtitulo_style = ParagraphStyle(
        "SubtituloCustom", parent=styles["Normal"], fontSize=11,
        textColor=colors.grey, spaceAfter=20
    )
    seccion_style = ParagraphStyle(
        "SeccionCustom", parent=styles["Heading2"], spaceBefore=16, spaceAfter=8
    )
    cuerpo_style = ParagraphStyle(
        "CuerpoCustom", parent=styles["Normal"], fontSize=11, leading=16
    )

    elementos = []

    elementos.append(Paragraph("Informe de Relevamiento Agronómico", titulo_style))
    elementos.append(Paragraph(
        f"Cliente: {cliente_nombre} &nbsp;|&nbsp; Campo: {campo_nombre} &nbsp;|&nbsp; Fecha: {fecha_vuelo}",
        subtitulo_style
    ))

    elementos.append(Paragraph("Mapa de Índice de Vegetación (NDVI)", seccion_style))
    elementos.append(Image(ruta_mapa_ndvi, width=14*cm, height=14*cm))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("Estadísticas del relevamiento", seccion_style))
    elementos.append(Paragraph(
        f"NDVI mínimo: {estadisticas['ndvi_min']:.3f} &nbsp;|&nbsp; "
        f"NDVI máximo: {estadisticas['ndvi_max']:.3f} &nbsp;|&nbsp; "
        f"NDVI promedio: {estadisticas['ndvi_promedio']:.3f}",
        cuerpo_style
    ))

    elementos.append(Paragraph("Análisis", seccion_style))
    for parrafo in texto_analisis.split("\n"):
        if parrafo.strip():
            elementos.append(Paragraph(parrafo, cuerpo_style))
            elementos.append(Spacer(1, 6))

    doc.build(elementos)