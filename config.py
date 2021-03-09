import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'salt29'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:www29@localhost/shop_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
