from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange, optional
from app.models import User, Item, Category

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AddCat(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('descriptione')
    submit = SubmitField('Add')
    
    def validate_name(self, name):
        cat = Category.query.filter_by(name=name.data).first()
        if cat is not None:
            raise ValidationError('This category is already exist')

class UpdateCat(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    submit = SubmitField('Update')

class DeleteCat(FlaskForm):
    name = StringField('Name')
    submit = SubmitField('Delete')

    def validate_name(self, name):
        name = Category.query.filter_by(name=name.data).first()
        if name is None:
            raise ValidationError('This category do not exist')


class AddItem(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('description')
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=1)]) 
    quantities = IntegerField('Quantities', validators=[NumberRange(min=0)])
    category = StringField('Category', validators=[DataRequired()])
    img = StringField('Image')
    submit = SubmitField('Add') 

    def validate_name(self, name):
        name = Category.query.filter_by(name=name.data).first()
        if name is not None:
            raise ValidationError('This category is already exist')

    def validate_category(self, category):
        cat = Category.query.filter_by(name=category.data).first()
        if cat is None:
            raise ValidationError('This category do not exist')



class UpdateItem(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('description')
    price = FloatField('Price', validators=[optional()]) 
    quantities = IntegerField('Quantities', validators=[optional()])
    category = StringField('Category')
    img = StringField('Image')
    submit = SubmitField('Update')

    def validate_price(self, price):
        if price.data is not None:
            if price.data < 0:
                raise ValidationError('Enter number >= 0')
    
    def validate_quantities(self, quantities):
        if quantities.data is not None:
            if quantities.data < 0:
                raise ValidationError('Enter number >= 0')

    def validate_name(self, name):
        name = Item.query.filter_by(name=name.data).first()
        if name is None:
            raise ValidationError('This item do not exist')
        

class DeleteItem(FlaskForm):
    name = StringField('Name')
    submit = SubmitField('Delete')

    def validate_name(self, name):
        name = Item.query.filter_by(name=name.data).first()
        if name is None:
            raise ValidationError('This item do not exist')