from flask import render_template

from dealfig import data
from dealfig.leads import app

@app.route("/")
@app.route("/active")
def active():
    return render_template("active_leads.html", leads=data.Leads.get_all())

@app.route("/<name>")
@app.route("/<name>/info")
def info(name):
    lead = data.Leads.get_by_designer(name)
    return render_template("lead-info.html", lead=lead)

@app.route("/new", methods=["GET", "POST"])
@app.route("/<name>/edit", methods=["GET", "POST"])
def configure(name):
    pass