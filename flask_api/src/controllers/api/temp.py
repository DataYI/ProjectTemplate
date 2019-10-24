from flask_restful import Resource, reqparse, request
from flask import g, current_app
from src.extensions.authentication import auth
# from .parsers import temp_parsers
from src.extensions import parse_args


cfg = {
    'GET': {
        'username': {'type': str, 'required': False, 'help': '用户名'}, 
        'password': {'type': str, 'required': False, 'help': '密码'}
    },
    'POST': {
        'f1': {'type': str, 'required': True, 'help': 'f1'},
        'f2': {'type': str, 'required': True, 'help': 'f2'}
    }
}

def parser_api(cfg: dict) -> dict:
    def get_parser(args):
        if not args:
            return None
        p = reqparse.RequestParser()
        for k, v in args.items():
            # v['type'] = eval(v['type'])
            p.add_argument(k, **v)
        return p
    parsers = {k: get_parser(v) for k, v in cfg.items()}
    return parsers

temp_parsers = parser_api(cfg)

@parse_args(temp_parsers)
class TempApi(Resource):

    def get(self):
        args = self.get_args('get')
        # args = request.args
        # print(args)

        return {'Hello': 'world'}

    @auth.login_required
    def post(self):
        # args = temp_parsers['POST'].parse_args(strict=True)
        args = self.get_args('post', strict=True)
        f1 = args['f1']
        f2 = args['f2']
        print(args)
        return {
            'f1': f1,
            'f2': f2,
            'id': g.id
        }
