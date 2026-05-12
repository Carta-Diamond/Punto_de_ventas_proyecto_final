from persistence.db import get_connection
import pymysql


class Producto:
    def __init__(self, id: int, nombre: str, descripcion: str,
                 precio: float, precio_oferta: float,
                 stock: int, categoria_id: int):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.precio_oferta = precio_oferta
        self.stock = stock
        self.categoria_id = categoria_id

    # ── Listar todos (JOIN con categorias) ────────────────────
    @staticmethod
    def get_all():
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT p.id, p.nombre, p.descripcion, p.precio,
                   p.precio_oferta, p.stock,
                   c.id AS categoria_id, c.nombre AS categoria
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            ORDER BY p.nombre
        """)

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    # ── Buscar por ID ─────────────────────────────────────────
    @staticmethod
    def get_by_id(id: int):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT p.id, p.nombre, p.descripcion, p.precio,
                   p.precio_oferta, p.stock,
                   c.id AS categoria_id, c.nombre AS categoria
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE p.id = %s
        """, (id,))

        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return row

    # ── Buscar por nombre (LIKE) ──────────────────────────────
    @staticmethod
    def get_by_nombre(nombre: str):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT p.id, p.nombre, p.descripcion, p.precio,
                   p.precio_oferta, p.stock,
                   c.id AS categoria_id, c.nombre AS categoria
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE p.nombre LIKE %s
            ORDER BY p.nombre
        """, (f'%{nombre}%',))

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    # ── Buscar por categoría ──────────────────────────────────
    @staticmethod
    def get_by_categoria(categoria_id: int):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT p.id, p.nombre, p.descripcion, p.precio,
                   p.precio_oferta, p.stock,
                   c.id AS categoria_id, c.nombre AS categoria
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE p.categoria_id = %s
            ORDER BY p.nombre
        """, (categoria_id,))

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    # ── Productos en oferta ───────────────────────────────────
    @staticmethod
    def get_en_oferta():
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT p.id, p.nombre, p.descripcion, p.precio,
                   p.precio_oferta, p.stock,
                   c.id AS categoria_id, c.nombre AS categoria
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE p.precio_oferta IS NOT NULL
            ORDER BY p.nombre
        """)

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    # ── Obtener categorias (para el filtro) ───────────────────
    @staticmethod
    def get_categorias():
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT id, nombre FROM categorias ORDER BY nombre")

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    # ── Insertar ──────────────────────────────────────────────
    def save(self):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            INSERT INTO productos
            (nombre, descripcion, precio, precio_oferta, stock, categoria_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (self.nombre, self.descripcion, self.precio,
              self.precio_oferta, self.stock, self.categoria_id))

        connection.commit()
        self.id = cursor.lastrowid
        cursor.close()
        connection.close()

    # ── Actualizar ────────────────────────────────────────────
    def update(self):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            UPDATE productos
            SET nombre=%s, descripcion=%s, precio=%s,
                precio_oferta=%s, stock=%s, categoria_id=%s
            WHERE id=%s
        """, (self.nombre, self.descripcion, self.precio,
              self.precio_oferta, self.stock, self.categoria_id, self.id))

        connection.commit()
        cursor.close()
        connection.close()

    # En entities/producto.py - agregar este método

    @staticmethod
    def get_productos_nunca_vendidos():

        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock,
                c.nombre AS categoria
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE p.id NOT IN (
                SELECT DISTINCT producto_id 
                FROM orden_productos
            )
            ORDER BY p.nombre
        """)
        
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    # ── Eliminar ──────────────────────────────────────────────
    def delete(self):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            "DELETE FROM productos WHERE id = %s", (self.id,)
        )

        connection.commit()
        cursor.close()
        connection.close()
