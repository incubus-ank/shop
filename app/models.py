from app import db
from app import login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'Пользователь: {}'.format(self.username)    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    items = db.relationship('Item', backref='cat', lazy='dynamic')

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(550), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantities = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return "{" + "'name': {}, 'description': {}, 'price': {}, 'quantities': {}, 'category': {} },".format(self.name, self.description, self.price, self.quantities, self.category)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quantities_old = db.Column(db.Integer, nullable=False)
    quantities_old = db.Column(db.Integer, nullable=False)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))




