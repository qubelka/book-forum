import os

class ConfigClass(object):
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if not os.environ.get("HEROKU"):
        DEBUG = True
        SQLALCHEMY_ECHO = True

    SECURITY_REGISTERABLE = True
    SECURITY_POST_REGISTER_VIEW = '/success/registration'
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_MSG_DISABLED_ACCOUNT = (('Specified user does not exist.'), 'error')
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    SECURITY_PASSWORD_HASH = os.getenv("SECURITY_PASSWORD_HASH", "sha512_crypt")