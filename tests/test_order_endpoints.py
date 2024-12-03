import unittest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db



class TestOrderEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        with self.app_context:
            db.create_all() 

    def tearDown(self):
        with self.app_context:
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    @patch('controllers.order_controller.OrderController.get_paginated_orders')
    def test_get_orders(self, mock_get_paginated_orders):
        mock_get_paginated_orders.return_value.items = []
        response = self.client.get('/orders/?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    @patch('controllers.order_controller.OrderController.add_order')
    def test_add_order(self, mock_add_order):
        mock_add_order.return_value = {
            'id': 1, 'customer_id': 1, 'product_id': 1, 
            'quantity': 10, 'total_price': 100.0
        }
        response = self.client.post('/orders/', json={
            'customer_id': 1,
            'product_id': 1,
            'quantity': 10,
            'total_price': 100.0
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['total_price'], 100.0)

    @patch('controllers.order_controller.OrderController.get_order_by_id')
    def test_get_order_not_found(self, mock_get_order_by_id):
        mock_get_order_by_id.return_value = None
        response = self.client.get('/orders/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Order not found')

if __name__ == '__main__':
    unittest.main()
