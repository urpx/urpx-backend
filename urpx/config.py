import os

class Config(object):
    SECRET_KEY = os.environ.get('URPX_SECRET', 'secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']