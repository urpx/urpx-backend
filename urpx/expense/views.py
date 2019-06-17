from flask import request
from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from .models import Expense
from .serializers import ExpenseSerializers
from urpx.exceptions import InvalidUsage
from urpx.extensions import db

api = Namespace('Spend API', description='Spends related operation')
serializers = ExpenseSerializers(api)

auth_parser = api.parser()
auth_parser.add_argument('Authorization', location='headers', 
    required=True, help='Bearer <access_token>')


@api.route('api/expenses')
@api.expect(auth_parser, validate=True)
class ExpensesResource(Resource):
    @jwt_required
    @api.expect(serializers.create_expense_dto, validate=True)
    @api.marshal_with(serializers.expense_dao, code=HTTPStatus.CREATED)
    @api.response(400, 'Invalid expense schema')
    @api.response(422, 'Already registered user')
    def post(self):
        expense_dto = request.get_json()

        expense = Expense(user_id=get_jwt_identity(), 
            amount=expense_dto['amount'], 
            description=expense_dto['description'])
        
        db.session.add(expense)
        db.session.commit()

        return expense, HTTPStatus.CREATED

    @jwt_required
    @api.marshal_list_with(serializers.expense_dao)
    def get(self):
        return Expense.query.filter_by(
            user_id=get_jwt_identity()).all()


@api.route('api/expenses/<expense_id>')
@api.param('expense_id', description='Expense ID')
@api.expect(auth_parser, validate=True)
class ExpenseResource(Resource):
    @jwt_required
    @api.marshal_with(serializers.expense_dao)
    @api.response(HTTPStatus.NOT_FOUND, 'NotFound expense entity')
    def get(self, expense_id):
        expense = Expense.get_by_id(expense_id)
        if expense is None:
            raise InvalidUsage.expense_not_found()

        return expense

    @jwt_required
    @api.expect(serializers.create_expense_dto, validate=True)
    @api.marshal_with(serializers.expense_dao)
    @api.response(HTTPStatus.NOT_FOUND, 'NotFound expense entity')
    def put(self, expense_id):
        expense_dto = request.get_json()

        expense = Expense.get_by_id(expense_id)
        if expense is None:
            raise InvalidUsage.expense_not_found()

        expense.amount = expense_dto['amount']
        expense.description = expense_dto['description']

        db.session.commit()

        return expense

    @jwt_required    
    @api.marshal_with(serializers.expense_dao, code=HTTPStatus.NO_CONTENT)
    @api.response(HTTPStatus.NOT_FOUND, 'NotFound expense entity')
    def delete(self, expense_id):
        expense = Expense.get_by_id(expense_id)
        if expense is None:
            raise InvalidUsage.user_not_found()

        db.session.delete(expense)
        db.session.commit()

        return expense, HTTPStatus.NO_CONTENT



