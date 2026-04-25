import os, uuid
from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models.media import Media
from app.utils.jwt_helper import jwt_required

media_bp = Blueprint("media", __name__)

ALLOWED_IMAGE = {"png", "jpg", "jpeg", "gif", "webp", "svg"}
ALLOWED_VIDEO = {"mp4", "webm", "ogg", "mov"}
ALLOWED_AUDIO = {"mp3", "wav", "ogg", "flac", "aac", "m4a"}
ALLOWED = ALLOWED_IMAGE | ALLOWED_VIDEO | ALLOWED_AUDIO

def get_ext(filename):
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

# 公开：获取媒体列表（前台展示用）
@media_bp.get("")
def list_media():
    file_type = request.args.get("type")  # image | video | None=all
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    q = Media.query
    if file_type:
        q = q.filter_by(file_type=file_type)
    pagination = q.order_by(Media.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "items": [m.to_dict() for m in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
    })

@media_bp.get("/<int:mid>")
def get_media(mid):
    m = Media.query.get_or_404(mid)
    return jsonify(m.to_dict())

# 管理：上传并保存到媒体库
@media_bp.post("")
@jwt_required
def upload_media():
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
    file_type = "video" if ext in ALLOWED_VIDEO else ("audio" if ext in ALLOWED_AUDIO else "image")
    m = Media(
        name=f.filename,
        url=f"/uploads/{name}",
        file_type=file_type,
        caption=request.form.get("caption", ""),
    )
    db.session.add(m)
    db.session.commit()
    return jsonify(m.to_dict()), 201

@media_bp.put("/<int:mid>")
@jwt_required
def update_media(mid):
    m = Media.query.get_or_404(mid)
    data = request.get_json()
    if "caption" in data:
        m.caption = data["caption"]
    db.session.commit()
    return jsonify(m.to_dict())

@media_bp.delete("/<int:mid>")
@jwt_required
def delete_media(mid):
    m = Media.query.get_or_404(mid)
    # 删除文件
    try:
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], m.url.split("/uploads/")[-1])
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass
    db.session.delete(m)
    db.session.commit()
    return jsonify({"msg": "deleted"})
