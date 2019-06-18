from flask_restplus import fields

class RequestSerializers():
    def __init__(self, api):
        self.create_request_dto = api.model("Create Request DTO", {            
            'product_name': fields.String(
                description='Name of product', required=True),
            'company': fields.String(
                description='company of product', required=True),
            'belongto': fields.String(
                description='Belong to user', required=True),
        })
        
        self.request_dao = api.inherit("Request DAO", 
            self.create_request_dto, {
                'id': fields.Integer(
                    description='Id of request', required=True),
                'created_at': fields.DateTime(
                    description='DateTime at created', required=True),
            }
        )
