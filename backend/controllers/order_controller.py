from flask import jsonify
from services.order_service import OrderService
from services.cart_service import CartService
from services.product_service import ProductService

order_service = OrderService()
cart_service = CartService()
product_service = ProductService()

def response_success(data=None, message="Success"):
    return jsonify({"message": message, "data": data if data is not None else {}})

def response_error(message="Error", status_code=400):
    return jsonify({"message": message, "data": {}}), status_code

def place_order(user_id):
    cart_items = cart_service.get_cart(user_id)
    if not cart_items:
        return response_success([], "Cart is empty")

    # Add product price to each item
    for item in cart_items:
        product = product_service.get(item["product_id"])
        item["price"] = product["price"]

    total_price = sum(item["quantity"] * item["price"] for item in cart_items)
    order = order_service.place_order(user_id, cart_items, total_price)

    cart_service.clear_cart(user_id)
    return response_success(order, "Order placed")

def get_orders(user_id=None):
    orders = order_service.get_orders(user_id)
    return response_success(orders, "Orders retrieved")
