import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generar_analisis_texto(cliente_nombre, campo_nombre, fecha_vuelo, estadisticas):
    prompt = f"""Sos un asistente que ayuda a redactar informes agronómicos claros y directos para productores agropecuarios argentinos.

Datos del relevamiento:
- Cliente: {cliente_nombre}
- Campo: {campo_nombre}
- Fecha del vuelo: {fecha_vuelo}
- Índice calculado: NDVI (Índice de Vegetación de Diferencia Normalizada)
- NDVI mínimo: {estadisticas['ndvi_min']:.3f}
- NDVI máximo: {estadisticas['ndvi_max']:.3f}
- NDVI promedio: {estadisticas['ndvi_promedio']:.3f}

Escribí un análisis breve (máximo 200 palabras) en español rioplatense, dirigido al productor, que explique:
1. Qué significa este resultado en términos simples
2. Si hay señales de alerta o el campo se ve saludable en promedio
3. Una recomendación concreta de qué hacer a continuación

No inventes datos que no te di. Aclará que este es un análisis preliminar basado en NDVI satelital, no una recomendación técnica definitiva sin validación de un ingeniero agrónomo."""

    respuesta = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )
    return respuesta.text