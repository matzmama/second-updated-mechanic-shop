from flask import request, jsonify
from application.extensions import db
from application.models import Customer
from . import customer_bp   

@customer_bp.route("/", methods=["POST"])
def create_customer():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data or "password" not in data:
        return jsonify({"message": "Missing required fields"}), 400

    new_customer = Customer(
        name=data["name"],
        email=data["email"],
        password=data["password"]
    )

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"message": "Customer created"}), 201


@customer_bp.route("/", methods=["GET"])
def get_customers():
    customers = Customer.query.all()

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "email": c.email
        } for c in customers
    ]), 200