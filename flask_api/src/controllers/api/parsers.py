from flask_restful import reqparse
import yaml

with open('./src/controllers/api/api_conf.yaml', 'r', encoding='utf-8') as f:
    api_config = yaml.load(f, Loader=yaml.FullLoader)
    # api_config = yaml.load(f)


def parser_api(cfg: dict) -> dict:
    def get_parser(d):
        if not d:
            return None
        args = d['args']
        p = reqparse.RequestParser()
        for k, v in args.items():
            v['type'] = eval(v['type'])
            p.add_argument(k, **v)
        return p
    parsers = {k: get_parser(v) for k, v in cfg['methods'].items()}
    return parsers


# 下面是不同接口参数解析器的字典，相同接口不同请求方法的解析器，使用方法名作为键值来获取
# 如登录接口的POST方法参数解析器为login_parsers['POST']

# 注册接口
register_parsers = parser_api(api_config['Register'])
# 登录接口
login_parsers = parser_api(api_config['Login'])
# 临时接口
temp_parsers = parser_api(api_config['Temp'])
# post（文章）接口
post_parsers = parser_api(api_config['Post'])

# print(api_config['Register'])


