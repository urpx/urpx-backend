from flask_restplus import fields

class UserSerializers():
    def __init__(self, api):
        self.base_user_model = api.model('User Model', {
            'username': fields.String(description='Username of user', required=True),
            'email': fields.String(description='Email of user', required=True),
        })

        self.create_user_dto = api.inherit("Create User DTO", self.base_user_model, {            
            'password': fields.String(description='Password of user', required=True),
        })
        
        self.user_dao = api.inherit("User DAO", self.base_user_model, {
            'id': fields.Integer(description='Id of user', required=True),
            'username': fields.String(description='Username of user', required=True),
            'email': fields.String(description='Email of user', required=True),
            'created_at': fields.DateTime(description='DateTime at created', required=True),
        })
