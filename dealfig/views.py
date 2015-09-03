from flask import render_template, request
from flask.ext.user import login_required

from dealfig import app, data

@app.route("/")
def home():
    return "Hello!"