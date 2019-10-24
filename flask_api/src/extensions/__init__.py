from functools import wraps
from celery import Celery
from flask_bcrypt import Bcrypt
from flask_restful import Resource

from .log import Logger
# from src.controllers.api import api_class_list


bcrypt = Bcrypt()
celery = Celery()
logger = Logger()


# 类装饰器
def parse_args(request_parser: dict) -> object:
    def wrapper(_class):
        _class.request_parser = request_parser
        def get_args(self, method: str, *args, **kwargs):
            """
            :param method: http请求方法
            :return: 请求参数构成的字典
            """
            method = method.upper()
            return self.request_parser[method].parse_args(*args, **kwargs)
        _class.get_args = get_args
        # api_class_list.append(_class)
        return _class
    return wrapper
