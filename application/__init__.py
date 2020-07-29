from flask import Flask
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
from .security.admin import AdminView, CustomAdminIndexView
admin = Admin(app, index_view=CustomAdminIndexView())
admin.add_view(AdminView(User, db.session))
admin.add_view((AdminView(Role, db.session)))
admin.add_view((AdminView(Thread, db.session)))
admin.add_view((AdminView(Message, db.session)))
admin.add_view((AdminView(Topic, db.session)))

from application.topics.topics_bp import topics
app.register_blueprint(topics, url_prefix='/topics')

from application import routes

''' uncomment to create db tables with test user and some pre-defined topics
@app.before_first_request
def create_user():
    db.drop_all()
    db.create_all()

    user_datastore.create_user(email='user@test.com', password='password', username="user")
    admin = user_datastore.create_user(email='admin@test.com', password='password', username="admin")
    role = user_datastore.create_role(name='admin', description='user with administrative privileges')
    admin.roles.append(role)

    bestsellers = Topic(name='Bestsellers', description='Discussions about best-selling books')
    new_releases = Topic(name='New Releases', description='Discussions about upcoming book releases')
    what_to_read = Topic(name='What Should I Read Next?', description='Discussions about reading suggestions')
    authors = Topic(name='Authors', description='Discussions about book authors')

    db.session.add_all([bestsellers, new_releases, what_to_read, authors])
    db.session.commit()
'''


