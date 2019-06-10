from flask import Blueprint, request
from flask_restplus import Resource, Namespace
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus

from urpx.exceptions import InvalidUsage
from urpx.extensions import db
from .models import User
from .serializers import UserSerializers

api = Namespace('User API', description='Users related operation')
serializers = UserSerializers(api)

@api.route('api/users')
class UsersResource(Resource):
    @api.expect(serializers.create_user_dto)
    @api.marshal_with(serializers.user_dao, code=HTTPStatus.CREATED)
    @api.response(400, 'Invalid user schema')
    @api.response(422, 'Already registered user')
    def post(self):
        user_dto = request.get_json()
        user = User(user_dto['username'], user_dto['email'], 
            password=user_dto['password'])
        
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            raise InvalidUsage.user_already_registered()

        return user, HTTPStatus.CREATED

    @api.marshal_list_with(serializers.user_dao)
    def get(self):
        return User.query.all()


@api.route('api/users/<user_id>')
@api.param('user_id', description='User ID')
class UserResource(Resource):
    @api.marshal_with(serializers.user_dao)
    @api.response(404, 'Notfound user entity')
    def get(self, user_id):
        user = User.get_by_id(user_id)
        if user is None:
            raise InvalidUsage.user_not_found()

        return user

