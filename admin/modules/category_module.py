from flask import Blueprint, render_template, request, session, redirect, url_for
import requests

BACKEND_URL = "http://127.0.0.1:5000"
category_bp = Blueprint("category", __name__, template_folder="../templates")

def get_admin_headers():
    admin = session.get("admin")
    if not admin:
        return None
    return {"X-ADMIN-ID": str(admin["id"])}

@category_bp.route("/", methods=["GET"])
def list_categories():
    headers = get_admin_headers()
    if not headers:
        return redirect(url_for("auth.login"))
    try:
        resp = requests.get(f"{BACKEND_URL}/categories/", headers=headers)
        categories = resp.json().get("data", [])
    except:
        categories = []
    return render_template("admin_categories.html", categories=categories)

@category_bp.route("/add", methods=["GET", "POST"])
def add_category():
    headers = get_admin_headers()
    if not headers:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        data = {"name": request.form.get("name")}
        try:
            resp = requests.post(f"{BACKEND_URL}/categories/", headers=headers, json=data)
            if resp.status_code == 200:
                return redirect(url_for("category.list_categories"))
            else:
                error = resp.json().get("message", "Failed to add category")
                return render_template("admin_add_category.html", error=error)
        except Exception as e:
            return render_template("admin_add_category.html", error=str(e))

    return render_template("admin_add_category.html")

@category_bp.route("/delete/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    headers = get_admin_headers()
    if not headers:
        return redirect(url_for("auth.login"))
    try:
        requests.delete(f"{BACKEND_URL}/categories/{category_id}", headers=headers)
    except:
        pass
    return redirect(url_for("category.list_categories"))
