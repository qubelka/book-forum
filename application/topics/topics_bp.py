from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import current_user
from flask_security import login_required
from .models import Message, Thread, Topic

from .forms import ThreadForm, MsgForm
from .. import db

topics = Blueprint('topics', __name__)

@topics.route("/<topic_slug>/add_thread", methods=["GET", "POST"])
@login_required
def add_thread(topic_slug):
    form = ThreadForm()

    if form.validate_on_submit():
        name = form.name.data
        topic = Topic.query.filter(Topic.slug == topic_slug).first()

        try:
            thread = Thread(name=name, topic_id=topic.id, user_id=current_user.id)
            db.session.add(thread)
            db.session.commit()
        except:
            flash('Something went wrong while trying to add the object to the database.', category='warning')

        return redirect(url_for('topics.topic_page', topic_slug=topic_slug))

    return render_template("topics/new_thread.html", form=form, topic_slug=topic_slug)

@topics.route("/<topic_slug>/<thread_slug>/add_message", methods=["GET", "POST"])
@login_required
def add_message(topic_slug, thread_slug):
    form = MsgForm()

    if form.validate_on_submit():
        body = form.body.data
        thread = Thread.query.filter(Thread.slug == thread_slug).first()

        try:
            message = Message(body=body, created_by=current_user.username, thread_id=thread.id, user_id=current_user.id)
            db.session.add(message)
            db.session.commit()
        except:
            flash('Something went wrong while trying to add the object to the database.', category='warning')

        return redirect(url_for('topics.show_thread', topic_slug=topic_slug, thread_slug=thread_slug))

    return render_template("topics/new_message.html", form=form, topic_slug=topic_slug, thread_slug=thread_slug)

@topics.route("/<topic_slug>/<thread_slug>")
def show_thread(topic_slug, thread_slug):
    thread = Thread.query.filter(Thread.slug == thread_slug).first()
    return render_template("topics/show_thread.html", thread=thread, topic_slug=topic_slug)

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