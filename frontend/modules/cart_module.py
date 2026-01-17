from flask import Blueprint, render_template, session, redirect, url_for
import requests

cart_bp = Blueprint("cart", __name__, template_folder="../templates")
BACKEND_URL = "http://127.0.0.1:5000"

def get_user_id():
    """Get logged-in user ID from session"""
    user = session.get("user")
    return user["id"] if user else None

def fetch_product_details(product_id):
    """Helper to get product name and price from backend"""
    try:
        resp = requests.get(f"{BACKEND_URL}/products/{product_id}", timeout=5)
        data = resp.json().get("data")
        if data:
            return {"name": data["name"], "price": data["price"]}
    except:
        pass
    return {"name": "Unknown", "price": 0}

# -------------------------------
# View cart page
# -------------------------------
@cart_bp.route("/", methods=["GET"])
def view_cart():
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for("auth.login"))

    error = None
    message = None
    try:
        resp = requests.get(f"{BACKEND_URL}/cart/{user_id}", timeout=5)
        cart = resp.json().get("data", [])

        # Normalize cart keys
        for item in cart:
            item['price'] = float(item.get('price') or item.get('unit_price', 0))
            item['quantity'] = int(item.get('quantity') or item.get('qty', 0))
            item['product_id'] = item.get('product_id') or item.get('id')
            item['product_name'] = item.get('product_name') or item.get('name', 'Unknown')

            # Calculate total_price per item
            item['total_price'] = item['price'] * item['quantity']

    except Exception as e:
        cart = []
        error = str(e)

    return render_template("cart.html", cart=cart, error=error, message=message)

# -------------------------------
# Add item to cart
# -------------------------------
@cart_bp.route("/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for("auth.login"))

    try:
        requests.post(
            f"{BACKEND_URL}/cart/{user_id}",
            json={"product_id": product_id, "quantity": 1},
            timeout=5
        )
    except Exception as e:
        print("Error adding to cart:", e)

    return redirect(url_for("cart.view_cart"))

# -------------------------------
# Remove item from cart
# -------------------------------
@cart_bp.route("/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for("auth.login"))

    try:
        # Correct DELETE endpoint
        requests.delete(f"{BACKEND_URL}/cart/{user_id}/{product_id}", timeout=5)
    except Exception as e:
        print("Error removing from cart:", e)

    return redirect(url_for("cart.view_cart"))
