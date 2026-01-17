from flask import Blueprint, render_template, request, session, redirect, url_for
import requests

auth_bp = Blueprint("auth", __name__, template_folder="../templates")
BACKEND_URL = "http://127.0.0.1:5000"

# -------------------------------
# Login
# -------------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            resp = requests.post(f"{BACKEND_URL}/auth/user/login", json={
                "email": email,
                "password": password
            }, timeout=5)
            data = resp.json()

            # Backend returns 401 for invalid credentials
            if resp.status_code == 200 and data.get("data"):
                session["user"] = data["data"]
                return redirect(url_for("dashboard"))
            else:
                error = data.get("message", "Login failed")

        except Exception as e:
            error = str(e)

    return render_template("login.html", error=error)

# -------------------------------
# Register
# -------------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            resp = requests.post(f"{BACKEND_URL}/auth/user/register", json={
                "name": name,
                "email": email,
                "password": password
            }, timeout=5)
            data = resp.json()

            if resp.status_code == 200 and data.get("data"):
                session["user"] = data["data"]
                return redirect(url_for("dashboard"))
            else:
                error = data.get("message", "Registration failed")

        except Exception as e:
            error = str(e)

    return render_template("register.html", error=error)

# -------------------------------
# Logout
# -------------------------------
@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))
