import unittest
from application import create_app
from application.extensions import db

class TestServiceTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get_service_tickets(self):
        response = self.client.get("/service-tickets/")
        self.assertEqual(response.status_code, 200)

    def test_create_service_ticket(self):
        response = self.client.post("/service-tickets/", json={})
        self.assertIn(response.status_code, [400, 401])