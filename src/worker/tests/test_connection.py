from db.connection import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM clientes;")
resultado = cursor.fetchone()
print(f"Conexión exitosa. Cantidad de clientes: {resultado[0]}")
cursor.close()
conn.close()