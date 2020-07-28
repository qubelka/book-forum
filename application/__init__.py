from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .config import ConfigClass

app = Flask(__name__)
app.config.from_object(ConfigClass)

db = SQLAlchemy(app)
from .models import *
from application.topics.models import Thread, Message
from application.security.forms import ExtendedRegisterForm

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

# Setup Flask-Admin
admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view((ModelView(Role, db.session)))
admin.add_view((ModelView(Thread, db.session)))
admin.add_view((ModelView(Message, db.session)))

from application.topics.topics_bp import topics
app.register_blueprint(topics, url_prefix='/topics')

from application import routes

''' uncomment to create db tables with test user
@app.before_first_request
def create_user():
    db.drop_all()
    db.create_all()
    user_datastore.create_user(email='user@test.com', password='password', username="user123")
    db.session.commit()
'''
