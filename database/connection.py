import pymysql
from pymysql.connections import Connection

def connection():
    conn: Connection = pymysql.connect(host="localhost", port=3306, user="root", password="nike",
                                       database="pythonTutorial")
    print("database connect")
    return conn


