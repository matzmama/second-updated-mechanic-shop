import unittest
from application import create_app
from application.extensions import db

class TestCustomers(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True

        with self.app.app_context():
            db.drop_all()
            db.create_all()

        self.client = self.app.test_client()

    # ✅ GET
    def test_get_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)

    # ✅ POST (valid)
    def test_create_customer(self):
        payload = {
            "name": "John Doe",
            "email": "john@email.com",
            "password": "123"
        }

        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)

    # ❌ NEGATIVE TEST
    def test_invalid_customer(self):
        payload = {
            "name": "John Doe"
        }

        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()