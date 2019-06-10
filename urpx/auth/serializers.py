from flask_restplus import fields

class AuthSerializers():
    def __init__(self, api):
        self.login_dto = api.model("Login DTO", {
            'email': fields.String(description='Email of user', required=True),
            'password': fields.String(description='Password of user', required=True),
        })

        self.token_info_dto = api.model("Token Info DTO", {
            'access_token': fields.String(description='AccessToken', required=True),
        })
