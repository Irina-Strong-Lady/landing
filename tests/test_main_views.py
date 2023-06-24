import unittest
from app import create_app
from flask import url_for
from app.models import User

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)
        
    def tearDown(self):
        self.app_context.pop()
    
    def test_index(self):        
        with self.app.test_request_context():
            response = self.client.get(url_for('main.index'))
            self.assertEqual('/', url_for('main.index'))                         
            self.assertTrue('Оставьте Ваш email. С Вами свяжется специалист!' in response.get_data(as_text=True))   
                        
    def test_index_email(self):
        u = User()        
        with self.app.test_request_context():
            self.client = self.app.test_client(use_cookies=True)
            response = self.client.get(url_for('main.get_email'))
            self.assertEqual('/email', url_for('main.get_email'))             
            self.assertNotIn('Банкротство юридических лиц', response.get_data(as_text=True))
            self.assertTrue(hasattr(u, 'email'))
            self.assertTrue(hasattr(u, 'name'))
            