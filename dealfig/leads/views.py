from flask import jsonify, redirect, render_template, request, url_for

from dealfig import data
from dealfig.leads import app

@app.route("/")
@app.route("/list/<year>")
def active(year=None):
    return render_template("list-leads.html", leads=data.Leads.get_by_year(year))

@app.route("/<designer>/create", methods=["POST"])
def create(designer):
    lead = data.Leads.get_or_create(designer)
    return url_for('leads.info', designer=designer)

@app.route("/<designer>")
@app.route("/<designer>/<year>")
def info(designer, year=None):
    lead = data.Leads.get_by_designer(designer, year)
    owner_list = data.Users.get_by_role("sales")
    return render_template("lead-info.html", lead=lead, owner_list=owner_list)

@app.route("/<designer>/comment", methods=["POST"])
def submit_comment(designer):
    text = request.form["commentText"]
    comment = data.Comments.create(designer, text)
    return render_template("_comment.html", comment=comment)

@app.route("/<designer>/status", methods=["POST"])
def update_status(designer):
    status = data.Leads.update_status(designer, request.form["status"])
    return jsonify({"name": status.name, "deal_ready": status.deal_ready})

@app.route("/<designer>/owner", methods=["POST"])
def update_owner(designer):
    return data.Leads.update_owner(designer, request.form["value"])

@app.route("/transitions")
def get_transitions():
    transitions = data.LeadStatus.get_transition_names(request.args["status"])
    return jsonify(data=transitions)
