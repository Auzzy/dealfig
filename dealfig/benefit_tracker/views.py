from flask import render_template, request

from dealfig import data
from dealfig.benefit_tracker import app


@app.route("/")
def all():
    exhibitors = data.Exhibitor.get_all()
    return render_template("list-exhibitors.html", exhibitors=exhibitors)

@app.route("/<designer>")
@app.route("/<designer>/info")
def info(designer):
    return ""