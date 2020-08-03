from flask import Blueprint, render_template, flash, url_for, redirect, request, abort
from flask_login import current_user
from flask_security import login_required
from .models import Message, Thread, Topic

from .forms import ThreadForm, MsgForm
from ..models import User
from .. import db

topics = Blueprint('topics', __name__)

@topics.route("/<topic_slug>/add_thread", methods=["GET", "POST"])
@login_required
def add_thread(topic_slug):
    form = ThreadForm()
    form.users.choices = [(user.id, user.username) for user in User.query.filter((User.active == True) or (User.id != current_user.id)).all()]

    if form.validate_on_submit():
        name = form.name.data
        topic = Topic.query.filter(Topic.slug == topic_slug).first()
        secret_thread_users = []
        secret_thread_user_objects = []

        if form.checkbox.data == True:
            secret_thread_users = request.form.getlist('secret_thread_users')
            if secret_thread_users:
                for id in secret_thread_users:
                    user = User.query.filter(User.id == id).first()
                    secret_thread_user_objects.append(user)

            secret_thread_user_objects.append(current_user)

        try:
            thread = Thread(name=name, topic_id=topic.id, creator_id=current_user.id)
            if form.checkbox.data == True:
                thread.secret_users.extend(secret_thread_user_objects)
            db.session.add(thread)
            db.session.commit()

        except:
            flash('Something went wrong while trying to add the object to the database.', category='warning')

        return redirect(url_for('topics.topic_page', topic_slug=topic_slug))

    return render_template("topics/new_thread.html", form=form, topic_slug=topic_slug)

@topics.route("/<topic_slug>/<thread_slug>/add_message", methods=["GET", "POST"])
@login_required
def add_message(topic_slug, thread_slug):
    thread = Thread.query.filter(Thread.slug == thread_slug).first()

    if thread.secret_users and (current_user not in thread.secret_users):
        abort(404)

    form = MsgForm()

    if form.validate_on_submit():
        body = form.body.data

        try:
            message = Message(body=body, thread_id=thread.id, user_id=current_user.id)
            db.session.add(message)
            db.session.commit()
        except:
            flash('Something went wrong while trying to add the object to the database.', category='warning')

        return redirect(url_for('topics.show_thread', topic_slug=topic_slug, thread_slug=thread_slug))

    return render_template("topics/new_message.html", form=form, topic_slug=topic_slug, thread_slug=thread_slug)

@topics.route("/<topic_slug>/<thread_slug>")
def show_thread(topic_slug, thread_slug):
    thread = Thread.query.filter(Thread.slug == thread_slug).first()

    if thread.secret_users and (current_user not in thread.secret_users):
        abort(404)

    topic = Topic.query.filter(Topic.slug==topic_slug).first()
    return render_template("topics/show_thread.html", thread=thread, topic=topic)

@topics.route("/")
def index():
    return render_template("index.html")

@topics.route("/<topic_slug>")
def topic_page(topic_slug):
    topic_obj = Topic.query.filter(Topic.slug == topic_slug).first()

    if not topic_obj:
        flash(f'Topic \'{topic_slug}\' does not exist.', category='warning')
        return redirect(url_for("index"))

    return render_template("topics/topic.html", topic=topic_obj)

@topics.route("/<topic_slug>/<thread_slug>/<msg_slug>/delete", methods=["GET", "POST"])
@login_required
def delete_msg(topic_slug, thread_slug, msg_slug):
    msg = Message.query.filter(Message.slug == msg_slug)

    if not current_user.id == msg[0].user_id:
        abort(404)

    if request.method == "GET":
        return render_template("topics/delete_message.html", topic_slug=topic_slug, thread_slug=thread_slug, msg_slug=msg_slug)

    msg.delete()
    db.session.commit()
    flash('The message has been successfully deleted.', category='success')
    return redirect(url_for('topics.show_thread', topic_slug=topic_slug, thread_slug=thread_slug))

@topics.route("/<topic_slug>/<thread_slug>/<msg_slug>/edit", methods=["GET", "POST"])
@login_required
def edit_msg(topic_slug, thread_slug, msg_slug):
    msg = Message.query.filter(Message.slug==msg_slug).first()

    if not current_user.id == msg.user_id:
        abort(404)

    if request.method == "GET":
        form = MsgForm(obj=msg)

        return render_template("topics/edit_message.html", form=form, topic_slug=topic_slug, thread_slug=thread_slug, msg_slug=msg_slug)

    form = MsgForm(formdata=request.form, obj=msg)
    form.populate_obj(msg)
    db.session.commit()
    flash('The message has been successfully edited.', category='success')
    return redirect(url_for('topics.show_thread', topic_slug=topic_slug, thread_slug=thread_slug))
