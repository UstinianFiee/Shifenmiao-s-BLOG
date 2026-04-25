from flask import Blueprint, request, jsonify
from app.utils.jwt_helper import jwt_required
from app.utils.file_handler import save_upload

upload_bp = Blueprint("upload", __name__)

@upload_bp.post("")
@jwt_required
def upload_file():
    f = request.files.get("file")
    if not f:
        return jsonify({"msg": "未选择文件"}), 400
    try:
        result = save_upload(f)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
