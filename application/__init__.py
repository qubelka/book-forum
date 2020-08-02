from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import Admin
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

from application.topics.topics_bp import topics
app.register_blueprint(topics, url_prefix='/topics')

from application import routes

from application.commands import create_db

app.cli.add_command(create_db)
