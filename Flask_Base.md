# Flask 

## Подготовка пространства

```
$ mkdir shop
$ cd shop

$ python3 -m venv venv //Создание виртуального пространства
$ source venv/bin/activate //И его запуск 
$ pip install flask //Установка фласк 

$ pip install flask-sqlalchemy
$ pip install flask-migrate
$ pip install flask-login
$ pip install flask_wtf
pip install wtforms[email]

$ flask db init
$ flask db migrate
$ flask db upgrade


FLASK_APP=shop.py flask shell



kill -9 $(ps -A | grep python | awk '{print $1}')
ps
```

