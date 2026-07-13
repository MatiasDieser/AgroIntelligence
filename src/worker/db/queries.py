import json
from db.connection import get_connection

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