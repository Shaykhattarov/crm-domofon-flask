from app import db
from flask_login import UserMixin



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=False, unique=False)
    address_id = db.Column(db.Integer, db.ForeignKey('user_address.id'))
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'))

    def __repr__(self):
        return '<User {}>'.format(self.name)
    


class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.value)
    



