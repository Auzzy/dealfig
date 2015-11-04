from flask import jsonify, render_template, request

from dealfig import data
from dealfig.leads import app


@app.route("/")
def active():
    return render_template("list-leads.html", leads=data.Leads.get_all())

@app.route("/<designer>")
@app.route("/<designer>/info")
def info(designer):
    lead = data.Leads.get_by_designer(designer)
    return render_template("lead-info.html", lead=lead)

@app.route("/<designer>/comment", methods=["POST"])
def submit_comment(designer):
    text = request.form["commentText"]
    lead = data.Leads.get_by_designer(designer)
    comment = data.Comment.submit(lead, text)
    return render_template("_comment.html", comment=comment)

@app.route("/transitions", methods=["POST"])
def get_transitions():
    transitions = data.LeadStatus.get_transitions(request.form["status"])
    transitions_dict = {transition.name:transition.name for transition in transitions}
    return jsonify(transitions_dict)

@app.route("/<designer>/status", methods=["POST"])
def post_status(designer):
    return data.Leads.update_status(designer, request.form["value"])