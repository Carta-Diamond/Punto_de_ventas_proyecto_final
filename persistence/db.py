import pymysql
import pymysql.cursors


def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='250597Pi',
        database='db_sistema_ventas',
        cursorclass=pymysql.cursors.DictCursor
    )
