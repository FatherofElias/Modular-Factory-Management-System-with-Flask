import unittest
from unittest.mock import patch
from app import create_app, db

class TestProductionEndpoints(unittest.TestCase):

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

    @patch('controllers.production_controller.ProductionController.get_all_productions')
    def test_get_productions(self, mock_get_all_productions):
        mock_get_all_productions.return_value = [
            {"id": 1, "product_id": 1, "employee_id": 1, "quantity_produced": 100, "date_produced": "2023-12-01"}
        ]
        response = self.client.get('/productions')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"id": 1, "product_id": 1, "employee_id": 1, "quantity_produced": 100, "date_produced": "2023-12-01"}
        ])
    
    @patch('controllers.production_controller.ProductionController.get_production_by_id')
    def test_get_production(self, mock_get_production_by_id):
        mock_get_production_by_id.return_value = {"id": 1, "product_id": 1, "employee_id": 1, "quantity_produced": 100, "date_produced": "2023-12-01"}
        response = self.client.get('/productions/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": 1, "product_id": 1, "employee_id": 1, "quantity_produced": 100, "date_produced": "2023-12-01"})
    
    @patch('controllers.production_controller.ProductionController.add_production')
    def test_add_production(self, mock_add_production):
        mock_add_production.return_value = {"id": 1, "product_id": 1, "employee_id": 1, "quantity_produced": 100, "date_produced": "2023-12-01"}
        response = self.client.post('/productions', json={"product_id": 1, "employee_id": 1, "quantity_produced": 100, "date_produced": "2023-12-01"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"id": 1, "product_id": 1, "employee_id": 1, "quantity_produced": 100, "date_produced": "2023-12-01"})
    
    @patch('controllers.production_controller.ProductionController.update_production')
    def test_update_production(self, mock_update_production):
        mock_update_production.return_value = {"id": 1, "product_id": 1, "employee_id": 1, "quantity_produced": 150, "date_produced": "2023-12-01"}
        response = self.client.put('/productions/1', json={"product_id": 1, "employee_id": 1, "quantity_produced": 150, "date_produced": "2023-12-01"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": 1, "product_id": 1, "employee_id": 1, "quantity_produced": 150, "date_produced": "2023-12-01"})

    @patch('controllers.production_controller.ProductionController.delete_production')
    def test_delete_production(self, mock_delete_production):
        mock_delete_production.return_value = {"id": 1, "product_id": 1, "employee_id": 1, "quantity_produced": 100, "date_produced": "2023-12-01"}
        response = self.client.delete('/productions/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": 1, "product_id": 1, "employee_id": 1, "quantity_produced": 100, "date_produced": "2023-12-01"})
    
    @patch('controllers.production_controller.ProductionController.evaluate_production_efficiency')
    def test_get_production_efficiency(self, mock_evaluate_production_efficiency):
        mock_evaluate_production_efficiency.return_value = [{"product_name": "Widget", "total_quantity_produced": 100}]
        response = self.client.get('/productions/efficiency/2023-12-01')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"product_name": "Widget", "total_quantity_produced": 100}])
    
    @patch('controllers.production_controller.ProductionController.save_production')
    def test_save_production(self, mock_save_production):
        mock_save_production.return_value = {"message": "Production saved successfully"}
        response = self.client.post('/productions/save', json={"product_id": 1, "employee_id": 1, "quantity_produced": 100, "date_produced": "2023-12-01"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Production saved successfully"})

if __name__ == '__main__':
    unittest.main()
