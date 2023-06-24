import unittest
from app import create_app, db
from app.models import User

class UserModelTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_valid_email(self):
        u = User(email='example@gmail.com')
        db.session.add(u)
        db.session.commit()       
        self.assertTrue(u.email == 'example@gmail.com')
        self.assertTrue(isinstance(u.id, int))
        self.assertTrue(isinstance(u, User))
        