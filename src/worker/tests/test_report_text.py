from reporting.generate_report import generar_analisis_texto

estadisticas = {
    "ndvi_min": -0.055,
    "ndvi_max": 0.921,
    "ndvi_promedio": 0.551
}

texto = generar_analisis_texto(
    cliente_nombre="Don Miguel",
    campo_nombre="La Gloria",
    fecha_vuelo="2026-07-10",
    estadisticas=estadisticas
)

print(texto)