from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import current_user
from flask_security import login_required
from .models import Message, Thread

from .forms import ThreadForm, MsgForm
from .. import db

topics = Blueprint('topics', __name__)

@topics.route("/<topic>")
def topic_page(topic):
    name = ''
    description = 'Discussions about '
    if topic == 'bestsellers':
        name = 'Bestsellers'
        description += 'best-selling books'
    elif topic == 'new_releases':
        name = 'New Releases'
        description += 'upcoming book releases'
    elif topic == 'what_to_read':
        name = 'What Should I Read Next?'
        description += 'reading suggestion'
    elif topic == 'authors':
        name = 'Authors'
        description += 'book authors'
    else:
        flash(f'Topic \'{topic}\' does not exist. Please choose one topic from the following list:')
        return redirect(url_for("index"))

    thread_list = Thread.query.filter(Thread.topic==topic).all()
    return render_template("topics/topic.html", topic=topic, name=name, description=description, threads=thread_list)

@topics.route("/<topic>/add_thread", methods=["GET", "POST"])
@login_required
def add_thread(topic):
    form = ThreadForm()

    if form.validate_on_submit():
        name = form.name.data

        try:
            thread = Thread(name=name, topic=topic, user_id=current_user.id)
            db.session.add(thread)
            db.session.commit()
        except:
            flash('Something went wrong while trying to add the object to the database.', category='warning')

        return redirect(url_for('topics.topic_page', topic=topic))

    return render_template("topics/new_thread.html", form=form, topic=topic)

@topics.route("/<topic>/<thread_slug>/add_message", methods=["GET", "POST"])
@login_required
def add_message(topic, thread_slug):
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

        return redirect(url_for('topics.show_thread', topic=topic, thread_slug=thread_slug))

    return render_template("topics/new_message.html", form=form, topic=topic, thread_slug=thread_slug)

@topics.route("/<topic>/<thread_slug>")
def show_thread(topic, thread_slug):
    thread = Thread.query.filter(Thread.slug == thread_slug).first()
    return render_template("topics/show_thread.html", thread=thread, topic=topic)

@topics.route("/")
def index():
    return render_template("index.html")
