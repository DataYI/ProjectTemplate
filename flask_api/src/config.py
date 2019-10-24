import yaml

with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


# class Config:
#     # SECRET_KEY = '5a8e43810ef2d0de40e5f4b86d791f6c'
#     # REFRESH_TIME = 60 * 60
#     SECRET_KEY = config['base']['SECRET_KEY']
#     REFRESH_TIME = config['base']['REFRESH_TIME']
#
#
# class ProConfig(Config):
#     pass
#
#
# class DevConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1qaz@WSX@39.104.168.95:3308/ashadow'
#     SQLALCHEMY_ECHO = False
#     # 默认为True，会追踪对象的修改并发送信号，需要额外的内存
#     SQLALCHEMY_TRACK_MODIFICATIONS = True
#     # amqp协议默认使用librabbitmq，如果没安装librabbitmq则使用pyamqp
#     CELERY_BROKER_URL = 'amqp://admin:rabbit123@39.104.168.95:5672//'
#     CELERY_BACKEND = 'amqp://admin:rabbit123@39.104.168.95:5672//'
#     HOST = '0.0.0.0'
#     PORT = 5000
