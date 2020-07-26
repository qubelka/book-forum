from flask import render_template, flash, redirect, url_for, request
from application import app

@app.route("/")
def index():
    return render_template("index.html")

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