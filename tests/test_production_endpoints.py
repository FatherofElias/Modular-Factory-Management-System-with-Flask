import unittest
from unittest.mock import patch
from datetime import datetime 
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

class TestProductionEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()


    @patch('controllers.production_controller.ProductionController.get_all_productions')
    def test_get_all_productions(self, mock_get_all_productions):
        mock_get_all_productions.return_value = []
        response = self.client.get('/productions/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])



    @patch('controllers.production_controller.ProductionController.add_production')
    def test_add_production(self, mock_add_production):
        mock_add_production.return_value = {
            'id': 1,
            'product_id': 1,
            'employee_id': 1,
            'quantity_produced': 100,
            'date_produced': datetime.strptime('2023-12-01', '%Y-%m-%d').date()
        }
        response = self.client.post('/productions/', json={
            'product_id': 1,
            'employee_id': 1,
            'quantity_produced': 100,
            'date_produced': '2023-12-01'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['quantity_produced'], 100)

    @patch('controllers.production_controller.ProductionController.get_production_by_id')
    def test_get_production_not_found(self, mock_get_production_by_id):
        mock_get_production_by_id.return_value = None
        response = self.client.get('/productions/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Production not found')

if __name__ == '__main__':
    unittest.main()
