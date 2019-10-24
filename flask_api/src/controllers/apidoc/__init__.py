from flask_restful.reqparse import Argument
from flask_restful import Api, Resource
from typing import List
from flask import Blueprint, current_app, jsonify, request, render_template


from src.controllers.api import api_list


api_doc_blueprint = Blueprint('api_doc', __name__, template_folder='templates')


@api_doc_blueprint.route('/api-doc/list/')
def api_doc_list():
    d = api_list_desc_method(api_list)
    # return jsonify(d)
    print(d)
    return render_template('ApiList.html', url_list=d)


@api_doc_blueprint.route('/api-doc/all/')
def api_doc_all():
    base_url = '127.0.0.1:5000'
    d = api_list_desc(api_list)
    return jsonify(d)


@api_doc_blueprint.route('/api-doc/view/<string:method>/')
def view(method: str):
    """
    根据url和method返回对应的参数描述
    """
    # base_url = '127.0.0.1:5000'
    url = request.args.get('url')
    # print(args)
    d = api_list_desc(api_list)
    try:
        args_m = d[url]
    except KeyError:
        return 'url不存在'
    try:
        args = [{'name': k, **v} for k, v in args_m[method.upper()].items()]
        return render_template('TestPost.html', args=args)
    except KeyError:
        return 'url没有对应的%s方法' % method.upper() 



@api_doc_blueprint.route('/api-doc/view/test/<string:method>/')
def view_test(method):
    url_map = list(current_app.url_map.iter_rules())
    endpoint = parse_rule(url_map[1])
    # print(dir(url_map))
    func = current_app.view_functions[endpoint]
    print(func)
    return 'ok'






def arg_desc(arg: Argument) -> dict:
    """
    描述参数的字典
    """
    d = {
        'type': str(arg.type).split("'")[1],
        'required': arg.required,
        'default': arg.default,
        'nullable': arg.nullable,
        'help': arg.help
    }
    return d


def resource_args_desc(resource: Resource) -> dict:
    """
    解析Resource对象，得到url和对应的参数描述
    """
    _class, url, _ = resource
    d = {}
    for method, parser in  _class.request_parser.items():
        d[method] = {arg.name: arg_desc(arg) for arg in parser.args}
    # return {'url': url[0], 'methods': d}
    return {url[0]: d}


def api_list_desc(api_list: List[Api]) -> dict:
    """
    返回api_list中所有api下的所有url及其支持的方法，方法下还有对应路由需要的请求参数描述
    :return: url字符串为key，value为嵌套字典（方法为key，参数描述字典为value）
    """
    d = {}
    for api in api_list:
        resources = api.resources
        for r in resources:
            d = {**d, **resource_args_desc(r)}
    return d 


def api_list_desc_method(api_list: List[Api]) -> dict:
    """
    返回api_list中所有api下的所有url及其支持的方法， 只解析到方法
    :return: url字符串为key，方法字符串组成的列表为value
    """
    urls_desc = []
    for api in api_list:
        resources = api.resources
        for resource in resources:
            _class, url, _ = resource
            d = {}
            d['url'] = url[0]
            d['description'] = '没有说明，自己想办法，告辞！'
            d['methods'] = list(_class.request_parser.keys())
            urls_desc.append(d)
        
    return urls_desc



def find_args(url: str, method: str) -> dict:
    """
    通过url和method找到对应的api参数说明
    """
    pass


def parse_rule(rule):
    methods = rule.methods
    return rule.endpoint