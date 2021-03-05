from flask import render_template, flash, redirect, url_for
from flask import request

from app import app
from app.forms import LoginForm

from flask_login import current_user, login_user
from flask_login import logout_user
from app.models import User, Item
from flask_login import login_required
from werkzeug.urls import url_parse

from app import db
from app.forms import RegistrationForm

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title = 'Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы зарегистрированы. Войдите в систему')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/items/')
def items():
    page = request.args.get('page', 1, type=int)
    items = Item.query.paginate(page, 10, False)
    #items = Item.query.all()
    next_url = url_for('items', page=items.next_num) \
        if items.has_next else None
    prev_url = url_for('items', page=items.prev_num) \
        if items.has_prev else None
    return render_template('items.html', items=items.items, page=page, next_url=next_url, prev_url=prev_url)
