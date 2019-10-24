from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from itsdangerous import SignatureExpired, BadSignature
from datetime import datetime
from .extensions import bcrypt
from .extensions.authentication import serializer

db = SQLAlchemy()


class DbCommitMixIn:
    def session_commit(self):
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            reason = str(e)
            current_app.logger.error(reason)
            return reason

    @classmethod
    def get(cls, id):
        return cls.query.filter_by(id=id).first()

    def add(self):
        db.session.add(self)
        return self.session_commit()

    def update(self):
        return self.session_commit()

    def delete(self):
        self.query.filter_by(id=self.id).delete()
        return self.session_commit()


role_users = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

tag_posts = db.Table(
    'tag_posts',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id', ondelete='CASCADE')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'))
)


class User(db.Model, DbCommitMixIn):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    login_time = db.Column(db.Integer)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    roles = db.relationship(
        'Role',
        secondary=role_users,
        backref=db.backref('users', lazy='dynamic')
    )

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password.encode('utf-8'))

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def generate_auth_token(self, expiration=2 * 60 * 60):
        s = serializer(expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            return user

    @staticmethod
    def verify_auth_token(token):
        s = serializer()
        try:
            data = s.loads(token)
        except(SignatureExpired, BadSignature):
            return None
        user = User.query.get(data['id'])
        return user


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class Post(db.Model, DbCommitMixIn):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    publish_date = db.Column(db.DateTime, default=datetime.now)
    # 多对多，文章与标签的对应
    tags = db.relationship(
        'Tag',
        secondary=tag_posts,
        backref=db.backref('post', lazy='dynamic')
        # lazy='dynamic',
        # cascade='all, delete',
        # passive_deletes=True
    )

    def __init__(self, title, text, user_id, tags=[], publish_date=None):
        self.title = title
        self.text = text
        self.user_id = user_id
        # self.tags = tags
        self.add_tags(tags)
        if not publish_date:
            self.publish_date = publish_date

    def __repr__(self):
        return "<Post '{}'>".format(self.title)

    def add_tags(self, tags):
        tags = [Tag(t) for t in tags]
        self.tags.extend(tags)
        return self.session_commit()


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    posts = db.relationship(
        'Post',
        secondary=tag_posts,
        backref=db.backref('tag', lazy='dynamic')
    )

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Tag '{}'>".format(self.title)
