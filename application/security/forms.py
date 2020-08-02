from flask_security.forms import RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class ExtendedRegisterForm(RegisterForm):
    username = StringField("Username", [DataRequired(), Length(min=4, message="Username should be at least 4 characters long.")])