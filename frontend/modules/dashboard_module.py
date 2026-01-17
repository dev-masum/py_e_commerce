from flask import Flask, render_template, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "college_project_secret"

BACKEND_URL = "http://127.0.0.1:5000"

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
    except:
        categories = []
        products = []

    return render_template("dashboard.html", user=user, categories=categories, products=products)
