from flask import Blueprint

app = Blueprint("admin", __name__, template_folder='templates', static_folder='static')

from dealfig.admin import views