from flask import render_template, request

from dealfig import data
from dealfig.benefit_tracker import app


@app.route("/")
@app.route("/list/<year>")
def all(year=None):
    exhibitors = data.Exhibitor.get_by_year(year)
    return render_template("list-exhibitors.html", exhibitors=exhibitors)

@app.route("/<designer>/info")
def info(designer):
    return ""