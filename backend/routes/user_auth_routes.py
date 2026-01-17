from flask import Blueprint
from controllers.user_auth_controller import register, login

user_auth_bp = Blueprint("user_auth", __name__)
user_auth_bp.route("/register", methods=["POST"])(register)
user_auth_bp.route("/login", methods=["POST"])(login)
