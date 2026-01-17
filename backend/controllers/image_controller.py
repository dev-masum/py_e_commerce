from flask import request, jsonify
from services.image_service import ImageService

image_service = ImageService()

def response_success(data=None, message="Success"):
    return jsonify({"message": message, "data": data if data else {}})

def response_error(message="Error", status_code=400):
    return jsonify({"message": message, "data": {}}), status_code

def upload_image():
    if "image" not in request.files:
        return response_error("No image file provided", 400)

    file = request.files["image"]
    try:
        image_url = image_service.save_image(file)
        return response_success({"image_url": image_url}, "Image uploaded successfully")
    except Exception as e:
        return response_error(str(e), 400)
