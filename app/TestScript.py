from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app import routes, db
from app.models import Item, Category

def TestDate():
    engine = create_engine('sqlite:///app.db')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    d1 = '''RedmiBook Ryzen Edition 14 это ноутбук, который подходит не только для повседневного серфинга 
    в интернете, но также и для продолжительных сеансах в современных высокопроизводительных играх.'''

    d2 = '''Xiaomi Redmi G Gaming Laptop это игровой ноутбук с современным дизайном, 
    экраном диагональю 16", производительным процессором семейства Intel 10-ого поколения и 
    игровой видеокартой от Nvidia.'''

    d3 = '''Xiaomi RedmiBook 16 представляет собой уникальный ноутбук от ведущего производителя 
    техники. Устройство оснащено дисплеем FHD диагональю 16.1 дюймов с разрешением 1920×1080. 
    Благодаря тонким рамкам, дисплей занимает 90 % площади всей фронтальной поверхности и 
    обладает большим углом обзора 178 градусов.'''

    i1 = Item(name='RedmiBook Ryzen Edition 14', description=d1, price=57990.00, quantities=3, category='1')
    i2 = Item(name='Redmi G Laptop', description=d2, price=86990.00, quantities=3, category='1')
    i3 = Item(name='RedmiBook 16', description=d3, price=67990.00, quantities=3, category='1')

    i13 = Category(name='notebook', description='ноутбуки, современные и мобильные копмьютеры.', )

    session.add(i1)
    session.add(i2)
    session.add(i3)
    session.add(i13)

    session.commit()
