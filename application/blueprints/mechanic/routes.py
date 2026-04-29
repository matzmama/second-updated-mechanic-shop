from . import mechanic_bp
from flask import request, jsonify
from application.extensions import db, limiter, cache
from application.models import Mechanic
from ..utils.util import encode_token, token_required, mechanic_token_required

@mechanic_bp.route("/", methods=["POST"])
@limiter.limit("100 per minute")
def create_mechanic():
    data = request.get_json()

    new_mechanic = Mechanic(name=data["name"])
    db.session.add(new_mechanic)
    db.session.commit()

    return jsonify({
        "id": new_mechanic.id,
        "name": new_mechanic.name
    }), 201

@mechanic_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)
def get_mechanics():
    mechanics = Mechanic.query.all()

    sorted_mechanics = sorted(mechanics, key=lambda m: len(m.tickets), reverse=True)

    return jsonify([
        {
            "id": m.id,
            "name": m.name,
            "tickets_worked": len(m.tickets)
        } for m in sorted_mechanics
    ])

@mechanic_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    mechanic = Mechanic.query.get(data["id"])

    if not mechanic:
        return {"error": "Invalid mechanic"}, 401

    token = encode_token(mechanic.id, role="mechanic")
    return {"token": token}


@mechanic_bp.route("/protected", methods=["GET"])
@mechanic_token_required
def protected(user_id):
    return {"message": f"Access granted for mechanic {user_id}"}