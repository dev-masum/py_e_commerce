from flask import Blueprint
from controllers.image_controller import upload_image

image_bp = Blueprint("images", __name__)

# Register routes just like cart example
image_bp.route("/upload", methods=["POST"])(upload_image)
