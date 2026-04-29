def test_create_inventory(self):
    payload = {
        "item_name": "Oil Filter",
        "quantity": 10
    }

    response = self.client.post('/inventory/', json=payload)

   
    self.assertEqual(response.status_code, 401)