from flask_login import current_user
from sqlalchemy import and_, or_

from application.topics.models import *

def get_messages(topic_name):
    if current_user.is_authenticated:
        message_list = Message.query.join(Thread).join(Topic).\
            filter(and_(Topic.name == topic_name, or_(~Thread.secret_users.any(), Thread.secret_users.contains(current_user)))).all()
    else:
        message_list = Message.query.join(Thread).join(Topic).\
            filter(and_(Topic.name == topic_name, ~Thread.secret_users.any())).all()
    return message_list

def get_latest_msg(topic_name):
    if current_user.is_authenticated:
        latest_msg = Message.query.join(Thread).join(Topic).\
            filter(and_(Topic.name == topic_name, or_(~Thread.secret_users.any(), Thread.secret_users.contains(current_user)))).order_by(Message.modified.desc()).first()
    else:
        latest_msg = Message.query.join(Thread).join(Topic).\
            filter(and_(Topic.name == topic_name, ~Thread.secret_users.any())).order_by(Message.modified.desc()).first()
    return latest_msg

def get_threads(topic_name):
    if current_user.is_authenticated:
        thread_list = Thread.query.join(Topic).filter(and_(Topic.name == topic_name,
                                                       or_(~Thread.secret_users.any(), Thread.secret_users.contains(current_user)))).all()
    else:
        thread_list = Thread.query.join(Topic).filter(and_(Topic.name == topic_name, ~Thread.secret_users.any())).all()

    return thread_list