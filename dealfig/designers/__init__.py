from flask import Blueprint

app = Blueprint("designers", __name__, template_folder='templates', static_folder='static')

from dealfig.designers import views