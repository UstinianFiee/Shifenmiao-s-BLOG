from flask import Blueprint, request, jsonify
from app.models.user import User
from app.utils.jwt_helper import create_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/login")
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()
    if not user or not user.check_password(data.get("password", "")):
        return jsonify({"msg": "用户名或密码错误"}), 401
    token = create_token(user.id)
    return jsonify({"token": token, "username": user.username})

@auth_bp.get("/me")
@jwt_required
def me():
    uid = get_jwt_identity()
    user = User.query.get(uid)
    return jsonify({"id": user.id, "username": user.username})
