import mysql.connector
def connect():
    try:
        conn=mysql.connector.connect(host="localhost",user="root",password="root@39",database="inventory_db")
        return conn
    except mysql.connector.Error as err:
        print("Database connection Failed:", err)
        return None