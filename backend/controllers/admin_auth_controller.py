from flask import request, jsonify
from middlewares.api_key_required import api_key_required
from services.admin_auth_service import AdminAuthService

admin_auth_service = AdminAuthService()

def response_success(data=None, message="Success"):
    return jsonify({"message": message, "data": data or {}})

def response_error(message="Error", status_code=400):
    return jsonify({"message": message, "data": {}}), status_code

@api_key_required
def admin_register():
    data = request.json
    if not data.get("name") or not data.get("email") or not data.get("password"):
        return response_error("Name, email, and password are required")

    admin = admin_auth_service.register(
        data["name"], data["email"], data["password"]
    )

    if not admin:
        return response_error("Email already exists")

    return response_success(admin, "Admin registered")

def admin_login():
    data = request.json
    if not data.get("email") or not data.get("password"):
        return response_error("Email and password are required")

    admin = admin_auth_service.login(data["email"], data["password"])
    if not admin:
        return response_error("Invalid credentials", 401)

    return response_success(admin, "Admin login successful")
