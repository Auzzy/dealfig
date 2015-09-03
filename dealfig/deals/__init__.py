from flask import Blueprint

app = Blueprint("deals", __name__, template_folder='templates', static_folder='static')

from dealfig.deals import views