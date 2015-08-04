from flask import Blueprint

app = Blueprint("assets", template_folder='templates', static_folder='static')