from app import db
from app import login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import insert 
from sqlalchemy import event


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
    name = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=True)
    items = db.relationship('Item', backref='cat', lazy='dynamic')

    def __repr__(self):
        return "{" + "'name': {}, 'description': {} },".format(self.name, self.description)

    def get_count_item(self):
        return db.session.query(db.func.sum(Item.quantities)).filter_by(category=self.name).scalar()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantities = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(30), db.ForeignKey('category.name', ondelete='CASCADE'))
    img = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return "{ 'name': {}, 'description': {}, 'price': {}, 'quantities': {}, 'category': {} },".format(self.name, self.description, self.price, self.quantities, self.category)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    quantities_old = db.Column(db.Integer, nullable=False)
    quantities_next = db.Column(db.Integer, nullable=False)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# @event.listens_for(Item, 'before_insert',retval=True)
# def item_before_insert(mapper, connection, target):
#     print(mapper)
#     item = Item.query.filter_by(id=target.id).first()
#     print(item.quantities)
#     print(target.quantities)






