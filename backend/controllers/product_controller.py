from flask import request, jsonify
from middlewares.admin_required import admin_required
from services.product_service import ProductService

product_service = ProductService()

def response_success(data=None, message="Success"):
    return jsonify({"message": message, "data": data if data is not None else {}})

def response_error(message="Error", status_code=400):
    return jsonify({"message": message, "data": {}}), status_code

def list_products():
    category_name = request.args.get("category")  # get category from query params
    if category_name:
        products = product_service.list_by_category(category_name)
    else:
        products = product_service.list()
    return response_success(products, "Products retrieved")


@admin_required
def add_product():
    data = request.json
    if not all(k in data for k in ("name", "price", "stock", "category_id")):
        return response_error("All product fields are required")

    product = product_service.add(data["name"], data["price"], data["stock"], data["category_id"])
    return response_success(product, "Product added")

def get_product(product_id):
    product = product_service.get(product_id)
    if not product:
        return response_error("Product not found")
    return response_success(product, "Product retrieved")

@admin_required
def update_product(product_id):
    data = request.json
    product_service.update(product_id, data.get("name"), data.get("price"), data.get("stock"))
    updated = product_service.get(product_id)
    return response_success(updated, "Product updated")

@admin_required
def delete_product(product_id):
    product_service.delete(product_id)
    return response_success({}, "Product deleted")
