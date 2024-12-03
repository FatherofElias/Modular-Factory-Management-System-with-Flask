import unittest
from unittest.mock import patch
from app import create_app, db

class TestCustomerEndpoints(unittest.TestCase):

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
        mock_get_all_customers.return_value = [{"id": 1, "name": "Alice"}]
        response = self.client.get('/customers')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"id": 1, "name": "Alice"}])
    
    @patch('controllers.customer_controller.CustomerController.get_customer_by_id')
    def test_get_customer_by_id(self, mock_get_customer_by_id):
        mock_get_customer_by_id.return_value = {"id": 1, "name": "Alice"}
        response = self.client.get('/customers/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": 1, "name": "Alice"})
    
    @patch('controllers.customer_controller.CustomerController.add_customer')
    def test_add_customer(self, mock_add_customer):
        mock_add_customer.return_value = {"id": 1, "name": "Alice"}
        response = self.client.post('/customers', json={"name": "Alice"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"id": 1, "name": "Alice"})

    @patch('controllers.customer_controller.CustomerController.update_customer')
    def test_update_customer(self, mock_update_customer):
        mock_update_customer.return_value = {"id": 1, "name": "Alice Updated"}
        response = self.client.put('/customers/1', json={"name": "Alice Updated"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": 1, "name": "Alice Updated"})

    @patch('controllers.customer_controller.CustomerController.delete_customer')
    def test_delete_customer(self, mock_delete_customer):
        mock_delete_customer.return_value = {"id": 1, "name": "Alice Deleted"}
        response = self.client.delete('/customers/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": 1, "name": "Alice Deleted"})

    @patch('controllers.customer_controller.CustomerController.determine_customer_lifetime_value')
    def test_get_customer_lifetime_value(self, mock_determine_customer_lifetime_value):
        mock_determine_customer_lifetime_value.return_value = {"id": 1, "lifetime_value": 1000}
        response = self.client.get('/customers/lifetime-value?threshold=500')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": 1, "lifetime_value": 1000})

    @patch('controllers.customer_controller.CustomerController.save_customer')
    def test_save_customer(self, mock_save_customer):
        mock_save_customer.return_value = {"message": "Customer saved successfully"}
        response = self.client.post('/customers/save', json={"name": "Alice"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Customer saved successfully"})

if __name__ == '__main__':
    unittest.main()
