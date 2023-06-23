import unittest
from app import create_app, db
from app.models import User, Claim
from datetime import datetime
from sqlalchemy_utils.types.phone_number import PhoneNumberType

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

    def test_claim_init(self):
        user = User(id=1)
        claim = Claim(user)
        db.session.add(claim)
        db.session.flush()
        self.assertEqual(claim.user_id, 1)
        self.assertNotEqual(claim.timestamp, datetime.utcnow())
        self.assertTrue(claim.timestamp, str)
        self.assertTrue(claim.timestamp, datetime)
    
    def test_unique_user_id(self):
        user1 = User()
        user2 = User()
        db.session.add(user1)
        db.session.add(user2)
        db.session.flush()
        self.assertNotEqual(user1.id, user2.id)
    
    def test_user_phone(self):
        user = User(phone_number='89001010010')
        db.session.add(user)
        db.session.flush()
        self.assertTrue(user.phone_number, str)
        self.assertTrue(user.phone_number, PhoneNumberType)

