from flask import Blueprint
from controllers.product_controller import list_products, get_product, add_product, update_product, delete_product

product_bp = Blueprint("products", __name__)
product_bp.route("/", methods=["GET"])(list_products)
product_bp.route("/<int:product_id>", methods=["GET"])(get_product)
product_bp.route("/", methods=["POST"])(add_product)
product_bp.route("/<int:product_id>", methods=["PUT"])(update_product)
product_bp.route("/<int:product_id>", methods=["DELETE"])(delete_product)
