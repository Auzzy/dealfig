from flask import jsonify, render_template, request, url_for

from dealfig import data
from dealfig.showcase import app

@app.route("/")
@app.route("/list/<event_name>")
def all(event_name=None):
    showcase = data.Showcases.get_by_event(event_name)
    return render_template("list-showcase.html", showcase=showcase)

@app.route("/<designer>")
@app.route("/<designer>/info")
def info(designer):
    showcase = data.Showcases.get_by_designer(designer)
    return render_template("showcase-info.html", showcase=showcase)

@app.route("/<designer>/create", methods=["POST"])
def create(designer):
    showcase = data.Showcases.get_or_create(designer)
    return url_for('showcase.info', designer=designer)

@app.route("/<designer>/name", methods=["POST"])
def update_name(designer):
    name = data.Showcases.update_name(designer, request.form["value"])
    return jsonify({"value": name})

@app.route("/<designer>/homepage", methods=["POST"])
def update_homepage(designer):
    homepage = data.Showcases.update_homepage(designer, request.form["value"])
    return jsonify({"value": homepage})

@app.route("/<designer>/description", methods=["POST"])
def update_description(designer):
    description = data.Showcases.update_description(designer, request.form["value"])
    return jsonify({"value": description})