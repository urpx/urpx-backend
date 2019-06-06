from flask import Flask
from http import HTTPStatus
from urpx.common.views import blueprint

def test_healthy():
    flask = Flask(__name__)
    flask.config['TESTING'] = True
    flask.config['ENV'] = 'testing'
    flask.register_blueprint(blueprint)

    flask_client = flask.test_client()
    
    res = flask_client.get('api/healthy')

    assert res.status_code == HTTPStatus.OK
