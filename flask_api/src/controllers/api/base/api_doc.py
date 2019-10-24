import inspect
import traceback
from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass
from functools import update_wrapper
from typing import List, Callable
import colorama

from flask import request, Response, current_app
from werkzeug.routing import Rule


from src.controllers.api.base.errors import ApiError
from src.controllers.api.base.reply_base import json_response, ReplyBase




def length(length_able) -> int:
    if length_able is None:
        return 0
    return len(length_able)


def not_default_arg(arg_index: int, arg_spec: inspect.FullArgSpec) -> bool:
    # 非默认值的参数数量
    offset = length(arg_spec.args) - length(arg_spec.defaults)
    return arg_index - offset < 0


def fullname_of_func(func) -> str:
    return '%s.%s' % (func.__module__, func.__qualname__)


def is_json_api_func(func: Callable) -> bool:
    """
    判断是否是标注为 api 接口的 rule, 并且返回的是 json (ReplyBase)
    """

    if hasattr(func, '__original__fun__'):
        return_cls = inspect.getfullargspec(func.__original__fun__).annotations.get('return', None)
        if return_cls:
            return issubclass(return_cls, ReplyBase)
    return False







def web_api(func):
    """
    json_api 装饰器, 它应该处于 flask route 装饰器的下面, 并且应该是控制器方法上最近的一个包装器
    :param func: 被装饰器所包装的函数方法
    :return: 返回包装后的函数方法
    """

    def wrapper(*args, **kwargs):
        is_return_json = False
        try:          
            func_return = func(*args, **kwargs)

            if isinstance(func_return, ReplyBase):
                is_return_json = True
                return json_response(func_return)
            elif isinstance(func_return, Response):
                func_return.headers['Access-Control-Allow-Origin'] = '*'
                return func_return
            elif isinstance(func_return, str):
                response = Response(func_return, content_type='text/plain; charset=utf-8')
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            
        except ApiError as e:
            reply = ReplyBase(e.err_code, e.err_msg)
            reply.traceback = traceback.format_exc()
            return json_response(reply)
        except BaseException as e:
            if is_return_json:
                reply = ReplyBase(-1, str(e))
                reply.traceback = traceback.format_exc()
                return json_response(reply)
            else:
                # logger().error(colorama.Fore.RED + traceback.format_exc())
                raise e

    wrapper.__original__fun__ = func
    return update_wrapper(wrapper, func)


@dataclass
class WebApiArg:
    # 参数名称
    name: str = ''
    # 参数位置索引
    index: int = 0
    # 参数是否有默认值
    has_default: bool = False
    # 参数的默认值
    default = None
    # 参数的类型描述
    type_desc: str = '开发人员很懒,没有标注参数的类型,鄙视他吧👎'


@dataclass
class WebApiDoc:
    path: str = ''
    func_module_name: str = ''
    func_qualified_name: str = ''
    func_full_name: str = ''
    comment: str = ''
    doc: str = '开发人员很懒,没有留下文档说明,鄙视他吧👎'
    has_doc: bool = False
    brief: str = '' # first line of doc
    is_support_get: bool = False
    is_support_post: bool = False
    args: List[WebApiArg] = None
    retrun_json: bool = True

    def load(self, rule: Rule):
        self.path = rule.rule
        func = current_app.view_functions[rule.endpoint]
        self.func_module_name = func.__module__
        self.func_qualified_name = func.__qualname__
        self.func_full_name = fullname_of_func(func)
        self.comments = inspect.getcomments(func)
        self.retrun_json = is_json_api_func(func)
        self.doc = inspect.getdoc(func) if inspect.getdoc(func) else '\n'
        self.brief = self.doc.splitlines()[0]
        self.is_support_get = 'GET' in rule.methods
        self.is_support_post = 'POST' in rule.methods
        self.args = []

        if hasattr(func, '__original__func__'):
            arg_spec = inspect.getfullargspec(func.__original__func__)
        else:
            arg_spec =inspect.getfullargspec(func)
        offset = length(arg_spec.args) - length(arg_spec.defaults)
        for arg_index, arg_name in enumerate(arg_spec.args):
            if arg_name == 'self':
                continue
            arg = WebApiArg()
            arg.name = arg_name
            arg.index = arg_index
            arg.has_default = arg_index - offset >= 0
            arg.type_desc = arg_spec.annotations[arg_name].__name__

            if arg.has_default:
                default_v = arg_spec.defaults[arg_index - offset]
                arg_type = arg_spec.annotations[arg_name]
                if arg_type == str:
                    arg.default = '"%s"' % default_v
                elif arg_type == datetime:
                    arg.default = default_v.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    arg.default = str(default_v)
            self.args.append(arg)
        return self
        

def is_web_api_func(rule: Rule) -> bool:
    func = current_app.view_functions[rule.endpoint]
    return hasattr(func, '__original__fun__')


def all_web_api() -> List[WebApiDoc]:
    rules = filter(is_web_api_func, current_app.url_map.iter_rules())
    return [WebApiDoc().load(rule) for rule in rules]
