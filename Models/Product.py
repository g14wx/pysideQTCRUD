from pymysql.connections import Connection

class Product:
    def __init__(self, conn: Connection ):
        self.conn = conn
        with self.conn.cursor() as cursor:
            sql = """CREATE TABLE IF NOT EXISTS products (
                    cod varchar(45),
                    title varchar(45),
                    price varchar(45),
                    category varchar(45)
                    )"""
            cursor.execute(sql)
            self.conn.commit()

    def get_products(self):
        with self.conn.cursor() as cursor:
            sql = """ select * from products """
            cursor.execute(sql)
            products = cursor.fetchall()
            return products
    def save(self,cod:str,title:str,price : str,cat: str):
        with self.conn.cursor() as cursor:
            sql = """ INSERT INTO products (cod,title,price,category) VALUES (%s,%s,%s,%s) """
            cursor.execute(sql,(cod,title,price,cat))
            return self.conn.commit()

    def get_product(self,cod:str):
        with self.conn.cursor() as cursor:
            sql = """ SELECT * FROM products WHERE cod = %s """
            cursor.execute(sql, (cod))
            return cursor.fetchone()
        
    def update(self,cod:str,title:str,price : str,cat: str):
        with self.conn.cursor() as cursor:
            sql = """UPDATE products SET title=%s, price= %s, category= %s WHERE cod = %s"""
            cursor.execute(sql,(title,price,cat,cod))
            self.conn.commit()

    def delete(self,cod:str):
        with self.conn.cursor() as cursor:
            sql = """ DELETE FROM products WHERE cod = %s """
            cursor.execute(sql, (cod))
            self.conn.commit()