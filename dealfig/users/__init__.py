from flask import Blueprint

app = Blueprint("users", __name__, template_folder='templates', static_folder='static')

from dealfig.users import views