from flask import request
from flask_restplus import Resource, Namespace
from flask_jwt_extended import create_access_token

from urpx.user.models import User
from urpx.exceptions import InvalidUsage
from .serializers import AuthSerializers

api = Namespace('Auth API', description='Auth related operation')
serializers = AuthSerializers(api)


@api.route('api/auth/login')
class AuthResource(Resource):
    @api.expect(serializers.login_dto, validate=True)
    @api.marshal_with(serializers.token_info_dto)
    @api.response(404, 'Not authorized info')
    def post(self):
        login_dto = request.get_json()

        user = User.query.filter_by(email=login_dto['email']).first()
        if user is not None and user.check_password(login_dto['password']):
            token = create_access_token(identity=user.id, fresh=True)
            return {
                'access_token': token
            }
        else:
            raise InvalidUsage.user_not_found()
