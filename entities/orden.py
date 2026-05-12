from persistence.db import get_connection
import pymysql


class Orden:
    def __init__(self, id: int, cliente_id: int, usuario_id: int,
                 total: float, is_active: bool = True):
        self.id = id
        self.cliente_id = cliente_id
        self.usuario_id = usuario_id
        self.total = total
        self.is_active = is_active

    # ── Listar todas (JOIN clientes y usuarios) ───────────────
    @staticmethod
    def get_all():
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT o.id, o.total, o.is_active, o.created_at,
                   c.nombre AS cliente,
                   u.nombre AS vendedor
            FROM ordenes o
            JOIN clientes c ON o.cliente_id = c.id
            JOIN usuarios u ON o.usuario_id = u.id
            ORDER BY o.created_at DESC
        """)

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    # ── Buscar por ID con detalle ─────────────────────────────
    @staticmethod
    def get_by_id(id: int):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT o.id, o.total, o.is_active, o.created_at,
                   c.nombre AS cliente,
                   u.nombre AS vendedor
            FROM ordenes o
            JOIN clientes c ON o.cliente_id = c.id
            JOIN usuarios u ON o.usuario_id = u.id
            WHERE o.id = %s
        """, (id,))

        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return row

    # ── Detalle de productos de una orden (JOIN) ──────────────
    @staticmethod
    def get_detalle(orden_id: int):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT p.nombre, op.cantidad, op.precio,
                   op.cantidad * op.precio AS subtotal
            FROM orden_productos op
            JOIN productos p ON op.producto_id = p.id
            WHERE op.orden_id = %s
        """, (orden_id,))

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows


    @staticmethod
    def get_log_stock():
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT l.id, l.stock_antes, l.stock_nuevo, l.fecha,
                p.nombre AS producto
            FROM log_stock l
            JOIN productos p ON l.producto_id = p.id
            ORDER BY l.fecha DESC
        """)

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    # ── Reporte: productos más vendidos (GROUP BY + HAVING) ───
    @staticmethod
    def reporte_mas_vendidos():
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
        SELECT p.nombre,
               SUM(op.cantidad)             AS total_vendidos,
               SUM(op.cantidad * op.precio) AS ingresos
        FROM orden_productos op
        JOIN productos p ON op.producto_id = p.id
        WHERE op.producto_id IN (
            SELECT DISTINCT producto_id
            FROM orden_productos
        )
        GROUP BY p.id, p.nombre
        HAVING total_vendidos > 10
        ORDER BY total_vendidos DESC
    """)

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    @staticmethod
    def get_from_view():
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            "SELECT * FROM vista_ordenes_detalle ORDER BY created_at DESC"
        )

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    # ── Insertar orden con sus productos ─────────────────────
    def save(self, detalles: list):
        """
        detalles: lista de dicts {'producto_id': int, 'cantidad': int, 'precio': float}
        """
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        try:
            connection.begin()

            cursor.execute(
                "INSERT INTO ordenes (cliente_id, usuario_id, total) VALUES (%s, %s, %s)",
                (self.cliente_id, self.usuario_id, self.total)
            )
            self.id = cursor.lastrowid

            for d in detalles:
                cursor.execute(
                    """INSERT INTO orden_productos (orden_id, producto_id, cantidad, precio)
                       VALUES (%s, %s, %s, %s)""",
                    (self.id, d['producto_id'], d['cantidad'], d['precio'])
                )

            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()

    # ── Eliminar ──────────────────────────────────────────────
    def delete(self):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("DELETE FROM ordenes WHERE id = %s", (self.id,))

        connection.commit()
        cursor.close()
        connection.close()

