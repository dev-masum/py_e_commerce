from data.db import get_connection
import bcrypt
import mysql.connector

class AdminAuthService:
    def register(self, name, email, password):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        try:
            cursor.execute(
                "INSERT INTO admins (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed)
            )
            conn.commit()
            return {
                "id": cursor.lastrowid,
                "name": name,
                "email": email
            }
        except mysql.connector.errors.IntegrityError:
            return None
        finally:
            cursor.close()
            conn.close()

    def login(self, email, password):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM admins WHERE email=%s", (email,))
        admin = cursor.fetchone()

        cursor.close()
        conn.close()

        if admin and bcrypt.checkpw(password.encode(), admin["password"].encode()):
            return {
                "id": admin["id"],
                "name": admin["name"],
                "email": admin["email"]
            }
        return None
