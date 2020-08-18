from flask_admin.contrib.sqla.validators import Unique
from flask_security.forms import RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from application import User, db


class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', [DataRequired(),
                                        Length(min=4, message='Username should be at least 4 characters long.'),
                                        Unique(model=User, column=User.username,
                                               message='This username is already associated with an account.', db_session=db.session)])