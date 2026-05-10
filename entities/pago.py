from persistence.db import get_connection
import pymysql


class Pago:
    def __init__(self, id: int, orden_id: int,
                 monto: float, metodo_pago: str):
        self.id = id
        self.orden_id = orden_id
        self.monto = monto
        self.metodo_pago = metodo_pago

    # ── Listar todos (JOIN con ordenes) ───────────────────────
    @staticmethod
    def get_all():
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT p.id, p.monto, p.metodo_pago, p.created_at,
                   o.id AS orden_id, o.total AS orden_total,
                   c.nombre AS cliente
            FROM pagos p
            JOIN ordenes o ON p.orden_id = o.id
            JOIN clientes c ON o.cliente_id = c.id
            ORDER BY p.created_at DESC
        """)

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    # ── Buscar por orden ──────────────────────────────────────
    @staticmethod
    def get_by_orden(orden_id: int):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            "SELECT id, monto, metodo_pago, created_at FROM pagos WHERE orden_id = %s",
            (orden_id,)
        )

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    # ── Insertar ──────────────────────────────────────────────
    def save(self):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            "INSERT INTO pagos (orden_id, monto, metodo_pago) VALUES (%s, %s, %s)",
            (self.orden_id, self.monto, self.metodo_pago)
        )

        connection.commit()
        self.id = cursor.lastrowid
        cursor.close()
        connection.close()

    # ── Eliminar ──────────────────────────────────────────────
    def delete(self):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("DELETE FROM pagos WHERE id = %s", (self.id,))

        connection.commit()
        cursor.close()
        connection.close()
