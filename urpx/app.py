from flask import Flask
from .common.views import blueprint as common_blueprint

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    register_blueprints(app)

    return app

def register_blueprints(app):
    app.register_blueprint(common_blueprint)
