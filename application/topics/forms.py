from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class ThreadForm(FlaskForm):
    name = StringField('Discussion name', [DataRequired(), Length(min=4, message="Discussion name should be at least 4 characters long."),
                                           Length(max=70, message="Discussion name can be max 70 characters long.")])

class MsgForm(FlaskForm):
    title = StringField('Message title', [DataRequired(), Length(min=4, message="Message title should be at least 4 characters long."),
                                          Length(max=70, message="Message title can be max 70 characters long.")])
    body = TextAreaField('Message body', [DataRequired(), Length(max=255, message="Message title can be max 255 characters long.")])
