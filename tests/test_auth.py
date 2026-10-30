import unittest
from app import app
from models.database import db, User
from werkzeug.security import generate_password_hash

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_register_page(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
    
    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
    
    def test_protected_route_redirect(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)  # Redirect to login

if __name__ == '__main__':
    unittest.main()
