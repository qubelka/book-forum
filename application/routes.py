from flask import render_template, flash, redirect, url_for, request
from flask_security import login_required
from application import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/topic/<topic>")
@login_required
def topic_page(topic):
    name = ''
    description = 'Conversations about '
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

    return render_template("topic.html", topic=topic, name=name, description=description)

@app.route("/success/<type>")
def success(type):
    if type == 'registration':
        flash('You have been successfully registered.', category='success')
    elif type == 'login':
        flash('You have been successfully logged in.', category='success')
    elif type == 'logout':
        flash('You have been successfully logged out.', category='success')
    else:
        flash(f'Path \'success/{type}\' does not exist.', category='warning')
    return redirect('/')

@app.errorhandler(404)
def error404(error):
    return render_template("404.html"), 404