from flask import request, jsonify
from services.cart_service import CartService
from services.product_service import ProductService

cart_service = CartService()
product_service = ProductService()

def response_success(data=None, message="Success"):
    return jsonify({"message": message, "data": data if data is not None else {}})

def response_error(message="Error", status_code=400):
    return jsonify({"message": message, "data": {}}), status_code

def get_cart(user_id):
    items = cart_service.get_cart(user_id)
    return response_success(items, "Cart retrieved")

def add_to_cart(user_id):
    data = request.json
    if not data.get("product_id") or not data.get("quantity"):
        return response_error("Product ID and quantity are required")
    cart_service.add_item(user_id, data["product_id"], data["quantity"])
    items = cart_service.get_cart(user_id)
    return response_success(items, "Item added to cart")

def remove_from_cart(user_id, product_id):
    cart_service.remove_item(user_id, product_id)
    items = cart_service.get_cart(user_id)
    return response_success(items, "Item removed from cart")

