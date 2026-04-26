from . import customer_bp
from flask import request, jsonify
from application.extensions import db, limiter, cache
from application.models import Customer
from ..utils.util import encode_token, token_required

# CREATE customer
@customer_bp.route("/", methods=["POST"])
@limiter.limit("100 per minute")
def create_customer():
    data = request.get_json()

    new_customer = Customer(
        name=data["name"],
        email=data["email"],
        password=data["password"]
    )

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({
        "id": new_customer.id,
        "name": new_customer.name,
        "email": new_customer.email
    }), 201


# GET customers (CACHED + PAGINATED)
@customer_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)
def get_customers():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    paginated = Customer.query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "customers": [
            {"id": c.id, "name": c.name, "email": c.email}
            for c in paginated.items
        ],
        "total": paginated.total,
        "pages": paginated.pages,
        "current_page": paginated.page
    })


# LOGIN (GET TOKEN)
@customer_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    customer = Customer.query.filter_by(email=data["email"]).first()

    if not customer or customer.password != data["password"]:
        return {"error": "Invalid credentials"}, 401

    token = encode_token(customer.id, role="customer")
    return {"token": token}


# UPDATE customer
@customer_bp.route("/<int:customer_id>", methods=["PUT"])
@token_required
def update_customer(user_id, customer_id):
    if user_id != customer_id:
        return {"error": "Unauthorized"}, 403

    customer = Customer.query.get(customer_id)
    if not customer:
        return {"error": "Customer not found"}, 404

    data = request.get_json()
    customer.name = data.get("name", customer.name)
    customer.email = data.get("email", customer.email)
    customer.password = data.get("password", customer.password)

    db.session.commit()

    return jsonify({
        "id": customer.id,
        "name": customer.name,
        "email": customer.email
    })


# DELETE customer
@customer_bp.route("/<int:customer_id>", methods=["DELETE"])
@token_required
def delete_customer(user_id, customer_id):
    if user_id != customer_id:
        return {"error": "Unauthorized"}, 403

    customer = Customer.query.get(customer_id)
    if not customer:
        return {"error": "Customer not found"}, 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted"})