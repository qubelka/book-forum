from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import Admin
from flask_admin.menu import MenuLink
from .config import ConfigClass

app = Flask(__name__)
app.config.from_object(ConfigClass)

db = SQLAlchemy(app)
from .models import *
from application.topics.models import Thread, Message, Topic
from application.security.forms import ExtendedRegisterForm

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

# Setup Flask-Admin
from .security.admin import *
admin = Admin(app, index_view=CustomAdminIndexView())
admin.add_view(UserCustomView(User, db.session))
admin.add_view((AdminView(Role, db.session)))
admin.add_view((TopicCustomView(Topic, db.session)))
admin.add_view((ThreadCustomView(Thread, db.session)))
admin.add_view((MessageCustomView(Message, db.session)))
admin.add_link(MenuLink(name='Back to book forum main page', category='', url='/'))

from application.topics.topics_bp import topics
app.register_blueprint(topics, url_prefix='/topics')

from application import routes

from application.commands import create_db

app.cli.add_command(create_db)

def get_not_secret_messages(topic_name):
    message_list = Message.query.join(Thread).join(Topic).\
        filter(and_(~Thread.secret_users.any(), Topic.name == topic_name))
    return message_list

def get_latest_msg(topic_name):
    latest_msg = Message.query.join(Thread).join(Topic).\
        filter(and_(~Thread.secret_users.any(), Topic.name == topic_name)).order_by(Message.modified.desc()).first()
    return latest_msg

def get_not_secret_threads(topic_name):
    thread_list = Thread.query.join(Topic).filter(and_(~Thread.secret_users.any(), Topic.name == topic_name))
    return thread_list

app.jinja_env.globals.update(get_not_secret_messages=get_not_secret_messages, get_latest_msg=get_latest_msg, get_not_secret_threads=get_not_secret_threads)
