import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

TEMPERATURE = 0.25  # bajo para reducir variabilidad/invención entre corridas


def generar_analisis_texto(cliente_nombre, campo_nombre, fecha_vuelo, estadisticas,
                            estadisticas_anteriores=None, intentos=3):

    seccion_comparacion_datos = ""
    seccion_comparacion_pedido = ""
    if estadisticas_anteriores:
        diferencia = estadisticas["ndvi_promedio"] - estadisticas_anteriores["ndvi_promedio"]
        seccion_comparacion_datos = f"""
Vuelo anterior del mismo campo ({estadisticas_anteriores.get('fecha_vuelo', 'sin fecha')}):
- NDVI promedio anterior: {estadisticas_anteriores['ndvi_promedio']:.3f}
- Diferencia respecto al vuelo actual: {diferencia:+.3f}
"""
        seccion_comparacion_pedido = """
Comparación con vuelo anterior:
[cómo cambió el NDVI respecto al vuelo anterior, y qué podría explicar la diferencia]
"""

    tiene_ndmi = "ndmi_promedio" in estadisticas
    seccion_ndmi_datos = ""
    if tiene_ndmi:
        seccion_ndmi_datos = f"""
- Índice calculado: NDMI (Índice de Humedad de Diferencia Normalizada, mide estrés hídrico)
- NDMI mínimo: {estadisticas['ndmi_min']:.3f}
- NDMI máximo: {estadisticas['ndmi_max']:.3f}
- NDMI promedio: {estadisticas['ndmi_promedio']:.3f}
Referencia para interpretar NDMI: por debajo de 0 indica suelo muy seco o sin cobertura vegetal, 0 a 0.2 estrés hídrico bajo a moderado, 0.2 a 0.4 humedad moderada, por encima de 0.4 alta humedad."""

    instruccion_ndmi = (
        "Tenés datos de NDMI además de NDVI: el Diagnóstico y las Zonas de atención "
        "tienen que cubrir tanto vigor vegetativo (NDVI) como estrés hídrico (NDMI) por separado, "
        "sin mezclar los dos índices en una sola idea confusa."
        if tiene_ndmi else
        "Solo tenés datos de NDVI (vigor vegetativo). No tenés información de humedad/estrés hídrico "
        "para este vuelo, así que no menciones ni infieras nada sobre riego o humedad."
    )

    prompt = f"""Sos un asistente que ayuda a redactar informes agronómicos claros y directos para productores agropecuarios argentinos.

Datos del relevamiento:
- Cliente: {cliente_nombre}
- Campo: {campo_nombre}
- Fecha del vuelo: {fecha_vuelo}
- Índice calculado: NDVI (Índice de Vegetación de Diferencia Normalizada)
- NDVI mínimo: {estadisticas['ndvi_min']:.3f}
- NDVI máximo: {estadisticas['ndvi_max']:.3f}
- NDVI promedio: {estadisticas['ndvi_promedio']:.3f}
{seccion_ndmi_datos}
{seccion_comparacion_datos}
{instruccion_ndmi}

Escribí el análisis en español rioplatense, dirigido al productor, siguiendo EXACTAMENTE esta estructura (repetí estos encabezados tal cual, cada uno en su propia línea, sin agregar otros):

Diagnóstico:
[2-3 oraciones sobre qué significa el resultado en términos simples, y si el campo se ve saludable o hay señales de alerta]

Zonas de atención:
[qué rangos de valores o áreas requieren revisión; si no hay nada preocupante, decilo explícitamente en vez de inventar un problema]

Acción sugerida:
[una recomendación concreta y accionable]
{seccion_comparacion_pedido}
No inventes datos que no te di. Cerrá siempre aclarando que este es un análisis preliminar basado en índices satelitales, no una recomendación técnica definitiva sin validación de un ingeniero agrónomo. Máximo 250 palabras en total."""

    for intento in range(1, intentos + 1):
        try:
            respuesta = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt,
                config=types.GenerateContentConfig(temperature=TEMPERATURE)
            )
            return respuesta.text
        except Exception as e:
            print(f"[X] Intento {intento}/{intentos} fallo ({e.__class__.__name__}: {e}). Reintentando...")
            if intento < intentos:
                time.sleep(5 * intento)
            else:
                raise
