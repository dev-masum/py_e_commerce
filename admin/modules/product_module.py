from flask import Blueprint, render_template, request, session, redirect, url_for
import requests

BACKEND_URL = "http://127.0.0.1:5000"
product_bp = Blueprint("product", __name__, template_folder="../templates")

def get_admin_headers():
    admin = session.get("admin")
    if not admin:
        return None
    return {"X-ADMIN-ID": str(admin["id"])}

@product_bp.route("/", methods=["GET"])
def list_products():
    headers = get_admin_headers()
    if not headers:
        return redirect(url_for("auth.login"))
    try:
        resp = requests.get(f"{BACKEND_URL}/products/", headers=headers)
        products = resp.json().get("data", [])
    except:
        products = []
    return render_template("admin_products.html", products=products)

@product_bp.route("/add", methods=["GET", "POST"])
def add_product():
    headers = get_admin_headers()
    if not headers:
        return redirect(url_for("auth.login"))

    # Fetch categories for dropdown
    try:
        cat_resp = requests.get(f"{BACKEND_URL}/categories/", headers=headers)
        categories = cat_resp.json().get("data", [])
    except:
        categories = []

    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "price": request.form.get("price"),
            "stock": request.form.get("stock"),
            "category_id": request.form.get("category_id")
        }
        try:
            resp = requests.post(f"{BACKEND_URL}/products/", headers=headers, json=data)
            if resp.status_code == 200:
                return redirect(url_for("product.list_products"))
            else:
                error = resp.json().get("message", "Failed to add product")
                return render_template("admin_add_product.html", categories=categories, error=error)
        except Exception as e:
            return render_template("admin_add_product.html", categories=categories, error=str(e))

    return render_template("admin_add_product.html", categories=categories)

@product_bp.route("/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    headers = get_admin_headers()
    if not headers:
        return redirect(url_for("auth.login"))
    try:
        requests.delete(f"{BACKEND_URL}/products/{product_id}", headers=headers)
    except:
        pass
    return redirect(url_for("product.list_products"))
