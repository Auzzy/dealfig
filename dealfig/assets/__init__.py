from flask import Blueprint

app = Blueprint("assets", __name__, template_folder='templates', static_folder='static')

from dealfig.assets import views