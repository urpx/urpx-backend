from flask_restplus import fields

class ExpenseSerializers():
    def __init__(self, api):
        self.create_expense_dto = api.model("Create Expense DTO", {            
            'description': fields.String(
                description='Description of expense', required=True),
            'amount': fields.Integer(
                description='Amount of expense', required=True),
        })
        
        self.expense_dao = api.inherit("Expense DAO", self.create_expense_dto, {
            'id': fields.Integer(
                description='Id of expense', required=True),
            'created_at': fields.DateTime(
                description='DateTime at created', required=True),
        })
