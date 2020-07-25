from flask_security.forms import RegisterForm
from wtforms import StringField

class ExtendedRegisterForm(RegisterForm):
    username = StringField("Username")