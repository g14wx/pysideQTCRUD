# This Python file uses the following encoding: utf-8

from pymysql.connections import Connection


class User:
    def __init__(self, conn: Connection):
        self.conn = conn
        with self.conn.cursor() as cursor:
            sql = """CREATE TABLE IF NOT EXISTS pythonTutorial.users(nombre VARCHAR(45),
                        password VARCHAR(191))"""
            cursor.execute(sql)
            self.conn.commit()

    def get_user(self, user: str, password: str):
        with self.conn.cursor() as cursor:
            sql = """ SELECT * FROM users WHERE nombre=%s AND password=%s"""
            cursor.execute(sql, (user, password))
            result = cursor.fetchone()
            return result
