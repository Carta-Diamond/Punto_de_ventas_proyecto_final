from persistence.db import get_connection
import pymysql


class Cliente:
    def __init__(self, id: int, nombre: str, email: str,
                 telefono: str, direccion: str):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion

    @staticmethod
    def get_all():
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            "SELECT id, nombre, email, telefono, direccion FROM clientes ORDER BY nombre"
        )

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows


    @staticmethod
    def get_by_id(id: int):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            "SELECT id, nombre, email, telefono, direccion FROM clientes WHERE id = %s",
            (id,)
        )

        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return row

  
    @staticmethod
    def get_by_nombre(nombre: str):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            """SELECT id, nombre, email, telefono, direccion
               FROM clientes WHERE nombre LIKE %s ORDER BY nombre""",
            (f'%{nombre}%',)
        )

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

   
    def save(self):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            """INSERT INTO clientes (nombre, email, telefono, direccion)
               VALUES (%s, %s, %s, %s)""",
            (self.nombre, self.email, self.telefono, self.direccion)
        )

        connection.commit()
        self.id = cursor.lastrowid
        cursor.close()
        connection.close()

    # ── Actualizar ────────────────────────────────────────────
    def update(self):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            """UPDATE clientes SET nombre=%s, email=%s, telefono=%s, direccion=%s
               WHERE id=%s""",
            (self.nombre, self.email, self.telefono, self.direccion, self.id)
        )

        connection.commit()
        cursor.close()
        connection.close()

    # ── Eliminar ──────────────────────────────────────────────
    def delete(self):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            "DELETE FROM clientes WHERE id = %s", (self.id,)
        )

        connection.commit()
        cursor.close()
        connection.close()
