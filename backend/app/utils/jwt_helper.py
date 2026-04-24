import jwt
import time
from functools import wraps
from flask import request, jsonify, current_app


def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "iat": int(time.time()),
        "exp": int(time.time()) + 86400,  # 1 day
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")


def decode_token(token: str) -> dict:
    return jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"msg": "Missing token"}), 401
        token = auth[7:]
        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"msg": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"msg": "Invalid token"}), 401
        request.current_user_id = payload["sub"]
        return f(*args, **kwargs)
    return decorated


def get_jwt_identity():
    return request.current_user_id
