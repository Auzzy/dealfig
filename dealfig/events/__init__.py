from flask import Blueprint

app = Blueprint("events", __name__, template_folder='templates', static_folder='static')

from dealfig.events import views