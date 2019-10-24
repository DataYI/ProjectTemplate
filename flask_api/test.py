# import requests

# url = 'http://127.0.0.1:5000/api/register/'

# res = requests.post(url, data={'username': 'test', 'password': 'test'})
# print(res.json())


# insert into post (title, text, user_id, publish_date) values ('测试文章', '恭喜发财，happy new year!', 1, now());


from src.controllers.api.parsers import temp_parsers

for arg in temp_parsers.get('POST').args:
    print(arg.name)
    break


[
    'alias', 'arguments', 'bind', 'build', 'build_compare_key', 'build_only', 'compile', 'defaults', 'empty', 'endpoint', 'get_converter', 'get_empty_kwargs', 'get_rules', 'host', 'is_leaf',
    'map', 'match', 'match_compare_key', 'methods', 'provide_automatic_options', 'provides_defaults_for', 'redirect_to', 'refresh', 'rule', 'strict_slashes', 'subdomain', 'suitable_for']


