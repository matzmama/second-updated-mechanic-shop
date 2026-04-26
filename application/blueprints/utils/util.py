from jose import jwt, JWTError
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app

def encode_token(user_id, role="customer"):
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )

def decode_token(token):
    try:
        return jwt.decode(
            token,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=["HS256"]
        )
    except JWTError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "Token missing"}), 401

        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"message": "Invalid token format"}), 401

        token = parts[1]
        data = decode_token(token)

        if not data:
            return jsonify({"message": "Invalid token"}), 401

        user_id = int(data["sub"])
        return f(user_id, *args, **kwargs)

    return decorated

def mechanic_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "Token missing"}), 401

        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"message": "Invalid token format"}), 401

        token = parts[1]
        data = decode_token(token)

        if not data:
            return jsonify({"message": "Invalid token"}), 401

        if data.get("role") != "mechanic":
            return jsonify({"message": "Mechanic access required"}), 403

        user_id = int(data["sub"])
        return f(user_id, *args, **kwargs)

    return decorated