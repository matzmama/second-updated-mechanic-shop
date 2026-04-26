from . import inventory_bp
from flask import request, jsonify
from application.extensions import db
from application.models import Inventory
from ..utils.util import mechanic_token_required

# CREATE part
@inventory_bp.route("/", methods=["POST"])
@mechanic_token_required
def create_part(mechanic_id):
    data = request.get_json()

    new_part = Inventory(
        name=data["name"],
        price=data["price"]
    )

    db.session.add(new_part)
    db.session.commit()

    return jsonify({
        "id": new_part.id,
        "name": new_part.name,
        "price": new_part.price
    }), 201


# GET all parts
@inventory_bp.route("/", methods=["GET"])
def get_parts():
    parts = Inventory.query.all()

    return jsonify([
        {"id": p.id, "name": p.name, "price": p.price} for p in parts
    ])


# GET single part
@inventory_bp.route("/<int:part_id>", methods=["GET"])
def get_part(part_id):
    part = Inventory.query.get(part_id)

    if not part:
        return jsonify({"error": "Part not found"}), 404

    return jsonify({
        "id": part.id,
        "name": part.name,
        "price": part.price
    })


# UPDATE part
@inventory_bp.route("/<int:part_id>", methods=["PUT"])
@mechanic_token_required
def update_part(mechanic_id, part_id):
    part = Inventory.query.get(part_id)

    if not part:
        return jsonify({"error": "Part not found"}), 404

    data = request.get_json()
    part.name = data.get("name", part.name)
    part.price = data.get("price", part.price)

    db.session.commit()

    return jsonify({
        "id": part.id,
        "name": part.name,
        "price": part.price
    })


# DELETE part
@inventory_bp.route("/<int:part_id>", methods=["DELETE"])
@mechanic_token_required
def delete_part(mechanic_id, part_id):
    part = Inventory.query.get(part_id)

    if not part:
        return jsonify({"error": "Part not found"}), 404

    db.session.delete(part)
    db.session.commit()

    return jsonify({"message": "Part deleted"})