from flask import jsonify, render_template, request, url_for

from dealfig import data, filters
from dealfig.leads import app

@app.route("/")
@app.route("/list/<event_name>")
def active(event_name=None):
    return render_template("list-leads.html", leads=data.Leads.get_by_event(event_name))

@app.route("/<designer>/create", methods=["POST"])
def create(designer):
    lead = data.Leads.get_or_create(designer)
    return url_for('leads.info', designer=designer)

@app.route("/<designer>")
@app.route("/<designer>/<event_name>")
def info(designer, event_name=None):
    lead = data.Leads.get_by_designer(designer, event_name)
    owner_list = data.Users.get_by_role("sales")
    return render_template("lead-info.html", lead=lead, owner_list=owner_list)

@app.route("/<designer>/comment", methods=["POST"])
def submit_comment(designer):
    text = request.form["commentText"]
    comment = data.Comments.create(designer, text)
    return render_template("_comment.html", comment=comment)

@app.route("/<designer>/comment/edit", methods=["POST"])
def edit_comment(designer):
    comment_id = request.form["commentId"]
    text = request.form["commentText"]
    comment = data.Comments.edit(comment_id, text)
    return jsonify({"comment": comment.text, "timestamp": filters.comment_datetime_filter(comment.edited)})

@app.route('/designer/comment/delete', methods=["POST"])
def delete_comment():
    id = request.form["comment_id"]
    data.Comments.delete(id)
    return jsonify({})

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
