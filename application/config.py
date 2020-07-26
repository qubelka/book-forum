from os import getenv

class ConfigClass(object):
    DEBUG = True
    SECRET_KEY = getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL")
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECURITY_REGISTERABLE = True
    SECURITY_POST_REGISTER_VIEW = '/success/registration'
    SECURITY_POST_LOGIN_VIEW = '/success/login'
    SECURITY_POST_LOGOUT_VIEW = '/success/logout'
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_PASSWORD_SALT = getenv("SECURITY_PASSWORD_SALT")
    SECURITY_PASSWORD_HASH = getenv("SECURITY_PASSWORD_HASH", "sha512_crypt")