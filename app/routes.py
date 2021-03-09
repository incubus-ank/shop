from flask import render_template, flash, redirect, url_for
from flask import request

from app import app
from app.forms import LoginForm

from flask_login import current_user, login_user
from flask_login import logout_user
from app.models import User, Item, Category
from flask_login import login_required
from werkzeug.urls import url_parse

from app import db
from app.forms import RegistrationForm, AddItem, UpdateItem, DeleteItem, AddCat, UpdateCat, DeleteCat


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
    return render_template('register.html', form=form)


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

@app.route('/items/<item>')
@login_required
def item(item):
    item = Item.query.filter_by(id=int(item)).first_or_404()
    print(item.name)
    return render_template('item.html', item=item)

@app.route('/category/<cat>/')
@login_required
def cat_items(cat):
    page = request.args.get('page', 1, type=int)
    cat_items = Item.query.filter_by(category=str(cat)).paginate(page, 10, False)
    next_url = url_for('cat_items', page=cat_items.next_num, cat=cat) \
        if cat_items.has_next else None
    prev_url = url_for('cat_items', page=cat_items.prev_num, cat=cat) \
        if cat_items.has_prev else None
    return render_template('items.html', items=cat_items.items, page=page, next_url=next_url, prev_url=prev_url)

@app.route('/category')
@login_required
def category():
    cats = Category.query.all()
    return render_template('category.html', cats=cats)


@app.route('/items/add', methods=['GET', 'POST'])
def add_item():
    form = AddItem()
    if form.validate_on_submit():
        item = Item(name=form.name.data, description=form.description.data, price=form.price.data, quantities=form.quantities.data, category=form.category.data)
        db.session.add(item)
        db.session.commit()
        flash('Товар добавлен')
        return redirect(url_for('items'))
    return render_template('man_item.html', form=form, act='Добавление Товара')

@app.route('/items/update', methods=['GET', 'POST'])
def update_item():
    form = UpdateItem()
    if form.validate_on_submit():
        item = Item.query.filter_by(name=form.name.data).first()
        print (item.id)
        if form.description.data is not None:
            item.description = form.description.data
            print(item.description)
        if form.price.data is not None:
            item.price = form.price.data
        if form.quantities.data is not None:
            item.quantities = form.quantities.data
        if form.category.data != '':
            item.category = form.category.data
        db.session.add(item)
        db.session.commit()
        flash('Товар изменен')
        return redirect(url_for('items'))
    return render_template('man_item.html', form=form, act='Изменение Товара')

@app.route('/items/delete', methods=['GET', 'POST'])
def delete_item():
    form = DeleteItem()
    if form.validate_on_submit():
        Item.query.filter_by(name=form.name.data).delete()
        db.session.commit()
        flash('Товар удален')
        return redirect(url_for('items'))
    return render_template('delete.html', form=form, act='Удаление Товара')

@app.route('/category/add', methods=['GET', 'POST'])
def add_category():
    form = AddCat()
    if form.validate_on_submit():
        cat = Category(name=form.name.data, description=form.description.data)
        db.session.add(cat)
        db.session.commit()
        flash('Категория добавлена')
        return redirect(url_for('category'))
    return render_template('man_cat.html', form=form, act='Добавлена Категория')

@app.route('/category/update', methods=['GET', 'POST'])
def update_category():
    form = UpdateCat()
    if form.validate_on_submit():
        cat = Category.query.filter_by(name=form.name.data).first()
        cat.description = form.description.data
        db.session.add(cat)
        db.session.commit()
        flash('Категория изменен')
        return redirect(url_for('category'))
    return render_template('man_cat.html', form=form, act='Изменение Категории')

@app.route('/category/delete', methods=['GET', 'POST'])
def delete_category():
    form = DeleteCat()
    if form.validate_on_submit():
        Category.query.filter_by(name=form.name.data).delete()
        db.session.commit()
        flash('Категория удалена')
        return redirect(url_for('category'))
    return render_template('delete.html', form=form, act='Удаление Категории')

@app.route('/manage/<est>')
def manage(est):
        return render_template('manage.html',est=est)
        

# @app.route('/test')
# def test():
#     return render_template('test.html')
