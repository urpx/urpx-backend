from flask import Blueprint
from flask_restplus import Api

from urpx import user

blueprint = Blueprint('api', __name__)
api = Api(blueprint, version='v0.1', title='URPX API', 
    description='The urpx api')
api.add_namespace(user.views.api, path='/')