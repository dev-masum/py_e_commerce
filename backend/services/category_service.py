import mysql
from data.db import get_connection

class CategoryService:
    def list(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        return categories

    def add(self, name):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
            conn.commit()
            return {"id": cursor.lastrowid, "name": name}
        except mysql.connector.errors.IntegrityError:
            return None
        finally:
            cursor.close()
            conn.close()
