import os
import json
import time

CARPETA_CLIENTES = r"C:\Users\matid\OneDrive\Escritorio\Proyecto\clientes"
EXTENSIONES_VALIDAS = (".tif", ".tiff", ".jpg", ".jpeg")
HORAS_LIMITE = 6  # a partir de cuántas horas consideramos que una carga está "trabada"


def contar_imagenes(carpeta):
    return [
        f for f in os.listdir(carpeta)
        if f.lower().endswith(EXTENSIONES_VALIDAS)
    ]


def revisar_cargas_incompletas():
    encontrados = 0

    for raiz, _, archivos in os.walk(CARPETA_CLIENTES):
        if "manifest.json" not in archivos:
            continue

        ruta_manifest = os.path.join(raiz, "manifest.json")

        with open(ruta_manifest) as f:
            manifest = json.load(f)

        cantidad_esperada = manifest["cantidad_esperada"]
        cantidad_actual = len(contar_imagenes(raiz))

        if cantidad_actual == cantidad_esperada:
            continue  # esta carga está OK, no hay nada que avisar

        antiguedad_horas = (time.time() - os.path.getmtime(ruta_manifest)) / 3600

        if antiguedad_horas >= HORAS_LIMITE:
            encontrados += 1
            print(f"[ALERTA] Vuelo {manifest['vuelo_id']}")
            print(f"         Carpeta: {raiz}")
            print(f"         Imágenes: {cantidad_actual}/{cantidad_esperada}")
            print(f"         Manifest creado hace {antiguedad_horas:.1f} horas")
            print(f"         → Revisar manualmente: ¿faltó subir algo? "
                  f"¿hay que reintentar o forzar el procesamiento?")
            print()

    if encontrados == 0:
        print("Todo en orden, no hay cargas trabadas.")
    else:
        print(f"Se encontraron {encontrados} carga(s) con problemas.")


if __name__ == "__main__":
    revisar_cargas_incompletas()