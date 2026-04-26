from . import service_ticket_bp
from flask import request, jsonify
from application.extensions import db
from application.models import ServiceTicket, Mechanic, Inventory
from ..utils.util import token_required, mechanic_token_required

# CREATE ticket
@service_ticket_bp.route("/", methods=["POST"])
@token_required
def create_ticket(customer_id):
    data = request.get_json()

    new_ticket = ServiceTicket(
        description=data["description"],
        customer_id=customer_id
    )

    db.session.add(new_ticket)
    db.session.commit()

    return jsonify({
        "id": new_ticket.id,
        "description": new_ticket.description,
        "customer_id": new_ticket.customer_id
    }), 201


# GET all tickets
@service_ticket_bp.route("/", methods=["GET"])
@mechanic_token_required
def get_tickets(mechanic_id):
    tickets = ServiceTicket.query.all()

    return jsonify([
        {
            "id": t.id,
            "description": t.description,
            "customer_id": t.customer_id,
            "mechanics": [{"id": m.id, "name": m.name} for m in t.mechanics],
            "parts": [{"id": p.id, "name": p.name, "price": p.price} for p in t.parts]
        } for t in tickets
    ])


# GET my tickets (customer)
@service_ticket_bp.route("/my-tickets", methods=["GET"])
@token_required
def my_tickets(customer_id):
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()

    return jsonify([
        {
            "id": t.id,
            "description": t.description,
            "mechanics": [{"id": m.id, "name": m.name} for m in t.mechanics],
            "parts": [{"id": p.id, "name": p.name, "price": p.price} for p in t.parts]
        } for t in tickets
    ])


# ASSIGN mechanic to ticket
@service_ticket_bp.route("/<int:ticket_id>/assign", methods=["PUT"])
@mechanic_token_required
def assign_mechanic(mechanic_id, ticket_id):
    data = request.get_json()

    ticket = ServiceTicket.query.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    mechanic = Mechanic.query.get(data["mechanic_id"])
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    ticket.mechanics.append(mechanic)
    db.session.commit()

    return jsonify({"message": "Mechanic assigned"})


# EDIT ticket - add/remove mechanics
@service_ticket_bp.route("/<int:ticket_id>/edit", methods=["PUT"])
@mechanic_token_required
def edit_ticket(mechanic_id, ticket_id):
    data = request.get_json()

    ticket = ServiceTicket.query.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    if "add_ids" in data:
        for mid in data["add_ids"]:
            mechanic = Mechanic.query.get(mid)
            if mechanic and mechanic not in ticket.mechanics:
                ticket.mechanics.append(mechanic)

    if "remove_ids" in data:
        for mid in data["remove_ids"]:
            mechanic = Mechanic.query.get(mid)
            if mechanic and mechanic in ticket.mechanics:
                ticket.mechanics.remove(mechanic)

    db.session.commit()

    return jsonify({
        "message": "Ticket updated",
        "mechanics": [{"id": m.id, "name": m.name} for m in ticket.mechanics]
    })


# ADD part to ticket
@service_ticket_bp.route("/<int:ticket_id>/add-part", methods=["PUT"])
@mechanic_token_required
def add_part(mechanic_id, ticket_id):
    data = request.get_json()

    ticket = ServiceTicket.query.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    part = Inventory.query.get(data["part_id"])
    if not part:
        return jsonify({"error": "Part not found"}), 404

    if part not in ticket.parts:
        ticket.parts.append(part)

    db.session.commit()

    return jsonify({
        "message": "Part added to ticket",
        "parts": [{"id": p.id, "name": p.name, "price": p.price} for p in ticket.parts]
    })