from flask import Flask
from urpx import common
from urpx.config import Config
from urpx.extensions import bcrypt, cors, db, migrate

def create_app(config=Config):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    """Register Flask blueprints."""
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(common.views.blueprint, origins=origins)

    app.register_blueprint(common.views.blueprint)
