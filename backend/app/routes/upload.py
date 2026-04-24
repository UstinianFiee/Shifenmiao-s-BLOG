import os, uuid
from flask import Blueprint, request, jsonify, current_app
from app.utils.jwt_helper import jwt_required
from werkzeug.utils import secure_filename

upload_bp = Blueprint("upload", __name__)

ALLOWED_IMAGE = {"png", "jpg", "jpeg", "gif", "webp", "svg"}
ALLOWED_VIDEO = {"mp4", "webm", "ogg", "mov"}
ALLOWED = ALLOWED_IMAGE | ALLOWED_VIDEO

def get_ext(filename):
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

@upload_bp.post("")
@jwt_required
def upload_file():
    f = request.files.get("file")
    if not f:
        return jsonify({"msg": "未选择文件"}), 400
    ext = get_ext(f.filename)
    if ext not in ALLOWED:
        return jsonify({"msg": f"不支持的文件类型 .{ext}"}), 400
    name = f"{uuid.uuid4().hex}.{ext}"
    folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)
    f.save(os.path.join(folder, name))
    file_type = "video" if ext in ALLOWED_VIDEO else "image"
    return jsonify({"url": f"/uploads/{name}", "type": file_type, "name": f.filename}), 201
