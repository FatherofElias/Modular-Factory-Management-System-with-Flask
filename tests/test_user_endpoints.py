import unittest
from unittest.mock import patch
from app import create_app, db
from models.user import User

class TestUserEndpoints(unittest.TestCase):

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

    @patch('models.user.User.query')
    def test_register(self, mock_query):
        mock_query.filter_by.return_value.first.return_value = None
        data = {"username": "testuser", "password": "password123", "role": "user"}
        response = self.client.post('/users/register', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "User created successfully"})
    
    @patch('models.user.User.query')
    def test_login(self, mock_query):
        user = User(username="testuser", role="user")
        user.set_password("password123")
        mock_query.filter_by.return_value.first.return_value = user
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post('/users/login', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json)
    
    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('flask_jwt_extended.view_decorators.get_jwt_identity')
    def test_me(self, mock_get_jwt_identity, mock_verify_jwt_in_request):
        mock_get_jwt_identity.return_value = {"username": "testuser", "role": "user"}
        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"username": "testuser", "role": "user"})

if __name__ == '__main__':
    unittest.main()
