import unittest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db


class TestProductEndpoints(unittest.TestCase):
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

    @patch('controllers.product_controller.ProductController.get_paginated_products')
    def test_get_products(self, mock_get_paginated_products):
        mock_get_paginated_products.return_value.items = []
        response = self.client.get('/products/?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    @patch('controllers.product_controller.ProductController.add_product')
    def test_add_product(self, mock_add_product):
        mock_add_product.return_value = {'id': 1, 'name': 'Product A', 'price': 100.0}
        response = self.client.post('/products/', json={'name': 'Product A', 'price': 100.0})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Product A')

    @patch('controllers.product_controller.ProductController.get_product_by_id')
    def test_get_product_not_found(self, mock_get_product_by_id):
        mock_get_product_by_id.return_value = None
        response = self.client.get('/products/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Product not found')

if __name__ == '__main__':
    unittest.main()

