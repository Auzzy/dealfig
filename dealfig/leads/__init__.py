from flask import Blueprint

app = Blueprint("leads", __name__, template_folder='templates', static_folder='static')

from dealfig.leads import views