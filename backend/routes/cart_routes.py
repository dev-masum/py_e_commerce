from flask import Blueprint
from controllers.cart_controller import get_cart, add_to_cart, remove_from_cart

cart_bp = Blueprint("cart", __name__)
cart_bp.route("/<int:user_id>", methods=["GET"])(get_cart)
cart_bp.route("/<int:user_id>", methods=["POST"])(add_to_cart)
cart_bp.route("/<int:user_id>/<int:product_id>", methods=["DELETE"])(remove_from_cart)
