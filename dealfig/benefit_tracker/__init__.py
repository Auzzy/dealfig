from flask import Blueprint

app = Blueprint("benefit_tracker", __name__, template_folder='templates', static_folder='static')

from dealfig.benefit_tracker import views