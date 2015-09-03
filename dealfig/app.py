from flask import Flask
from flask.ext.mail import Mail
from flask.ext.wtf.csrf import CsrfProtect

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object("dealfig.settings")

csrf = CsrfProtect(app)
mail = Mail(app)