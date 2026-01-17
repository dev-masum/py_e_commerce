from flask import Flask, render_template, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "college_project_secret"

BACKEND_URL = "http://127.0.0.1:5000"


def add_base_url_to_image(product):
    """If product has an image_url, prepend backend base URL."""
    if product and product.get("image_url"):
        if not product["image_url"].startswith("http"):
            product["image_url"] = f"{BACKEND_URL}{product['image_url']}"
    return product


@app.route("/")
def dashboard():
    user = session.get("user")
    if not user:
        return redirect(url_for("auth.login"))

    # Fetch categories and products from backend
    try:
        resp_cat = requests.get(f"{BACKEND_URL}/categories/")
        categories = resp_cat.json().get("data", [])

        resp_prod = requests.get(f"{BACKEND_URL}/products/")
        products = resp_prod.json().get("data", [])

        # Add full URL for product images
        for p in products:
            add_base_url_to_image(p)

    except Exception:
        categories = []
        products = []

    return render_template("dashboard.html", user=user, categories=categories, products=products)
