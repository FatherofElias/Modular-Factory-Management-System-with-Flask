import unittest
from unittest.mock import patch
from models.customer import Customer
from models.order import Order
from app import create_app, db
from controllers.customer_controller import CustomerController

class TestCustomerController(unittest.TestCase):

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

    @patch('controllers.customer_controller.CustomerController.get_all_customers')
    def test_get_all_customers(self, mock_get_all_customers):
        mock_get_all_customers.return_value = [Customer(id=1, name="Alice", email="alice@example.com", phone="1234567890")]
        customers = CustomerController.get_all_customers()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].name, "Alice")
    
    @patch('controllers.customer_controller.CustomerController.get_customer_by_id')
    def test_get_customer_by_id(self, mock_get_customer_by_id):
        mock_get_customer_by_id.return_value = Customer(id=1, name="Alice", email="alice@example.com", phone="1234567890")
        customer = CustomerController.get_customer_by_id(1)
        self.assertIsNotNone(customer)
        self.assertEqual(customer.name, "Alice")
    
    @patch('controllers.customer_controller.CustomerController.add_customer')
    def test_add_customer(self, mock_add_customer):
        mock_add_customer.return_value = Customer(id=1, name="Alice", email="alice@example.com", phone="1234567890")
        data = {"name": "Alice", "email": "alice@example.com", "phone": "1234567890"}
        customer = CustomerController.add_customer(data)
        self.assertIsNotNone(customer)
        self.assertEqual(customer.name, "Alice")

    @patch('controllers.customer_controller.CustomerController.update_customer')
    def test_update_customer(self, mock_update_customer):
        mock_update_customer.return_value = Customer(id=1, name="Alice Updated", email="alice@example.com", phone="1234567890")
        data = {"name": "Alice Updated", "email": "alice@example.com", "phone": "1234567890"}
        customer = CustomerController.update_customer(1, data)
        self.assertIsNotNone(customer)
        self.assertEqual(customer.name, "Alice Updated")

    @patch('controllers.customer_controller.CustomerController.delete_customer')
    def test_delete_customer(self, mock_delete_customer):
        mock_delete_customer.return_value = Customer(id=1, name="Alice Deleted", email="alice@example.com", phone="1234567890")
        customer = CustomerController.delete_customer(1)
        self.assertIsNotNone(customer)
        self.assertEqual(customer.name, "Alice Deleted")
    
    @patch('controllers.customer_controller.CustomerController.save_customer')
    def test_save_customer(self, mock_save_customer):
        mock_save_customer.return_value = {"message": "Customer saved successfully"}
        data = {"name": "Alice", "email": "alice@example.com", "phone": "1234567890"}
        response = CustomerController.save_customer(data)
        self.assertEqual(response["message"], "Customer saved successfully")

    @patch('controllers.customer_controller.CustomerController.determine_customer_lifetime_value')
    def test_determine_customer_lifetime_value(self, mock_determine_customer_lifetime_value):
        mock_determine_customer_lifetime_value.return_value = [
            {"customer_name": "Alice", "total_order_value": 1000}
        ]
        threshold = 500
        lifetime_value_data = CustomerController.determine_customer_lifetime_value(threshold)
        self.assertEqual(len(lifetime_value_data), 1)
        self.assertEqual(lifetime_value_data[0]["customer_name"], "Alice")
        self.assertEqual(lifetime_value_data[0]["total_order_value"], 1000)

if __name__ == '__main__':
    unittest.main()
