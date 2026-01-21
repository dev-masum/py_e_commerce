from flask import Blueprint, render_template, session, redirect, url_for, flash
import requests

order_bp = Blueprint("order", __name__, template_folder="../templates")
BACKEND_URL = "http://127.0.0.1:5000"

def get_user_id():
    user = session.get("user")
    return user["id"] if user else None

@order_bp.route("/", methods=["GET"])
def view_my_orders():
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for("auth.login"))

    orders = []
    message = None
    error = None

    try:
        resp = requests.get(f"{BACKEND_URL}/orders/{user_id}", timeout=5)
        data = resp.json()
        orders = data.get("data", [])
        message = data.get("message", None)

        # Convert price strings to float and calculate total_price
        for order in orders:
            total = sum(item["quantity"] * float(item["price"]) for item in order["products"])
            order["total_price"] = total

    except Exception as e:
        print("Error fetching orders:", e)
        error = "Could not fetch orders at this time."

    return render_template("orders.html", orders=orders, message=message, error=error)


@order_bp.route("/place", methods=["POST"])
def place_order():
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for("auth.login"))

    try:
        resp = requests.post(f"{BACKEND_URL}/orders/{user_id}", timeout=5)
        if resp.status_code == 200:
            flash("Order placed successfully!", "success")
        else:
            flash("Failed to place order.", "error")
    except Exception as e:
        print("Error placing order:", e)
        flash("Could not place order at this time.", "error")

    return redirect(url_for("order.view_my_orders"))

@order_bp.route("/payment")
def payment():
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for("auth.login"))

    error = None
    message = None
    cart_items = []
    total_price = 0.0

    try:
        # Get cart items
        resp = requests.get(f"{BACKEND_URL}/cart/{user_id}", timeout=5)
        cart = resp.json().get("data", [])

        for item in cart:
            product_id = item.get("product_id") or item.get("id")
            quantity = int(item.get("quantity") or item.get("qty") or 0)

            # Fetch product info
            try:
                prod_resp = requests.get(f"{BACKEND_URL}/products/{product_id}", timeout=5)
                prod_data = prod_resp.json().get("data", {})
            except:
                prod_data = {}

            price = float(prod_data.get("price") or 0)
            name = prod_data.get("name") or "Unknown"
            image_url = prod_data.get("image_url")
            if image_url and not image_url.startswith("http"):
                image_url = BACKEND_URL + image_url

            # Append normalized item
            cart_items.append({
                "product_id": product_id,
                "product_name": name,
                "price": price,
                "quantity": quantity,
                "image_url": image_url
            })

            # Update total
            total_price += price * quantity

    except Exception as e:
        cart_items = []
        error = str(e)

    return render_template("payment.html", cart=cart_items, total_price=round(total_price, 2))

