from flask import render_template, request

from dealfig import data
from dealfig.benefit_tracker import app


@app.route("/")
@app.route("/list/<event_name>")
def all(event_name=None):
    sponsors = [deal.designer for deal in data.Deals.get_by_event(event_name)]
    showcase_designers = [showcase.designer for showcase in data.Showcases.get_by_event(event_name)]
    exhibitors = set(sponsors + showcase_designers)
    return render_template("benefit-tracker.html", exhibitors=exhibitors)

@app.route("/<designer>/benefits")
def benefits(designer):
    return ""