from flask import render_template, flash, redirect, url_for, request
from application import app
from application.topics.models import Thread, Message, Topic

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result")
def result():
    query = request.args.get("query")
    result_msg = None
    result_thread = None
    result_topic = None

    if query:
        result_msg = Message.query.filter(Message.body.contains(query)).all()
        result_thread = Thread.query.filter(Thread.name.contains(query)).all()
        result_topic = Topic.query.filter(Topic.name.contains(query)).all()

    return render_template("result.html", result_msg=result_msg, result_thread=result_thread, result_topic=result_topic, query=query)

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

@app.context_processor
def get_topics():
    return dict(topics_list=Topic.query)