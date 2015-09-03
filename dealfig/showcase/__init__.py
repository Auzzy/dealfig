from flask import Blueprint

app = Blueprint("showcase", __name__, template_folder='templates', static_folder='static')

from dealfig.showcase import views