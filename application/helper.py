from flask_login import current_user
from sqlalchemy import and_

from application.topics.models import *

def get_messages(topic_name):
    message_list = Message.query.join(Thread).join(Topic). \
        filter(and_(Topic.name == topic_name, ~Thread.secret_users.any())).all()

    if current_user.is_authenticated:
        secret_messages_with_access = Message.query.join(Thread).join(Topic).\
            filter(and_(Topic.name == topic_name, Thread.secret_users.contains(current_user))).all()
        message_list.extend(secret_messages_with_access)

    return message_list

def get_latest_msg(topic_name):
    latest_msg = Message.query.join(Thread).join(Topic). \
        filter(and_(Topic.name == topic_name, ~Thread.secret_users.any())).order_by(Message.modified.desc()).first()

    if current_user.is_authenticated:
        latest_secret_msg = Message.query.join(Thread).join(Topic).\
            filter(and_(Topic.name == topic_name, Thread.secret_users.contains(current_user))).order_by(Message.modified.desc()).first()

        if latest_secret_msg and latest_msg:
            if latest_secret_msg.modified > latest_msg.modified:
                latest_msg = latest_secret_msg

    return latest_msg

def get_threads(topic_name):
    thread_list = Thread.query.join(Topic).filter(and_(Topic.name == topic_name, ~Thread.secret_users.any())).all()

    if current_user.is_authenticated:
        secret_with_access = Thread.query.join(Topic).filter(and_(Topic.name == topic_name, Thread.secret_users.contains(current_user))).all()
        thread_list.extend(secret_with_access)

    return thread_list