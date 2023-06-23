import unittest
import re
from app import create_app, db
from flask import url_for

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_index(self):        
        with self.app.test_request_context():
            response = self.client.get(url_for('main.index'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual('/', url_for('main.index'))             
            self.assertTrue('Оставьте Ваш email. С Вами свяжется специалист!' in response.get_data(as_text=True))   
    
    def test_claim(self):        
        with self.app.test_request_context():
            self.client = self.app.test_client(use_cookies=True)
            response = self.client.get(url_for('main.claim_form'))
            self.assertEqual('/claim', url_for('main.claim_form'))             
            self.assertTrue('Пожалуйста, заполните форму!' in response.get_data(as_text=True))
    
    def test_index_page(self):
        # Заполнение формы заявки
        response = self.client.post(url_for('main.get_email'), data={'email': 'john@example.com'})
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('john@example.com', data))
        self.assertTrue('Специалист свяжется с Вами по адресу john@example.com в ближайшее время!' in data)
    
    def test_claim_form_male_user(self):
        # Заполнение формы заявки
        response = self.client.post(url_for('main.claim_form'), data={
            'name': 'Иван',
            'email': 'john@example.com',
            'phone_number': '89001011010',
            'location': 'Краснодар',
            'fabula': 'Привет'
            })
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('Уважаемый Иван! Заявка принята.', data))
        self.assertFalse(re.search('Уважаемая Иван! Заявка принята.', data))
        self.assertFalse(re.search('Пожалуйста, заполните форму!', data))
        
    
    def test_claim_form_female_user(self):
        # Заполнение формы заявки
        response = self.client.post(url_for('main.claim_form'), data={
            'name': 'Ирина',
            'email': 'john@example.com',
            'phone_number': '89001011010',
            'location': 'Краснодар',
            'fabula': 'Привет'
            })
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('Уважаемая Ирина! Заявка принята.', data))
        self.assertFalse(re.search('Уважаемый Ирина! Заявка принята.', data))
        self.assertFalse(re.search('Пожалуйста, заполните форму!', data))

    def test_claim_fill_error(self):        
        response = self.client.post(url_for('main.claim_form'), data={
            # Ошибка при внесении имени (должно состоять из одного слова)
            'name': 'Иван Иванов',
            # Ошибка при внесении email (в тесте венсено без расширения)
            'email': 'john@example',
            # Ошибка при внесении номера телефона (в тесте не хватает последней цифры)
            'phone_number': '8900101101',
            'location': 'Краснодар',
            'fabula': 'Привет'
            })
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('Имя должно содержать только одно слово на кириллице либо латинице', data))
        self.assertTrue(re.search('Формат email не соответствует установленным правилам', data))
        self.assertTrue(re.search('Неверный формат номера', data))
        self.assertTrue(re.search('Пожалуйста, заполните форму!', data))
