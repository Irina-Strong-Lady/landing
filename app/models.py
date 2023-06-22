from . import db
from datetime import datetime
from sqlalchemy_utils.types.phone_number import PhoneNumberType

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = name = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True)
    phone_number = db.Column(PhoneNumberType(region='RU', max_length=20))
    claims = db.relationship('Claim', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return '<User %r>' % self.email
    
class Claim(db.Model):
    __tablename__ = 'claims'
    id = db.Column(db.Integer, primary_key=True)
    fabula = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, user):
        self.user_id = user.id

    def __repr__(self):
        return '<Claim %r>' % self.id
