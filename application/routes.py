from flask import render_template, flash, redirect, request
from flask_security.views import register as flask_register
from application import app
from application.topics.models import Thread, Message, Topic

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    query = request.args.get('query')

    if query:
        result_msg = Message.query.filter(Message.body.ilike(f'%{query}%')).all()
        result_thread = Thread.query.filter(Thread.name.ilike(f'%{query}%')).all()
        result_topic = Topic.query.filter(Topic.name.ilike(f'%{query}%')).all()

        return render_template('result.html', result_msg=result_msg, result_thread=result_thread, result_topic=result_topic, query=query)

    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    result = flask_register()
    if request.method == 'POST' and type(result).__name__ == 'Response':
        flash('You have been successfully registered.', category='success')

    return result

@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404

@app.context_processor
def get_topics():
    return dict(topics_list=Topic.query)