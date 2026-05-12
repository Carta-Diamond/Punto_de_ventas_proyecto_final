import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='admin',
        database='db_sistema_ventas'
    )