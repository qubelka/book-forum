from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class ThreadForm(FlaskForm):
    name = StringField('Discussion name', [DataRequired(), Length(min=4, message='Discussion name should be at least 4 characters long.'),
                                           Length(max=70, message='Discussion name can be max 70 characters long.')])
    checkbox = BooleanField('Make this thread secret')
    users = SelectMultipleField('Users', choices=[])

class MsgForm(FlaskForm):
    body = TextAreaField('Message body', [DataRequired(), Length(max=255, message='Message title can be max 255 characters long.')])
