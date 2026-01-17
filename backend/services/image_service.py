import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads", "images")
MAX_SIZE_MB = 10

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class ImageService:
    def save_image(self, file):
        if not file:
            raise ValueError("No file provided")

        # Check file size
        file.seek(0, os.SEEK_END)
        size_mb = file.tell() / (1024 * 1024)
        file.seek(0)
        if size_mb > MAX_SIZE_MB:
            raise ValueError(f"File size exceeds {MAX_SIZE_MB} MB")

        # Save file
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        # Return the relative URL
        return f"/uploads/images/{filename}"
