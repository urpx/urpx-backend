from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

from urpx.auth.jwt import identity_loader

jwt = JWTManager()
jwt.user_identity_loader(identity_loader)