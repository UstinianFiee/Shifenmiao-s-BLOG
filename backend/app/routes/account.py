from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.models.profile import Profile
from app.utils.jwt_helper import jwt_required, get_jwt_identity

account_bp = Blueprint("account", __name__)

def _get_profile():
    p = Profile.query.first()
    if not p:
        p = Profile()
        db.session.add(p)
        db.session.commit()
    return p

# 公开接口：前台关于页读取
@account_bp.get("/profile")
def get_profile():
    return jsonify(_get_profile().to_dict())

# 以下需要登录

@account_bp.put("/profile")
@jwt_required
def update_profile():
    data = request.get_json()
    p = _get_profile()
    for field in ("nickname", "bio", "avatar"):
        if field in data:
            setattr(p, field, data[field])
    db.session.commit()
    return jsonify(p.to_dict())

@account_bp.put("/password")
@jwt_required
def change_password():
    data = request.get_json()
    uid = get_jwt_identity()
    user = User.query.get(uid)
    if not user.check_password(data.get("old_password", "")):
        return jsonify({"msg": "原密码错误"}), 400
    new_pwd = data.get("new_password", "")
    if len(new_pwd) < 6:
        return jsonify({"msg": "新密码至少6位"}), 400
    user.set_password(new_pwd)
    db.session.commit()
    return jsonify({"msg": "密码修改成功"})

@account_bp.put("/username")
@jwt_required
def change_username():
    data = request.get_json()
    uid = get_jwt_identity()
    user = User.query.get(uid)
    new_name = data.get("username", "").strip()
    if not new_name:
        return jsonify({"msg": "用户名不能为空"}), 400
    if User.query.filter(User.username == new_name, User.id != user.id).first():
        return jsonify({"msg": "用户名已存在"}), 400
    user.username = new_name
    db.session.commit()
    return jsonify({"msg": "用户名修改成功", "username": user.username})
