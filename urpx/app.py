from flask import Flask, Blueprint
from flask_restplus import Api

from urpx import common, modules
from urpx.config import Config
from urpx.extensions import bcrypt, cors, db, migrate
from urpx.exceptions import InvalidUsage


def create_app(config=Config):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app, modules.api)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()
    migrate.init_app(app, db)


def register_blueprints(app):
    """Register Flask blueprints."""
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(common.views.blueprint, origins=origins)
    cors.init_app(modules.blueprint, origins=origins)

    app.register_blueprint(common.views.blueprint)
    app.register_blueprint(modules.blueprint)


def register_errorhandlers(app, api):
    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)
    api.errorhandler(InvalidUsage)(errorhandler)
