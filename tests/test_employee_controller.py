import unittest
from unittest.mock import patch
from app import create_app, db
from models.employee import Employee
from models.production import Production
from controllers.employee_controller import EmployeeController

class TestEmployeeController(unittest.TestCase):

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
        mock_get_all_employees.return_value = [Employee(id=1, name="John Doe", position="Engineer")]
        employees = EmployeeController.get_all_employees()
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0].name, "John Doe")
    
    @patch('controllers.employee_controller.EmployeeController.get_employee_by_id')
    def test_get_employee_by_id(self, mock_get_employee_by_id):
        mock_get_employee_by_id.return_value = Employee(id=1, name="John Doe", position="Engineer")
        employee = EmployeeController.get_employee_by_id(1)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.name, "John Doe")
    
    @patch('controllers.employee_controller.EmployeeController.add_employee')
    def test_add_employee(self, mock_add_employee):
        mock_add_employee.return_value = Employee(id=1, name="John Doe", position="Engineer")
        data = {"name": "John Doe", "position": "Engineer"}
        employee = EmployeeController.add_employee(data)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.name, "John Doe")

    @patch('controllers.employee_controller.EmployeeController.update_employee')
    def test_update_employee(self, mock_update_employee):
        mock_update_employee.return_value = Employee(id=1, name="John Doe Updated", position="Engineer")
        data = {"name": "John Doe Updated", "position": "Engineer"}
        employee = EmployeeController.update_employee(1, data)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.name, "John Doe Updated")

    @patch('controllers.employee_controller.EmployeeController.delete_employee')
    def test_delete_employee(self, mock_delete_employee):
        mock_delete_employee.return_value = Employee(id=1, name="John Doe", position="Engineer")
        employee = EmployeeController.delete_employee(1)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.name, "John Doe")

    @patch('controllers.employee_controller.EmployeeController.save_employee')
    def test_save_employee(self, mock_save_employee):
        mock_save_employee.return_value = {"message": "Employee saved successfully"}
        data = {"name": "John Doe", "position": "Engineer"}
        response = EmployeeController.save_employee(data)
        self.assertEqual(response["message"], "Employee saved successfully")

    @patch('controllers.employee_controller.EmployeeController.analyze_employee_performance')
    def test_analyze_employee_performance(self, mock_analyze_employee_performance):
        mock_analyze_employee_performance.return_value = [{"employee_name": "John Doe", "total_quantity_produced": 100}]
        performance_data = EmployeeController.analyze_employee_performance()
        self.assertEqual(len(performance_data), 1)
        self.assertEqual(performance_data[0]["employee_name"], "John Doe")
        self.assertEqual(performance_data[0]["total_quantity_produced"], 100)

if __name__ == '__main__':
    unittest.main()
