import json
from db.connection import get_connection
import secrets


def crear_trabajo(vuelo_id, etapa_actual="iniciando"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO trabajos (vuelo_id, estado, etapa_actual, fecha_inicio)
        VALUES (%s, 'procesando', %s, NOW())
        RETURNING id;
        """,
        (vuelo_id, etapa_actual)
    )
    trabajo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return trabajo_id


def actualizar_etapa_trabajo(trabajo_id, etapa_actual):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE trabajos SET etapa_actual = %s WHERE id = %s;",
        (etapa_actual, trabajo_id)
    )
    conn.commit()
    cur.close()
    conn.close()


def marcar_trabajo_completado(trabajo_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE trabajos
        SET estado = 'completado', fecha_fin = NOW()
        WHERE id = %s;
        """,
        (trabajo_id,)
    )
    conn.commit()
    cur.close()
    conn.close()


def marcar_trabajo_error(trabajo_id, error_detalle):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE trabajos
        SET estado = 'error', error = %s, fecha_fin = NOW()
        WHERE id = %s;
        """,
        (str(error_detalle)[:2000], trabajo_id)
    )
    conn.commit()
    cur.close()
    conn.close()


def obtener_resultado_anterior(vuelo_id):
    """
    Busca el vuelo NDVI más reciente anterior al vuelo dado, para el mismo
    campo. Devuelve un dict con fecha y estadísticas, o None si no hay
    vuelo previo (caso normal hoy, con un solo vuelo cargado).
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT campo_id, fecha FROM vuelos WHERE id = %s;", (vuelo_id,))
    row = cur.fetchone()
    if not row or row[0] is None:
        cur.close()
        conn.close()
        return None
    campo_id, fecha_actual = row

    cur.execute(
        """
        SELECT id, fecha FROM vuelos
        WHERE campo_id = %s AND id != %s AND fecha < %s
        ORDER BY fecha DESC
        LIMIT 1;
        """,
        (campo_id, vuelo_id, fecha_actual)
    )
    row_anterior = cur.fetchone()
    if not row_anterior:
        cur.close()
        conn.close()
        return None
    vuelo_anterior_id, fecha_anterior = row_anterior

    cur.execute(
        """
        SELECT estadisticas FROM resultados
        WHERE vuelo_id = %s AND indice_tipo = 'NDVI'
        ORDER BY fecha_generacion DESC
        LIMIT 1;
        """,
        (vuelo_anterior_id,)
    )
    row_resultado = cur.fetchone()
    cur.close()
    conn.close()

    if not row_resultado:
        return None

    estadisticas_anteriores = row_resultado[0]
    estadisticas_anteriores["fecha_vuelo"] = str(fecha_anterior)
    return estadisticas_anteriores


def guardar_resultado(vuelo_id, indice_tipo, indice_path, estadisticas, ortomosaico_path=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO resultados (vuelo_id, ortomosaico_path, indice_tipo, indice_path, estadisticas)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (vuelo_id, ortomosaico_path, indice_tipo, indice_path, json.dumps(estadisticas))
    )
    resultado_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return resultado_id


def generar_link_unico():
    return secrets.token_urlsafe(16)  


def guardar_informe(vuelo_id, pdf_path):
    link_unico = generar_link_unico()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO informes (vuelo_id, pdf_path, link_unico, estado)
        VALUES (%s, %s, %s, 'borrador')
        RETURNING id, link_unico;
        """,
        (vuelo_id, pdf_path, link_unico)
    )
    informe_id, link = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return informe_id, link