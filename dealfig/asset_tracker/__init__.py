from flask import Blueprint

app = Blueprint("asset_tracker", __name__, template_folder='templates', static_folder='static')

from dealfig.asset_tracker import views