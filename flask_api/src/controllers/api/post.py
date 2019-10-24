from flask_restful import Resource
from flask import g, current_app
from src.extensions.authentication import auth
from src.models import Post, User
from src.extensions import parse_args
from .parsers import post_parsers


@parse_args(post_parsers)
class PostApi(Resource):
    @auth.login_required
    def post(self):
        args = self.get_args('post')
        print(args)
        post_ = Post(args['title'], args['text'], g.id, tags=args['tags'])
        if not post_:
            current_app.logger.info('PostApi参数错误！')
            return {'status': 403, 'msg': '文章发布失败！'}
        post_.add()
        return {'status': 200, 'msg': '文章发布成功！'}

    def get(self):
        args = self.get_args('get')
        post_ = Post.get(args['post_id'])
        author = User.get(post_.user_id).username
        post_data = {
            'title': post_.title,
            'text': post_.text,
            'publish_date': post_.publish_date.strftime('%Y-%m-%d %H:%M:%S'),
            'author': author
        }
        print(post_data)
        return {'status': 200, 'msg': '成功', 'post': post_data}

    def put(self):
        pass
