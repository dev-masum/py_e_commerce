from flask import request, jsonify
from services.user_auth_service import UserAuthService

auth_service = UserAuthService()

def response_success(data=None, message="Success"):
    return jsonify({"message": message, "data": data if data is not None else {}})

def response_error(message="Error", status_code=400):
    return jsonify({"message": message, "data": {}}), status_code

def register():
    data = request.json
    if not data.get("name") or not data.get("email") or not data.get("password"):
        return response_error("Name, email, and password are required")

    user = auth_service.register(data["name"], data["email"], data["password"])
    if not user:
        return response_error("Email already exists")

    return response_success({"id": user["id"], "name": user["name"], "email": user["email"]}, "User registered")

def login():
    data = request.json
    if not data.get("email") or not data.get("password"):
        return response_error("Email and password are required")

    user = auth_service.login(data["email"], data["password"])
    if not user:
        return response_error("Invalid credentials", 401)

    return response_success({"id": user["id"], "name": user["name"], "email": user["email"]}, "Login successful")
