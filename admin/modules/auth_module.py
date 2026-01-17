from flask import Blueprint, render_template, request, session, redirect, url_for
import requests

auth_bp = Blueprint("auth", __name__, template_folder="../templates")
BACKEND_URL = "http://127.0.0.1:5000"

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            resp = requests.post(f"{BACKEND_URL}/auth/admin/login", json={
                "email": email,
                "password": password
            })
            data = resp.json()

            if resp.status_code == 200:
                session["admin"] = data["data"]
                return redirect(url_for("dashboard"))
            else:
                error = data.get("message", "Invalid credentials")
        except Exception as e:
            error = str(e)

    return render_template("admin_login.html", error=error)

@auth_bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("auth.login"))
