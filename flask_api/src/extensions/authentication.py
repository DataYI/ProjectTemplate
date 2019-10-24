from functools import wraps
from flask import current_app, make_response, request, jsonify, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import (
    TimedJSONWebSignatureSerializer,
    JSONWebSignatureSerializer,
    BadHeader,
    SignatureExpired,
    BadSignature
)


class Serializer(TimedJSONWebSignatureSerializer):
    def make_header(self, header_fields):
        """
        dumps生成token时会调用此函数
        :param header_fields: 默认为空
        :return: 一个存入了部分信息的字典
        """
        header = JSONWebSignatureSerializer.make_header(self, header_fields)
        iat = self.now()
        exp = iat + self.expires_in
        # 刷新时间由配置文件配置，默认1小时，刷新时间应该小于过期时间
        refresh_exp = iat + current_app.config.get('REFRESH_TIME', 3600)
        header['iat'] = iat
        header['exp'] = exp
        header['refresh_exp'] = refresh_exp
        return header

    def loads(self, s, salt=None, return_header=False):
        payload, header = JSONWebSignatureSerializer.loads(
            self, s, salt, return_header=True
        )
        # 生成新token
        new_token = None

        if 'exp' not in header:
            raise BadSignature('Missing expiry date', payload=payload)

        int_date_error = BadHeader('Expiry date is not an IntDate', payload=payload)
        try:
            header['exp'] = int(header['exp'])
        except ValueError:
            raise int_date_error
        if header['exp'] < 0:
            raise int_date_error

        if header['refresh_exp'] < self.now():
            # 超过了刷新时间，抛出异常
            if header['exp'] < self.now():
                raise SignatureExpired(
                    'Signature expired',
                    payload=payload,
                    date_signed=self.get_issue_date(header),
                )
            # 还在可刷新时间内，生成新的token
            else:
                ser = Serializer(current_app.config['SECRET_KEY'], expires_in=self.expires_in)
                new_token = ser.dumps(payload)
        if return_header:
            return payload, new_token, header
        return payload, new_token


# token过期时间为24小时
def serializer(expiration=24*60*60):
    key = current_app.config['SECRET_KEY']
    return Serializer(key, expires_in=expiration)


class Auth(HTTPTokenAuth):
    def authenticate(self, auth):
        if auth:
            token = auth['token']
        else:
            token = ""
        if self.verify_token_callback:
            return self.verify_token_callback(token)
        return False,

    def login_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # 获取请求中的Authorization
            auth = self.get_auth()
            # token过期但没超过刷新时间时，返回新token
            new_token = None
            # Flask normally handles OPTIONS requests on its own, but in the
            # case it is configured to forward those to the application, we
            # need to ignore authentication headers and let the request through
            # to avoid unwanted interactions with CORS.
            if request.method != 'OPTIONS':  # pragma: no cover
                # authenticate调用通过verify_token注册的回调函数验证token
                # others降低了包含new_toekn,还有可能包含header，取决于回调函数
                is_authorization, *others = self.authenticate(auth)
                if not is_authorization:
                    # Clear TCP receive buffer of any pending data
                    request.data
                    return self.auth_error_callback()
                new_token = others[0]
            if new_token:
                resp = make_response(f(*args, **kwargs))
                resp.headers['Authorization'] = new_token
                resp.headers['Access-Control-Expose-Headers'] = 'Authorization'
                return resp
            return f(*args, **kwargs)
        return decorated


auth = Auth(scheme='Bearer')


# token验证函数
@auth.verify_token
def verify_token(token):
    g.id = None
    try:
        payload, new_token = serializer().loads(token)
    except(SignatureExpired, BadSignature):
        return False,
    if 'id' in payload:
        g.id = payload['id']
        return True, new_token
    return False,


@auth.error_handler
def auth_error():
    resp = make_response(jsonify({'status': 401, 'msg': 'token无效'}))
    return resp
