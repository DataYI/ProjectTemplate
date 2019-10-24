from flask_restful import Api
from .login import LoginApi
from .temp import TempApi
from .post import PostApi
from .register import RegisterApi

register_api = Api()
login_api = Api()
temp_api = Api()
post_api = Api()

register_api.add_resource(RegisterApi, '/api/register/')
login_api.add_resource(LoginApi, '/api/login/')
temp_api.add_resource(TempApi, '/api/temp/')
post_api.add_resource(PostApi, '/api/post/')

api_list = [login_api, temp_api, post_api, register_api]
api_class_list = []

def api_init(app):
    for api in api_list:
        api.init_app(app)


# print(dir(temp_api))
# print(temp_api.resources)