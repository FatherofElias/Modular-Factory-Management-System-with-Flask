import unittest
from unittest.mock import patch
from test_app import create_app, db

class TestEmployeeEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('TestingConfig')
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()
    
    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('controllers.employee_controller.EmployeeController.get_all_employees')
    def test_get_all_employees(self, mock_get_all_employees):
        mock_get_all_employees.return_value = [{"id": 1, "name": "John Doe"}]
        response = self.client.get('/employees')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"id": 1, "name": "John Doe"}])
    
    @patch('controllers.employee_controller.EmployeeController.get_employee_by_id')
    def test_get_employee_by_id(self, mock_get_employee_by_id):
        mock_get_employee_by_id.return_value = {"id": 1, "name": "John Doe"}
        response = self.client.get('/employees/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": 1, "name": "John Doe"})
    
    @patch('controllers.employee_controller.EmployeeController.add_employee')
    def test_add_employee(self, mock_add_employee):
        mock_add_employee.return_value = {"id": 1, "name": "John Doe"}
        response = self.client.post('/employees', json={"name": "John Doe"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"id": 1, "name": "John Doe"})

    @patch('controllers.employee_controller.EmployeeController.update_employee')
    def test_update_employee(self, mock_update_employee):
        mock_update_employee.return_value = {"id": 1, "name": "John Doe Updated"}
        response = self.client.put('/employees/1', json={"name": "John Doe Updated"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": 1, "name": "John Doe Updated"})

    @patch('controllers.employee_controller.EmployeeController.delete_employee')
    def test_delete_employee(self, mock_delete_employee):
        mock_delete_employee.return_value = {"id": 1, "name": "John Doe Deleted"}
        response = self.client.delete('/employees/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": 1, "name": "John Doe Deleted"})

    @patch('controllers.employee_controller.EmployeeController.analyze_employee_performance')
    def test_get_employee_performance(self, mock_analyze_employee_performance):
        mock_analyze_employee_performance.return_value = {"performance": "excellent"}
        response = self.client.get('/employees/performance')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"performance": "excellent"})

    @patch('controllers.employee_controller.EmployeeController.save_employee')
    def test_save_employee(self, mock_save_employee):
        mock_save_employee.return_value = {"message": "Employee saved successfully"}
        response = self.client.post('/employees/save', json={"name": "John Doe"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Employee saved successfully"})

if __name__ == '__main__':
    unittest.main()
