from flask import Flask, request, jsonify
from .extensions import db, ma, limiter, cache
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    # Import blueprints
    from .blueprints.mechanic.routes import mechanic_bp
    from .blueprints.service_ticket.routes import service_ticket_bp
    from .blueprints.customer.routes import customer_bp
    from .blueprints.inventory.routes import inventory_bp

    # Register blueprints
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    # 🔥 TDD ROUTES (FOR TESTING)

    @app.route('/sum', methods=['POST'])
    def sum_numbers():
        data = request.get_json()
        try:
            return jsonify({'result': data['num1'] + data['num2']}), 200
        except KeyError:
            return jsonify({'message': 'Missing num1 or num2'}), 400

    @app.route('/subtract', methods=['POST'])
    def subtract():
        data = request.get_json()
        try:
            return jsonify({'result': data['num1'] - data['num2']}), 200
        except KeyError:
            return jsonify({'message': 'Missing num1 or num2'}), 400

    @app.route('/multiply', methods=['POST'])
    def multiply():
        data = request.get_json()
        try:
            return jsonify({'result': data['num1'] * data['num2']}), 200
        except KeyError:
            return jsonify({'message': 'Missing num1 or num2'}), 400

    @app.route('/divide', methods=['POST'])
    def divide():
        data = request.get_json()
        try:
            return jsonify({'result': data['num1'] / data['num2']}), 200
        except KeyError:
            return jsonify({'message': 'Missing num1 or num2'}), 400
        except ZeroDivisionError:
            return jsonify({'message': 'Cannot divide by zero'}), 400

    with app.app_context():
        db.create_all()

    return app