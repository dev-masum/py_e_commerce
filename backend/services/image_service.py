import os
import uuid
from werkzeug.datastructures import FileStorage

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads", "images")
MAX_SIZE_MB = 10

MIME_EXTENSION_MAP = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/gif": "gif",
    "image/webp": "webp",
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class ImageService:
    def save_image(self, file: FileStorage) -> str:
        print("\n========== IMAGE UPLOAD DEBUG START ==========")

        # Basic object info
        print("File object:", file)
        print("File class:", type(file))

        if not file:
            print("ERROR: file is None or False")
            raise ValueError("No file provided")

        # Filename & headers
        print("RAW filename repr:", repr(file.filename))
        print("Filename string:", file.filename)
        print("MIME type:", file.mimetype)
        print("Content-Type header:", file.content_type)
        print("Headers:", dict(file.headers))

        # Size check
        file.seek(0, os.SEEK_END)
        size_bytes = file.tell()
        size_mb = size_bytes / (1024 * 1024)
        file.seek(0)

        print("File size (bytes):", size_bytes)
        print("File size (MB):", round(size_mb, 3))

        if size_mb > MAX_SIZE_MB:
            print("ERROR: File too large")
            raise ValueError(f"File size exceeds {MAX_SIZE_MB} MB")

        # MIME validation
        if file.mimetype not in MIME_EXTENSION_MAP:
            print("ERROR: MIME type not allowed")
            print("Allowed MIME types:", list(MIME_EXTENSION_MAP.keys()))
            raise ValueError("Unsupported image type")

        # Extension resolution
        ext = MIME_EXTENSION_MAP[file.mimetype]
        print("Resolved extension from MIME:", ext)

        # Final filename
        filename = f"{uuid.uuid4().hex}.{ext}"
        save_path = os.path.join(UPLOAD_FOLDER, filename)

        print("Generated filename:", filename)
        print("Saving to path:", save_path)

        try:
            file.save(save_path)
            print("File saved successfully")
        except Exception as e:
            print("ERROR while saving file:", repr(e))
            raise RuntimeError("Failed to save image")

        print("Return URL:", f"/uploads/images/{filename}")
        print("========== IMAGE UPLOAD DEBUG END ==========\n")

        return f"/uploads/images/{filename}"
