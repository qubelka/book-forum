from os import getenv
from flask import Flask

app = Flask(__name__)
app.secret_key = 'secret'
#print(getenv("SECRET_KEY"))
from application import routes