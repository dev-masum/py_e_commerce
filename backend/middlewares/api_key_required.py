from functools import wraps
from flask import request, jsonify

API_KEY = "api-key"

def api_key_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")

        if not api_key:
            return jsonify({"message": "API key required"}), 401

        if api_key != API_KEY:
            return jsonify({"message": "Invalid API key"}), 401

        return f(*args, **kwargs)
    return wrapper
