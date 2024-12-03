import unittest
from unittest.mock import patch

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db


class TestEmployeeEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()
    
    @patch('controllers.employee_controller.EmployeeController.get_all_employees')
    def test_get_all_employees(self, mock_get_all_employees):
        mock_get_all_employees.return_value = []
        response = self.client.get('/employees/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    @patch('controllers.employee_controller.EmployeeController.add_employee')
    def test_add_employee(self, mock_add_employee):
        mock_add_employee.return_value = {'id': 1, 'name': 'John Doe', 'position': 'Manager'}
        response = self.client.post('/employees/', json={'name': 'John Doe', 'position': 'Manager'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'John Doe')

    @patch('controllers.employee_controller.EmployeeController.get_employee_by_id')
    def test_get_employee_not_found(self, mock_get_employee_by_id):
        mock_get_employee_by_id.return_value = None
        response = self.client.get('/employees/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Employee not found')


if __name__ == '__main__':
    unittest.main()
