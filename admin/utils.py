from flask import session, redirect, url_for
from functools import wraps

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper
