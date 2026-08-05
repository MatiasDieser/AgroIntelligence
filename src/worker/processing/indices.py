import rasterio
import numpy as np
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def calcular_ndvi(ruta_banda_roja, ruta_banda_nir):
    with rasterio.open(ruta_banda_roja) as src_red:
        red = src_red.read(1).astype(float)
        perfil = src_red.profile

    with rasterio.open(ruta_banda_nir) as src_nir:
        nir = src_nir.read(1).astype(float)

    denominador = nir + red
    denominador[denominador == 0] = 0.0001

    ndvi = (nir - red) / denominador

    return ndvi, perfil

def calcular_ndmi(ruta_banda_nir, ruta_banda_swir):
    """
    NDMI (Normalized Difference Moisture Index) = (NIR - SWIR) / (NIR + SWIR)
    Detecta estrés hídrico. En Sentinel-2, NIR es B08 (10m) y SWIR es B11 (20m)
    -- NO tienen la misma resolución. Si vienen con distinta forma, remuestreamos
    el SWIR a la grilla del NIR (bilinear) antes de operar; si no, numpy tira
    error de shape mismatch o, peor, hace broadcasting silencioso mal alineado.
    """
    with rasterio.open(ruta_banda_nir) as src_nir:
        nir = src_nir.read(1).astype(float)
        perfil = src_nir.profile
        forma_nir = nir.shape

    with rasterio.open(ruta_banda_swir) as src_swir:
        if src_swir.shape != forma_nir:
            from rasterio.enums import Resampling
            swir = src_swir.read(
                1,
                out_shape=forma_nir,
                resampling=Resampling.bilinear
            ).astype(float)
        else:
            swir = src_swir.read(1).astype(float)

    denominador = nir + swir
    denominador[denominador == 0] = 0.0001

    ndmi = (nir - swir) / denominador

    return ndmi, perfil


def guardar_mapa_indice(matriz, ruta_salida, titulo, etiqueta, colores, vmin=None, vmax=None):
    cmap = mcolors.LinearSegmentedColormap.from_list("indice_cmap", colores)

    # Si no se pasa un rango fijo, se usa el percentil 2/98 de la propia imagen
    # (bueno para resaltar contraste relativo dentro de un solo vuelo, pero
    # engañoso para comparar humedad/vigor entre vuelos distintos, porque el
    # rango se recalcula cada vez).
    if vmin is None:
        vmin = np.percentile(matriz, 2)
    if vmax is None:
        vmax = np.percentile(matriz, 98)

    plt.figure(figsize=(10, 10))
    img = plt.imshow(matriz, cmap=cmap, vmin=vmin, vmax=vmax)
    cbar = plt.colorbar(img, label=etiqueta)
    plt.title(titulo)
    plt.axis("off")
    plt.savefig(ruta_salida, dpi=150, bbox_inches="tight")
    plt.close()


def guardar_mapa_ndvi(ndvi, ruta_salida):
    colores = ["#a50026", "#f46d43", "#fee08b", "#d9ef8b", "#66bd63", "#1a9850"]
    guardar_mapa_indice(ndvi, ruta_salida, "Mapa NDVI", "NDVI", colores)


def guardar_mapa_ndmi(ndmi, ruta_salida):
    # Marrón (seco) -> Azul (húmedo), escala más intuitiva para estrés hídrico.
    # Rango FIJO (no percentiles): -0.4 a 0.4, alineado a referencias agronómicas
    # estándar de NDMI (< 0 muy seco/suelo desnudo, 0 a 0.2 estrés bajo-moderado,
    # 0.2 a 0.4 humedad moderada, > 0.4 alta humedad). Así el color de un vuelo
    # es comparable contra el de otro vuelo distinto, no solo contra sí mismo.
    colores = ["#8c510a", "#d8b365", "#f6e8c3", "#c7eae5", "#5ab4ac", "#01665e"]
    guardar_mapa_indice(ndmi, ruta_salida, "Mapa NDMI (estrés hídrico)", "NDMI", colores,
                        vmin=-0.4, vmax=0.4)