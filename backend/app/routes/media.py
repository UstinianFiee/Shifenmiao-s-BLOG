import os
from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models.media import Media
from app.utils.jwt_helper import jwt_required
from app.utils.file_handler import save_upload, ALLOWED_IMAGE, ALLOWED_VIDEO

media_bp = Blueprint("media", __name__)

@media_bp.get("")
def list_media():
    file_type = request.args.get("type")
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

@media_bp.post("")
@jwt_required
def upload_media():
    f = request.files.get("file")
    if not f:
        return jsonify({"msg": "未选择文件"}), 400
    try:
        result = save_upload(f, allowed=ALLOWED_IMAGE | ALLOWED_VIDEO)
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    m = Media(
        name=result["name"],
        url=result["url"],
        file_type=result["type"],
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
    try:
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], m.url.split("/uploads/")[-1])
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass
    db.session.delete(m)
    db.session.commit()
    return jsonify({"msg": "deleted"})
