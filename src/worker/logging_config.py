import os
import re
import logging
from datetime import date

# src/worker/logging_config.py -> subir 2 niveles llega a la raíz del proyecto
RAIZ_PROYECTO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RUTA_LOGS_WORKER = os.path.join(RAIZ_PROYECTO, "logs", "worker")


def _sanitizar(nombre):
    nombre = (nombre or "").strip()
    if not nombre:
        return "sin_cliente"
    return re.sub(r"[^\w\-]+", "_", nombre)


def obtener_logger(cliente_nombre):
    """
    Devuelve un logger que escribe en logs/worker/<cliente>/<fecha>.log
    y también imprime en consola (mismo formato de siempre, sin timestamp,
    para no ensuciar lo que ya se ve bien en la terminal).
    """
    cliente_seguro = _sanitizar(cliente_nombre)
    fecha_hoy = date.today().isoformat()

    carpeta = os.path.join(RUTA_LOGS_WORKER, cliente_seguro)
    os.makedirs(carpeta, exist_ok=True)
    ruta_archivo = os.path.join(carpeta, f"{fecha_hoy}.log")

    logger = logging.getLogger(f"worker.{cliente_seguro}")
    logger.setLevel(logging.INFO)

    # Evitar duplicar handlers si se pide el mismo logger varias veces
    # (por ejemplo, dos vuelos del mismo cliente el mismo día).
    ya_tiene_handler_de_archivo = any(
        isinstance(h, logging.FileHandler) and h.baseFilename == os.path.abspath(ruta_archivo)
        for h in logger.handlers
    )

    if not ya_tiene_handler_de_archivo:
        formato_archivo = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler_archivo = logging.FileHandler(ruta_archivo, encoding="utf-8")
        handler_archivo.setFormatter(formato_archivo)
        logger.addHandler(handler_archivo)

    if not any(isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler) for h in logger.handlers):
        handler_consola = logging.StreamHandler()
        handler_consola.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler_consola)

    logger.propagate = False
    return logger
