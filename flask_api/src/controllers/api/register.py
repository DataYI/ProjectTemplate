from flask_restful import Resource
from flask import make_response, jsonify, current_app
from src.models import User
from .parsers import register_parsers
from src.extensions import parse_args


@parse_args(register_parsers)
class RegisterApi(Resource):
    def post(self):
        # args = register_parsers['POST'].parse_args()
        # print(args)
        args = self.get_args('post')
        username = args['username']
        password = args['password']
        user = User(username)
        user.set_password(password)
        user.add()
        return {'status': 200, 'msg': 'ok'}

    def get(self):
        return {'status': 200, 'msg': 'ok'}