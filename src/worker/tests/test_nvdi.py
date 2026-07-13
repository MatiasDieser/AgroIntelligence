from processing.indices import calcular_ndvi, guardar_mapa_ndvi
from db.queries import guardar_resultado

ruta_red = r"C:\Users\matid\OneDrive\Escritorio\Proyecto\data_pruebas\sentinel\b04_2.tiff"
ruta_nir = r"C:\Users\matid\OneDrive\Escritorio\Proyecto\data_pruebas\sentinel\b08_2.tiff"
ruta_salida = r"C:\Users\matid\OneDrive\Escritorio\Proyecto\data_pruebas\sentinel\ndvi_mapa_6.png"

VUELO_ID = "71b298c0-64d1-47a3-9448-80401a9eefdf"

ndvi, perfil = calcular_ndvi(ruta_red, ruta_nir)

estadisticas = {
    "ndvi_min": float(ndvi.min()),
    "ndvi_max": float(ndvi.max()),
    "ndvi_promedio": float(ndvi.mean())
}

print(f"NDVI mínimo: {estadisticas['ndvi_min']:.3f}")
print(f"NDVI máximo: {estadisticas['ndvi_max']:.3f}")
print(f"NDVI promedio: {estadisticas['ndvi_promedio']:.3f}")

guardar_mapa_ndvi(ndvi, ruta_salida)
print(f"Mapa guardado en: {ruta_salida}")

resultado_id = guardar_resultado(
    vuelo_id=VUELO_ID,
    indice_tipo="NDVI",
    indice_path=ruta_salida,
    estadisticas=estadisticas
)
print(f"Resultado guardado en la base con id: {resultado_id}")