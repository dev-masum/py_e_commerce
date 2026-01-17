from functools import wraps
from flask import request, jsonify
from data.db import get_connection

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        admin_id = request.headers.get("X-ADMIN-ID")

        if not admin_id:
            return jsonify({"message": "Admin access required"}), 401

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM admins WHERE id=%s", (admin_id,))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()

        if not admin:
            return jsonify({"message": "Invalid admin"}), 401

        return f(*args, **kwargs)
    return wrapper
