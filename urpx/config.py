import os
import json

class Config(object):
    SECRET_KEY = os.environ.get('URPX_SECRET', 'secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    API_KEY = os.environ.get('URPX_API_KEY', 'sample')
    ELEVEN_API_KEY = os.environ.get('URPX_ELEVEN_API_KEY', 'simple')
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24 * 30
    JSON_AS_ASCII = False
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300

    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)

        self.API_KEY = config['API_KEY']
        self.ELEVEN_API_KEY = config['ELEVEN_API_KEY']


class DevelopConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/postgres'
