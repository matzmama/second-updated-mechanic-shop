# 🔒 POST (protected → expect 401)
def test_create_inventory(self):
    payload = {
        "item_name": "Oil Filter",
        "quantity": 10
    }

    response = self.client.post('/inventory/', json=payload)

    # ✅ EXPECT 401 because route is protected
    self.assertEqual(response.status_code, 401)