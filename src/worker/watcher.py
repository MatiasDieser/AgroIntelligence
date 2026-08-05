import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from processing.indices import calcular_ndvi, guardar_mapa_ndvi, calcular_ndmi, guardar_mapa_ndmi
from db.queries import (
    guardar_resultado,
    guardar_informe,
    crear_trabajo,
    actualizar_etapa_trabajo,
    marcar_trabajo_completado,
    marcar_trabajo_error,
    obtener_resultado_anterior,
)
from reporting.generate_report import generar_analisis_texto
from reporting.pdf_builder import generar_pdf
from logging_config import obtener_logger

CARPETA_A_VIGILAR = r"C:\Users\matid\OneDrive\Escritorio\Proyecto\clientes"
EXTENSIONES_VALIDAS = (".tif", ".tiff", ".jpg", ".jpeg")


def contar_imagenes(carpeta_vuelo):
    return [
        f for f in os.listdir(carpeta_vuelo)
        if f.lower().endswith(EXTENSIONES_VALIDAS)
    ]


def procesar_vuelo(carpeta_vuelo, manifest):
    vuelo_id = manifest["vuelo_id"]
    logger = obtener_logger(manifest.get("cliente_nombre", "Cliente"))
    logger.info(f"[OK] Procesando vuelo {vuelo_id}...")

    try:
        trabajo_id = crear_trabajo(vuelo_id, etapa_actual="iniciando")
    except Exception as e:
        # Si ya hay un trabajo activo (pendiente/procesando) para este vuelo,
        # el índice único de la tabla lo va a rechazar. No abortamos el
        # procesamiento por esto, solo seguimos sin registro en trabajos.
        logger.warning(f"  [!] No se pudo crear registro en trabajos ({e.__class__.__name__}: {e}). Sigo sin trazabilidad.")
        trabajo_id = None

    try:
        ruta_red = os.path.join(carpeta_vuelo, "b04_2.tiff")
        ruta_nir = os.path.join(carpeta_vuelo, "b08_2.tiff")
        ruta_swir = os.path.join(carpeta_vuelo, "b11_2.tiff")
        ruta_mapa = os.path.join(carpeta_vuelo, "ndvi_mapa.png")
        ruta_mapa_ndmi = os.path.join(carpeta_vuelo, "ndmi_mapa.png")
        ruta_pdf = os.path.join(carpeta_vuelo, "informe.pdf")

        if trabajo_id:
            actualizar_etapa_trabajo(trabajo_id, "calculando_ndvi")
        ndvi, _ = calcular_ndvi(ruta_red, ruta_nir)

        estadisticas = {
            "ndvi_min": float(ndvi.min()),
            "ndvi_max": float(ndvi.max()),
            "ndvi_promedio": float(ndvi.mean())
        }

        guardar_mapa_ndvi(ndvi, ruta_mapa)

        guardar_resultado(
            vuelo_id=vuelo_id,
            indice_tipo="NDVI",
            indice_path=ruta_mapa,
            estadisticas=estadisticas
        )

        # NDMI (estrés hídrico) es opcional: solo se calcula si la banda SWIR
        # (B11) está disponible en la carpeta del vuelo. Con datos de prueba
        # viejos que solo tienen B04/B08 esto se salta sin romper nada.
        ruta_mapa_ndmi_final = None
        if os.path.exists(ruta_swir):
            if trabajo_id:
                actualizar_etapa_trabajo(trabajo_id, "calculando_ndmi")
            ndmi, _ = calcular_ndmi(ruta_nir, ruta_swir)

            estadisticas["ndmi_min"] = float(ndmi.min())
            estadisticas["ndmi_max"] = float(ndmi.max())
            estadisticas["ndmi_promedio"] = float(ndmi.mean())

            guardar_mapa_ndmi(ndmi, ruta_mapa_ndmi)

            guardar_resultado(
                vuelo_id=vuelo_id,
                indice_tipo="NDMI",
                indice_path=ruta_mapa_ndmi,
                estadisticas={
                    "ndmi_min": estadisticas["ndmi_min"],
                    "ndmi_max": estadisticas["ndmi_max"],
                    "ndmi_promedio": estadisticas["ndmi_promedio"],
                }
            )
            ruta_mapa_ndmi_final = ruta_mapa_ndmi

        if trabajo_id:
            actualizar_etapa_trabajo(trabajo_id, "generando_analisis_texto")

        try:
            estadisticas_anteriores = obtener_resultado_anterior(vuelo_id)
        except Exception as e:
            logger.warning(f"  [!] No se pudo buscar vuelo anterior ({e.__class__.__name__}: {e}). Sigo sin comparación.")
            estadisticas_anteriores = None

        texto_analisis = generar_analisis_texto(
            cliente_nombre=manifest.get("cliente_nombre", "Cliente"),
            campo_nombre=manifest.get("campo_nombre", "Campo"),
            fecha_vuelo=manifest.get("fecha_vuelo", "sin fecha"),
            estadisticas=estadisticas,
            estadisticas_anteriores=estadisticas_anteriores
        )

        if trabajo_id:
            actualizar_etapa_trabajo(trabajo_id, "generando_pdf")
        generar_pdf(
            ruta_salida=ruta_pdf,
            cliente_nombre=manifest.get("cliente_nombre", "Cliente"),
            campo_nombre=manifest.get("campo_nombre", "Campo"),
            fecha_vuelo=manifest.get("fecha_vuelo", "sin fecha"),
            estadisticas=estadisticas,
            texto_analisis=texto_analisis,
            ruta_mapa_ndvi=ruta_mapa,
            ruta_mapa_ndmi=ruta_mapa_ndmi_final
        )

        if trabajo_id:
            actualizar_etapa_trabajo(trabajo_id, "guardando_informe")
        informe_id, link_unico = guardar_informe(
            vuelo_id=vuelo_id,
            pdf_path=ruta_pdf
        )

        logger.info(f"  [OK] Informe generado: {ruta_pdf}")
        logger.info(f"  [OK] Link único: {link_unico}")

        if trabajo_id:
            marcar_trabajo_completado(trabajo_id)

    except Exception as e:
        logger.error(f"  [X] ERROR procesando vuelo {vuelo_id}: {e.__class__.__name__}: {e}")
        if trabajo_id:
            marcar_trabajo_error(trabajo_id, f"{e.__class__.__name__}: {e}")
        raise


class CargaCompletaHandler(FileSystemEventHandler):
    def __init__(self):
        self.vuelos_ya_disparados = set()
        self.imagenes_ya_logueadas = set()

    def on_any_event(self, event):
        if event.is_directory:
            return

        if event.src_path.lower().endswith(EXTENSIONES_VALIDAS):
            if event.src_path not in self.imagenes_ya_logueadas:
                print(f"  ↳ Imagen detectada: {os.path.basename(event.src_path)}")
                self.imagenes_ya_logueadas.add(event.src_path)

        carpeta_vuelo = os.path.dirname(event.src_path)
        ruta_manifest = os.path.join(carpeta_vuelo, "manifest.json")

        if not os.path.exists(ruta_manifest):
            return

        try:
            with open(ruta_manifest) as f:
                manifest = json.load(f)
        except Exception as e:
            print(f" No se pudo leer manifest.json en {carpeta_vuelo}: {e}")
            return

        vuelo_id = manifest.get("vuelo_id")
        if not vuelo_id or vuelo_id in self.vuelos_ya_disparados:
            return

        cantidad_esperada = manifest.get("cantidad_esperada")
        imagenes_actuales = contar_imagenes(carpeta_vuelo)

        if len(imagenes_actuales) == cantidad_esperada:
            logger = obtener_logger(manifest.get("cliente_nombre", "Cliente"))
            logger.info(f"[OK] Carga completa para vuelo {vuelo_id}: "
                        f"{len(imagenes_actuales)}/{cantidad_esperada} imágenes")
            self.vuelos_ya_disparados.add(vuelo_id)

            try:
                procesar_vuelo(carpeta_vuelo, manifest)
            except Exception:
                # El error ya quedó registrado (consola + logs/worker/<cliente>/<fecha>.log)
                # dentro de procesar_vuelo. Acá solo confirmamos que el watcher sigue vivo.
                print(" El watcher sigue funcionando. Revisar manualmente esta carga.")


if __name__ == "__main__":
    handler = CargaCompletaHandler()
    observer = Observer()
    observer.schedule(handler, CARPETA_A_VIGILAR, recursive=True)
    observer.start()

    print(f"Vigilando cargas en: {CARPETA_A_VIGILAR}")
    print("Presioná Ctrl+C para detener.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()