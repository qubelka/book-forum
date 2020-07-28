from flask import Blueprint, render_template, flash, url_for, redirect, request
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
    thread_form = ThreadForm()

    if thread_form.validate_on_submit():
        name = thread_form.name.data

        try:
            thread = Thread(name=name, topic=topic)
            db.session.add(thread)
            db.session.commit()
        except:
            print('Something went wrong while trying to add the object to the db.')

        return redirect(url_for('topics.topic_page', topic=topic))

    return render_template("topics/new_thread.html", thread_form=thread_form, topic=topic)


@topics.route("/<topic>/<thread_slug>")
def show_thread(topic, thread_slug):
    thread = Thread.query.filter(Thread.slug == thread_slug).first()
    return render_template("topics/show_thread.html", name=thread)

@topics.route("/")
def index():
    return render_template("index.html")
