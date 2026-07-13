import rasterio
import numpy as np
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

def guardar_mapa_ndvi(ndvi, ruta_salida):
    colores = ["#a50026", "#f46d43", "#fee08b", "#d9ef8b", "#66bd63", "#1a9850"]
    cmap = mcolors.LinearSegmentedColormap.from_list("ndvi_cmap", colores)

    vmin = np.percentile(ndvi, 2)
    vmax = np.percentile(ndvi, 98)

    plt.figure(figsize=(10, 10))
    img = plt.imshow(ndvi, cmap=cmap, vmin=vmin, vmax=vmax)
    cbar = plt.colorbar(img, label="NDVI")
    plt.title("Mapa NDVI")
    plt.axis("off")
    plt.savefig(ruta_salida, dpi=150, bbox_inches="tight")
    plt.close()