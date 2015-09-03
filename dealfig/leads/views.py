from flask import render_template

from dealfig.leads import app

@app.route("/")
@app.route("/active")
def active():
    return render_template("active_leads.html")

