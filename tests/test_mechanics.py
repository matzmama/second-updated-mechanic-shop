import unittest
from application import create_app
from application.extensions import db

class TestMechanics(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True

        with self.app.app_context():
            db.drop_all()
            db.create_all()

        self.client = self.app.test_client()

    def test_get_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)

    def test_create_mechanic(self):
        payload = {
            "name": "John",
            "specialty": "Engine"
        }

        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()