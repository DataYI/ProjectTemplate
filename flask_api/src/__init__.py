from flask import Flask
from flask_cors import CORS
from .models import db
from .extensions import bcrypt
from .extensions import logger
from .controllers.api import api_init
from .controllers.apidoc import api_doc_blueprint



def create_app(cfg):
    app = Flask(__name__)
    # app.config.from_object(cfg)
    app.config.update(cfg)
    app.jinja_env.variable_start_string = '{['
    app.jinja_env.variable_end_string = ']}'
    CORS(app, supports_credentials=True, resources=r'/*')
    db.init_app(app)
    bcrypt.init_app(app)
    # login_api.init_app(app)
    # temp_api.init_app(app)
    # 初始化所有api
    api_init(app)
    logger.init_app(app)
    app.register_blueprint(api_doc_blueprint)
    return app
