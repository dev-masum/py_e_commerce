from flask import Blueprint, render_template, request, session, redirect, url_for
import requests

product_bp = Blueprint("product", __name__, template_folder="../templates")
BACKEND_URL = "http://127.0.0.1:5000"

def get_user_id():
    user = session.get("user")
    return user["id"] if user else None

# List all products (optional filtering by category)
@product_bp.route("/", methods=["GET"])
def list_products():
    category = request.args.get("category")
    try:
        url = f"{BACKEND_URL}/products"
        if category:
            url += f"?category={category}"
        resp = requests.get(url)
        products = resp.json().get("data", [])
    except:
        products = []
    return render_template("products.html", products=products)

@product_bp.route("/<int:product_id>", methods=["GET"])
def view_product(product_id):
    try:
        resp = requests.get(f"{BACKEND_URL}/products/{product_id}")
        product = resp.json().get("data")
        if not product:
            return "Product not found", 404
    except:
        product = None
    return render_template("product_detail.html", product=product)
