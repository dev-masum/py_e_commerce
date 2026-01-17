from flask import Blueprint
from controllers.order_controller import place_order, get_orders

order_bp = Blueprint("orders", __name__)
order_bp.route("/", methods=["GET"])(get_orders)
order_bp.route("/<int:user_id>", methods=["GET"])(lambda user_id: get_orders(user_id))
order_bp.route("/<int:user_id>", methods=["POST"])(place_order)
