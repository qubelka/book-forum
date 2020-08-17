from flask import Blueprint, render_template, flash, url_for, redirect, request, abort
from flask_login import current_user
from flask_security import login_required
from sqlalchemy import and_
from .models import Message, Thread, Topic

from .forms import ThreadForm, MsgForm
from ..models import User
from .. import db

topics = Blueprint('topics', __name__)

@topics.route('/<topic_slug>/add_thread', methods=['GET', 'POST'])
@login_required
def add_thread(topic_slug):
    topic = Topic.query.filter(Topic.slug == topic_slug).first()
    if not topic:
        abort(404)

    thread_form = ThreadForm()
    thread_form.users.choices = [(user.id, user.username) for user in User.query.filter(and_(User.active == True, User.id != current_user.id)).all()]
    msg_form = MsgForm()

    if thread_form.validate_on_submit() and msg_form.validate_on_submit():
        name = thread_form.name.data
        body = msg_form.body.data
        secret_thread_users = []
        secret_thread_user_objects = []

        if thread_form.checkbox.data:
            secret_thread_users = request.form.getlist('secret_thread_users')
            if secret_thread_users:
                for id in secret_thread_users:
                    user = User.query.filter(User.id == id).first()
                    secret_thread_user_objects.append(user)

            secret_thread_user_objects.append(current_user)

        thread = Thread(name=name, topic_id=topic.id, creator_id=current_user.id)

        try:
            if thread_form.checkbox.data:
                thread.secret_users.extend(secret_thread_user_objects)
            db.session.add(thread)
            db.session.flush()
            message = Message(body=body, thread_id=thread.id, creator_id=current_user.id)
            db.session.add(message)
            db.session.commit()
        except:
            flash('Something went wrong while trying to add the object to the database. Please try again later.', category='warning')

        return redirect(url_for('topics.show_thread', topic_slug=topic_slug, thread_slug=thread.slug))

    return render_template('topics/new_thread.html', thread_form=thread_form, msg_form=msg_form, topic_slug=topic_slug)

@topics.route('/<topic_slug>/<thread_slug>', methods=['GET', 'POST'])
def show_thread(topic_slug, thread_slug):
    thread = Thread.query.filter(Thread.slug == thread_slug).first()
    topic = Topic.query.filter(Topic.slug == topic_slug).first()

    if thread and topic:
        if thread.secret_users and (current_user not in thread.secret_users):
            abort(404)
    else:
        abort(404)

    form = MsgForm()
    page = request.args.get('page', 1, type=int)
    messages = Message.query.filter(Message.thread_id == thread.id).paginate(page=page, per_page=5)

    if form.validate_on_submit():
        body = form.body.data
        try:
            message = Message(body=body, thread_id=thread.id, creator_id=current_user.id)
            db.session.add(message)
            db.session.commit()
        except:
            flash('Something went wrong while trying to add the object to the database. Please try again later.', category='warning')

        updated_message_list = Message.query.filter(Message.thread_id == thread.id).paginate(page=page, per_page=5)
        return redirect(url_for('topics.show_thread', topic_slug=topic_slug, thread_slug=thread_slug, page=updated_message_list.pages))

    return render_template('topics/show_thread.html', thread=thread, topic=topic, messages=messages, form=form)

@topics.route('/')
def index():
    return render_template('index.html')

@topics.route('/<topic_slug>')
def topic_page(topic_slug):
    topic_obj = Topic.query.filter(Topic.slug == topic_slug).first()

    if not topic_obj:
        flash(f'Topic \'{topic_slug}\' does not exist.', category='warning')
        return redirect(url_for('index'))

    return render_template('topics/topic.html', topic=topic_obj)

@topics.route('/<topic_slug>/<thread_slug>/<msg_slug>/delete', methods=['GET', 'POST'])
@login_required
def delete_msg(topic_slug, thread_slug, msg_slug):
    topic = Topic.query.filter(Topic.slug == topic_slug).first()
    thread = Thread.query.filter(Thread.slug == thread_slug).first()
    msg = Message.query.filter(Message.slug == msg_slug)

    if topic and thread and msg.first():
        if current_user.id != msg[0].creator_id:
            abort(404)
    else:
        abort(404)

    page = request.args.get('page', 1, type=int)
    if request.method == 'GET':
        return render_template('topics/delete_message.html', topic_slug=topic_slug, thread_slug=thread_slug, msg_slug=msg_slug, page=page)

    msg.delete()
    db.session.commit()
    flash('The message has been successfully deleted.', category='success')

    updated_message_list = Message.query.filter(Message.thread_id == thread.id).paginate(page=1, per_page=5)

    if (page > updated_message_list.pages) and (updated_message_list.pages != 0):
        page = updated_message_list.pages

    return redirect(url_for('topics.show_thread', topic_slug=topic_slug, thread_slug=thread_slug, page=page))

@topics.route('/<topic_slug>/<thread_slug>/<msg_slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_msg(topic_slug, thread_slug, msg_slug):
    topic = Topic.query.filter(Topic.slug == topic_slug).first()
    thread = Thread.query.filter(Thread.slug == thread_slug).first()
    msg = Message.query.filter(Message.slug==msg_slug).first()

    if topic and thread and msg:
        if current_user.id != msg.creator_id:
            abort(404)
    else:
        abort(404)

    if request.method == 'GET':
        form = MsgForm(obj=msg)

        return render_template('topics/edit_message.html', form=form, topic_slug=topic_slug, thread_slug=thread_slug, msg_slug=msg_slug)

    form = MsgForm(formdata=request.form, obj=msg)
    form.populate_obj(msg)
    db.session.commit()
    flash('The message has been successfully edited.', category='success')

    updated_message_list = Message.query.filter(Message.thread_id == thread.id).paginate(page=1, per_page=5)
    return redirect(url_for('topics.show_thread', topic_slug=topic_slug, thread_slug=thread_slug, page=updated_message_list.pages))
