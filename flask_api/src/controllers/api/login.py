from flask_restful import Resource
from flask import make_response, jsonify, current_app
from src.models import User
from .parsers import login_parsers
from src.extensions import parse_args


@parse_args(login_parsers)
class LoginApi(Resource):
    def post(self):
        # args = login_parsers['POST'].parse_args()
        args = self.get_args('post')
        user = User.authenticate(args['username'], args['password'])
        if user:
            resp_json = jsonify({'status': '200',
                                 'msg': 'ok',
                                 'token': user.generate_auth_token()})
            resp = make_response(resp_json, 200)
            if args['remembered']:
                resp.headers['Authorization'] = user.generate_auth_token(
                    7 * 24 * 60 * 60)
            else:
                resp.headers['Authorization'] = user.generate_auth_token(
                    2 * 60 * 60)
            resp.headers['Access-Control-Expose-Headers'] = 'Authorization'
            return resp
        else:
            current_app.logger.info('test')
            return {'status': 403, 'message': '用户名或密码错误'}
