from flask import Blueprint
from controllers.category_controller import list_categories, add_category

category_bp = Blueprint("categories", __name__)
category_bp.route("/", methods=["GET"])(list_categories)
category_bp.route("/", methods=["POST"])(add_category)
