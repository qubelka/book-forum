from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from .config import ConfigClass
from application.topics.topics_bp import topics

app = Flask(__name__)
app.config.from_object(ConfigClass)
app.register_blueprint(topics, url_prefix='/topics')

db = SQLAlchemy(app)
from .models import *
from application.security.forms import ExtendedRegisterForm

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

from application import routes
from application.topics import models

''' uncomment to create db tables with test user
@app.before_first_request
def create_user():
    db.drop_all()
    db.create_all()
    user_datastore.create_user(email='user@test.com', password='password', username="user123")
    db.session.commit()
'''