from flask import Flask
from flask.ext.mail import Mail
from flask.ext.wtf.csrf import CsrfProtect

from dealfig import assets, deals, leads

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object("sponsortracker.settings")

app.register_blueprint(assets.app, url_prefix='/assets')
app.register_blueprint(deals.app, url_prefix='/deals')
app.register_blueprint(leads.app, url_prefix='/leads')

csrf = CsrfProtect(app)
mail = Mail(app)