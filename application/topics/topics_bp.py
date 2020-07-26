from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_security import login_required
from .forms import ThreadForm, MsgForm

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

    return render_template("topics/topic.html", topic=topic, name=name, description=description)

@topics.route("/<topic>/add_thread", methods=["GET", "POST"])
@login_required
def add_thread(topic):
    if request.method=="GET":
        thread_form = ThreadForm()
        return render_template("topics/new_thread.html", thread_form=thread_form, topic=topic)

    return "great"

@topics.route("/<topic>/<thread_slug>")
def show_thread(topic, thread_slug):
    return render_template("topics/show_thread.html", name='Thread1')

@topics.route("/")
def index():
    return render_template("index.html")
