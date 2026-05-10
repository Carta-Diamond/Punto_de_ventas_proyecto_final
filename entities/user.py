from persistence.db import get_connection
from enums.profile import Profile
import pymysql


class User:
    def __init__(self, id: int, nombre: str, email: str,
                 password: str, profile: Profile, is_active: bool):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.profile = profile
        self.active = is_active

    @property
    def is_active(self):
        return self.active

    def is_admin(self):
        return self.profile == Profile.ADMIN

    # ── Listar todos ──────────────────────────────────────────
    @staticmethod
    def get_all():
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            "SELECT id, nombre, email, is_active, rol FROM usuarios ORDER BY nombre"
        )

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    # ── Buscar por ID ─────────────────────────────────────────
    @staticmethod
    def get_by_id(id: int):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            "SELECT id, nombre, email, is_active, rol FROM usuarios WHERE id = %s",
            (id,)
        )

        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return row

    # ── Verificar si email existe ─────────────────────────────
    @staticmethod
    def check_email_exists(email) -> bool:
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            "SELECT email FROM usuarios WHERE email = %s", (email,)
        )

        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return row is not None

    # ── Insertar ──────────────────────────────────────────────
    def save(self):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            """INSERT INTO usuarios (nombre, email, password_hash, is_active, rol)
               VALUES (%s, %s, %s, %s, %s)""",
            (self.nombre, self.email, self.password,
             self.active, self.profile.name.lower())
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
            """UPDATE usuarios
               SET nombre=%s, email=%s, is_active=%s, rol=%s
               WHERE id=%s""",
            (self.nombre, self.email,
             self.active, self.profile.name.lower(), self.id)
        )

        connection.commit()
        cursor.close()
        connection.close()

    # ── Eliminar ──────────────────────────────────────────────
    def delete(self):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            "DELETE FROM usuarios WHERE id = %s", (self.id,)
        )

        connection.commit()
        cursor.close()
        connection.close()
