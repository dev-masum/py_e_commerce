from flask import Blueprint, render_template
import requests
from utils import admin_required

order_bp = Blueprint("order", __name__, template_folder="../templates")
BACKEND_URL = "http://127.0.0.1:5000"

@order_bp.route("/")
@admin_required
def list_orders():
    try:
        resp = requests.get(f"{BACKEND_URL}/orders/")
        orders = resp.json().get("data", [])
    except:
        orders = []

    return render_template("admin_orders.html", orders=orders)
