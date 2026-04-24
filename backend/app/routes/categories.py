from flask import Blueprint, request, jsonify
from app import db
from app.models.category import Category
from app.utils.jwt_helper import jwt_required

categories_bp = Blueprint("categories", __name__)

@categories_bp.get("")
def list_categories():
    return jsonify([c.to_dict() for c in Category.query.all()])

@categories_bp.post("")
@jwt_required
def create_category():
    data = request.get_json()
    c = Category(name=data["name"])
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201

@categories_bp.delete("/<int:cid>")
@jwt_required
def delete_category(cid):
    c = Category.query.get_or_404(cid)
    db.session.delete(c)
    db.session.commit()
    return jsonify({"msg": "deleted"})
