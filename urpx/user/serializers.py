from flask_restplus import fields

class UserSerializers():
    def __init__(self, api):
        self.create_user_dto = api.model("Create User DTO", {            
            'username': fields.String(description='Username of user', required=True),
            'email': fields.String(description='Email of user', required=True),
            'password': fields.String(description='Password of user', required=True),
        })
        
        self.user_dao = api.inherit("User DAO", self.create_user_dto, {
            'id': fields.Integer(description='Id of user', required=True),
            'username': fields.String(description='Username of user', required=True),
            'email': fields.String(description='Email of user', required=True),
            'created_at': fields.DateTime(description='DateTime at created', required=True),
        })
