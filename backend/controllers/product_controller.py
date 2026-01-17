from flask import request, jsonify
from middlewares.admin_required import admin_required
from services.product_service import ProductService

product_service = ProductService()

def response_success(data=None, message="Success"):
    return jsonify({"message": message, "data": data if data is not None else {}})

def response_error(message="Error", status_code=400):
    return jsonify({"message": message, "data": {}}), status_code

# List all products (optionally filtered by category)
def list_products():
    category_name = request.args.get("category")
    if category_name:
        products = product_service.list_by_category(category_name)
    else:
        products = product_service.list()
    return response_success(products, "Products retrieved")


# Admin: Add new product
@admin_required
def add_product():
    data = request.json
    required_fields = ("name", "price", "stock", "category_id")
    if not all(k in data for k in required_fields):
        return response_error("All product fields are required")

    # Include image_url and description if provided
    product = product_service.add(
        name=data["name"],
        price=data["price"],
        stock=data["stock"],
        category_id=data["category_id"],
        image_url=data.get("image_url"),
        description=data.get("description")
    )
    return response_success(product, "Product added")


# Get a single product
def get_product(product_id):
    product = product_service.get(product_id)
    if not product:
        return response_error("Product not found", 404)
    return response_success(product, "Product retrieved")


# Admin: Update existing product
@admin_required
def update_product(product_id):
    data = request.json
    product_service.update(
        product_id,
        name=data.get("name"),
        price=data.get("price"),
        stock=data.get("stock"),
        image_url=data.get("image_url"),
        description=data.get("description")
    )
    updated = product_service.get(product_id)
    return response_success(updated, "Product updated")


# Admin: Delete product
@admin_required
def delete_product(product_id):
    product_service.delete(product_id)
    return response_success({}, "Product deleted")
