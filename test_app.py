import unittest
from application import create_app

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()

    def test_sum(self):
        payload = {'num1': 2, 'num2': 3}
        response = self.app.post('/sum', json=payload)
        data = response.get_json()
        self.assertEqual(data['result'], 5)

    def test_subtract(self):
        payload = {'num1': 5, 'num2': 3}
        response = self.app.post('/subtract', json=payload)
        data = response.get_json()
        self.assertEqual(data['result'], 2)

    def test_multiply(self):
        payload = {'num1': 4, 'num2': 3}
        response = self.app.post('/multiply', json=payload)
        data = response.get_json()
        self.assertEqual(data['result'], 12)

    def test_divide(self):
        payload = {'num1': 10, 'num2': 2}
        response = self.app.post('/divide', json=payload)
        data = response.get_json()
        self.assertEqual(data['result'], 5)

if __name__ == '__main__':
    unittest.main()