from flask import jsonify, redirect, render_template, request, url_for
from flask.ext.user import login_required

from dealfig import data
from dealfig.designers import app

@app.route("/")
def all():
    designers = data.Designers.get_all()
    designer_types = data.DesignerTypes.get_all()
    return render_template("list-designers.html", designers=designers, designer_types=designer_types)

@app.route("/new", methods=["POST"])
def new_designer():
    designer = data.Designers.new(request.form["name"], request.form["designer_type"])
    return url_for("designers.info", designer_name=designer.name)

@app.route("/<designer_name>")
@app.route("/<designer_name>/info")
def info(designer_name):
    designer = data.Designers.get_by_name(designer_name)
    designer_types = data.DesignerTypes.get_all()
    return render_template("designer.html", designer=designer, designer_types=designer_types)

@app.route("/<designer_name>/leads")
def leads(designer_name):
    designer = data.Designers.get_by_name(designer_name)
    return render_template("designer-leads.html", designer=designer)

@app.route("/<designer_name>/deals")
def deals(designer_name):
    designer = data.Designers.get_by_name(designer_name)
    return render_template("designer-deals.html", designer=designer)

@app.route("/<designer_name>/type", methods=["POST"])
def update_type(designer_name):
    return data.Designers.update_type(designer_name, request.form["value"])

@app.route("/<designer_name>/homepage", methods=["POST"])
def update_homepage(designer_name):
    homepage = data.Designers.update_homepage(designer_name, request.form["value"])
    return jsonify({"value": homepage})

@app.route("/<designer_name>/notes", methods=["POST"])
def update_notes(designer_name):
    notes = data.Designers.update_notes(designer_name, request.form["value"])
    return jsonify({"value": notes})

@app.route("/<designer_name>/add-contact", methods=["POST"])
def add_contact(designer_name):
    data.Designers.add_contact(designer_name, request.form["name"], request.form["email"])
    return ""

@app.route("/<designer_name>/delete-contact", methods=["POST"])
def delete_contact(designer_name):
    return data.Designers.delete_contact(designer_name, request.form["email"])