import unittest
from app import create_app, db
from models.user import User

class TestUserModel(unittest.TestCase):

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

    def test_set_password(self):
        user = User(username='testuser', role='user')
        user.set_password('password123')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.check_password('wrongpassword'))
    
    def test_check_password(self):
        user = User(username='testuser', role='user')
        user.set_password('password123')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.check_password('password321'))

if __name__ == '__main__':
    unittest.main()
