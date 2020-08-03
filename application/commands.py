import click
from flask.cli import with_appcontext

from application import db, user_datastore
from application.topics.models import Topic

@click.command(name="create_db")
@with_appcontext
def create_db():
    db.drop_all()
    db.create_all()

    user_datastore.create_user(email='user@test.com', password='password', username='user')
    admin = user_datastore.create_user(email='admin@test.com', password='password', username='admin')
    role = user_datastore.create_role(name='admin', description='user with administrative privileges')
    admin.roles.append(role)

    bestsellers = Topic(name='Bestsellers', description='Discussions about best-selling books')
    new_releases = Topic(name='New Releases', description='Discussions about upcoming book releases')
    what_to_read = Topic(name='What Should I Read Next?', description='Discussions about reading suggestions')
    authors = Topic(name='Authors', description='Discussions about book authors')

    db.session.add_all([bestsellers, new_releases, what_to_read, authors])
    db.session.commit()