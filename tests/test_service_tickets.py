import unittest
from application import create_app
from application.extensions import db

class TestServiceTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True

        with self.app.app_context():
            db.drop_all()
            db.create_all()

        self.client = self.app.test_client()

       def test_get_service_tickets(self):
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 401)

       def test_create_service_ticket(self):
        payload = {
            "description": "Oil change",
            "status": "Open"
        }

        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()