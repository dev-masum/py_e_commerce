from flask import Blueprint
from controllers.admin_auth_controller import admin_register, admin_login

admin_auth_bp = Blueprint("admin_auth", __name__)
admin_auth_bp.route("/register", methods=["POST"])(admin_register)
admin_auth_bp.route("/login", methods=["POST"])(admin_login)
