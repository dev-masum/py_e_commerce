from .user_auth_routes import user_auth_bp
from .product_routes import product_bp
from .category_routes import category_bp
from .cart_routes import cart_bp
from .order_routes import order_bp
from .admin_auth_routes import admin_auth_bp

def register_routes(app):
    app.register_blueprint(user_auth_bp, url_prefix="/auth/user")
    app.register_blueprint(admin_auth_bp, url_prefix="/auth/admin")
    app.register_blueprint(product_bp, url_prefix="/products")
    app.register_blueprint(category_bp, url_prefix="/categories")
    app.register_blueprint(cart_bp, url_prefix="/cart")
    app.register_blueprint(order_bp, url_prefix="/orders")

