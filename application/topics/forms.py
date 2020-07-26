from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField

class ThreadForm(FlaskForm):
    name = StringField('Discussion name')

class MsgForm(FlaskForm):
    title = StringField('Message title')
    body = TextAreaField('Message body')