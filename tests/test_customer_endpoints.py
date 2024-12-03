import unittest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

class TestCustomerEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()

    @patch('controllers.customer_controller.CustomerController.get_all_customers')
    def test_get_all_customers(self, mock_get_all_customers):
        mock_get_all_customers.return_value = []
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    @patch('controllers.customer_controller.CustomerController.add_customer')
    def test_add_customer(self, mock_add_customer):
        mock_add_customer.return_value = {'id': 1, 'name': 'Customer A', 'email': 'customer@example.com', 'phone': '1234567890'}
        response = self.client.post('/customers/', json={'name': 'Customer A', 'email': 'customer@example.com', 'phone': '1234567890'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Customer A')

    @patch('controllers.customer_controller.CustomerController.get_customer_by_id')
    def test_get_customer_not_found(self, mock_get_customer_by_id):
        mock_get_customer_by_id.return_value = None
        response = self.client.get('/customers/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Customer not found')

if __name__ == '__main__':
    unittest.main()
