import os, uuid
from flask import Blueprint, request, jsonify, current_app
from app.utils.jwt_helper import jwt_required
from werkzeug.utils import secure_filename

upload_bp = Blueprint("upload", __name__)

ALLOWED = {"png", "jpg", "jpeg", "gif", "webp", "svg"}

def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED

@upload_bp.post("")
@jwt_required
def upload_file():
    f = request.files.get("file")
    if not f or not allowed(f.filename):
        return jsonify({"msg": "不支持的文件类型"}), 400
    ext = f.filename.rsplit(".", 1)[1].lower()
    name = f"{uuid.uuid4().hex}.{ext}"
    folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)
    f.save(os.path.join(folder, name))
    return jsonify({"url": f"/uploads/{name}"}), 201
