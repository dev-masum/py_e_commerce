import mysql
from data.db import get_connection
import bcrypt

class UserAuthService:
    def register(self, name, email, password):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                           (name, email, hashed))
            conn.commit()
            user_id = cursor.lastrowid
            return {"id": user_id, "name": name, "email": email}
        except mysql.connector.errors.IntegrityError:
            return None  # email already exists
        finally:
            cursor.close()
            conn.close()

    def login(self, email, password):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
            return {"id": user["id"], "name": user["name"], "email": user["email"]}
        return None
