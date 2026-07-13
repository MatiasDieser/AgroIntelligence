from processing.indices import calcular_ndvi, guardar_mapa_ndvi
from db.queries import guardar_resultado
from reporting.generate_report import generar_analisis_texto
from reporting.pdf_builder import generar_pdf

ruta_red = r"C:\Users\matid\OneDrive\Escritorio\Proyecto\data_pruebas\sentinel\b04_2.tiff"
ruta_nir = r"C:\Users\matid\OneDrive\Escritorio\Proyecto\data_pruebas\sentinel\b08_2.tiff"
ruta_mapa = r"C:\Users\matid\OneDrive\Escritorio\Proyecto\data_pruebas\sentinel\ndvi_mapa7.png"
ruta_pdf = r"C:\Users\matid\OneDrive\Escritorio\Proyecto\data_pruebas\sentinel\informe.pdf"

VUELO_ID = "71b298c0-64d1-47a3-9448-80401a9eefdf"
CLIENTE_NOMBRE = "Don Miguel"
CAMPO_NOMBRE = "La Gloria"
FECHA_VUELO = "2026-07-10"

ndvi, perfil = calcular_ndvi(ruta_red, ruta_nir)

estadisticas = {
    "ndvi_min": float(ndvi.min()),
    "ndvi_max": float(ndvi.max()),
    "ndvi_promedio": float(ndvi.mean())
}

guardar_mapa_ndvi(ndvi, ruta_mapa)

guardar_resultado(
    vuelo_id=VUELO_ID,
    indice_tipo="NDVI",
    indice_path=ruta_mapa,
    estadisticas=estadisticas
)

texto_analisis = generar_analisis_texto(
    cliente_nombre=CLIENTE_NOMBRE,
    campo_nombre=CAMPO_NOMBRE,
    fecha_vuelo=FECHA_VUELO,
    estadisticas=estadisticas
)

generar_pdf(
    ruta_salida=ruta_pdf,
    cliente_nombre=CLIENTE_NOMBRE,
    campo_nombre=CAMPO_NOMBRE,
    fecha_vuelo=FECHA_VUELO,
    estadisticas=estadisticas,
    texto_analisis=texto_analisis,
    ruta_mapa_ndvi=ruta_mapa
)

print(f"PDF generado en: {ruta_pdf}")