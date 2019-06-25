from flask import request
from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from .models import Request
from .serializers import RequestSerializers
from urpx.exceptions import InvalidUsage
from urpx.extensions import db

api = Namespace('Request API', description='Request related operation')
serializers = RequestSerializers(api)

auth_parser = api.parser()
auth_parser.add_argument('Authorization', location='headers', 
    required=True, help='Bearer <access_token>')

@api.route('api/request')
@api.expect(auth_parser, validate=True)
class RequestsResource(Resource):
    @jwt_required
    @api.expect(serializers.create_request_dto, validate=True)
    @api.marshal_with(serializers.request_dao, code=HTTPStatus.CREATED)
    @api.response(400, 'Invalid request schema')
    @api.response(422, 'Invalid access token')
    def post(self):
        request_dto = request.get_json()

        req = Request(user_id=get_jwt_identity(),
            product_name=request_dto['product_name'],
            company=request_dto['company'],
            belongto=request_dto['belongto'])
        
        db.session.add(req)
        db.session.commit()

        return req, HTTPStatus.CREATED

    @jwt_required
    @api.marshal_list_with(serializers.request_dao)
    def get(self):
        return Request.query.order_by(
            Request.created_at.desc()).all()


@api.route('api/request/<request_id>')
@api.param('request_id', description='Request ID')
@api.expect(auth_parser, validate=True)
class RequestResource(Resource):
    @jwt_required    
    @api.marshal_with(serializers.request_dao, code=HTTPStatus.NO_CONTENT)
    @api.response(HTTPStatus.NOT_FOUND, 'NotFound request entity')
    def delete(self, request_id):
        request = Request.get_by_id(request_id)
        if request is None:
            raise InvalidUsage.user_not_found()

        db.session.delete(request)
        db.session.commit()

        return request, HTTPStatus.NO_CONTENT