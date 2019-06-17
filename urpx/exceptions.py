from flask import jsonify


def template(data, code=500):
    return {'message': {'errors': {'body': data}}, 'status_code': code}


UNAUTHORIZED_TOKEN = template(['Unauthorized token'], code=401)
USER_NOT_FOUND = template(['User not found'], code=404)
USER_ALREADY_REGISTERED = template(['User already registered'], code=422)
UNKNOWN_ERROR = template([], code=500)


class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = self.message
        return jsonify(rv)

    @classmethod
    def unauthorized_token(cls):
        return cls(**UNAUTHORIZED_TOKEN)

    @classmethod
    def user_not_found(cls):
        return cls(**USER_NOT_FOUND)

    @classmethod
    def user_already_registered(cls):
        return cls(**USER_ALREADY_REGISTERED)

    @classmethod
    def unknown_error(cls):
        return cls(**UNKNOWN_ERROR)