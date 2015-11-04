from flask import render_template, request
from flask.ext.user import login_required

from dealfig import data
from dealfig.showcase import app

@app.route("/")
def all():
    showcase = data.Showcase.get_all()
    return render_template("list-showcase.html", showcase=showcase)

@app.route("/<designer>")
@app.route("/<designer>/info")
def info(designer):
    showcase = data.Showcase.get_by_designer(designer)
    return render_template("showcase-info.html", showcase=showcase)
