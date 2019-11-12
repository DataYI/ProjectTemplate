import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from src import create_app, db
from src.models import User, Role, Post, Tag
from src.config import config


ENV = os.environ.get('FLASK_ENV', 'development').lower()

app = create_app(config[ENV])
# app.config.from_mapping(config[ENV])

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('server', Server(host='0.0.0.0'))
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Tag=Tag)


if __name__ == '__main__':
    manager.run()

