from flask import Blueprint, request, jsonify
from app import db
from app.models.tag import Tag
from app.utils.jwt_helper import jwt_required

tags_bp = Blueprint("tags", __name__)

@tags_bp.get("")
def list_tags():
    return jsonify([t.to_dict() for t in Tag.query.all()])

@tags_bp.post("")
@jwt_required
def create_tag():
    data = request.get_json()
    t = Tag(name=data["name"])
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201

@tags_bp.delete("/<int:tid>")
@jwt_required
def delete_tag(tid):
    t = Tag.query.get_or_404(tid)
    db.session.delete(t)
    db.session.commit()
    return jsonify({"msg": "deleted"})
