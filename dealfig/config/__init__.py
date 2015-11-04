from flask import Blueprint

app = Blueprint("config", __name__, template_folder='templates', static_folder='static')

from dealfig.config import views