from flask import Blueprint, render_template, session, redirect, url_for
import requests

category_bp = Blueprint("category", __name__, template_folder="../templates")
BACKEND_URL = "http://127.0.0.1:5000"

def get_user_id():
    user = session.get("user")
    return user["id"] if user else None

@category_bp.route("/", methods=["GET"])
def list_categories():
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for("auth.login"))

    try:
        resp = requests.get(f"{BACKEND_URL}/categories/")
        categories = resp.json().get("data", [])
    except:
        categories = []

    return render_template("categories.html", categories=categories, message=None, error=None)
