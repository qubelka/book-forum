from flask_security import UserMixin, RoleMixin
from datetime import datetime
from application import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

secret_threads_users = db.Table('secret_threads_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('thread_id', db.Integer(), db.ForeignKey('thread.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Role: {self.name}, id: {self.id}>'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    joined = db.Column(db.DateTime, default=datetime.now())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    created_threads = db.relationship('Thread', backref='creator', lazy=True)
    secret_threads = db.relationship('Thread', secondary=secret_threads_users, backref=db.backref('secret_users', lazy=True))
    messages = db.relationship('Message', backref='user', lazy=True)

    def __repr__(self):
        return f'<User: {self.username}, id: {self.id}>'
