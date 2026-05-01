from flask import Flask
from .extensions import db, ma, limiter, cache

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    from .blueprints.mechanic.routes import mechanic_bp
    from .blueprints.service_ticket.routes import service_ticket_bp
    from .blueprints.customer.routes import customer_bp
    from .blueprints.inventory.routes import inventory_bp

    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    with app.app_context():
        db.create_all()

    return app