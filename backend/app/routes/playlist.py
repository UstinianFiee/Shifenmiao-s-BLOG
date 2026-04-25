from flask import Blueprint, request, jsonify
from app import db
from app.models.playlist import PlaylistItem
from app.utils.jwt_helper import jwt_required

playlist_bp = Blueprint("playlist", __name__)

# 公开：前台获取播放列表
@playlist_bp.get("")
def get_playlist():
    items = PlaylistItem.query.order_by(PlaylistItem.sort, PlaylistItem.id).all()
    return jsonify([i.to_dict() for i in items])

# 管理：添加曲目
@playlist_bp.post("")
@jwt_required
def add_item():
    data = request.get_json()
    item = PlaylistItem(
        title=data.get("title", "未知曲目"),
        artist=data.get("artist", ""),
        url=data["url"],
        cover=data.get("cover", ""),
        sort=data.get("sort", 0),
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

# 管理：更新曲目
@playlist_bp.put("/<int:pid>")
@jwt_required
def update_item(pid):
    item = PlaylistItem.query.get_or_404(pid)
    data = request.get_json()
    for f in ("title", "artist", "url", "cover", "sort"):
        if f in data:
            setattr(item, f, data[f])
    db.session.commit()
    return jsonify(item.to_dict())

# 管理：删除曲目
@playlist_bp.delete("/<int:pid>")
@jwt_required
def delete_item(pid):
    item = PlaylistItem.query.get_or_404(pid)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"msg": "deleted"})
