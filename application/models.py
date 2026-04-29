from .extensions import db

service_mechanic = db.Table(
    "service_mechanic",
    db.Column("service_ticket_id", db.Integer, db.ForeignKey("service_tickets.id")),
    db.Column("mechanic_id", db.Integer, db.ForeignKey("mechanics.id"))
)

# MANY-TO-MANY: service_inventory
service_inventory = db.Table(
    "service_inventory",
    db.Column("service_ticket_id", db.Integer, db.ForeignKey("service_tickets.id")),
    db.Column("inventory_id", db.Integer, db.ForeignKey("inventory.id"))
)

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    tickets = db.relationship("ServiceTicket", back_populates="customer")


class Mechanic(db.Model):
    __tablename__ = "mechanics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    tickets = db.relationship(
        "ServiceTicket",
        secondary=service_mechanic,
        back_populates="mechanics"
    )


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    tickets = db.relationship(
        "ServiceTicket",
        secondary=service_inventory,
        back_populates="parts"
    )


class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=True)

    customer = db.relationship("Customer", back_populates="tickets")
    mechanics = db.relationship(
        "Mechanic",
        secondary=service_mechanic,
        back_populates="tickets"
    )
    parts = db.relationship(
        "Inventory",
        secondary=service_inventory,
        back_populates="tickets"
    )