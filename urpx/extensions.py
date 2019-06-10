from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
