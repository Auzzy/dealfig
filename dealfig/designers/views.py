from flask import redirect, render_template, request, url_for
from flask.ext.user import login_required

from dealfig import data
from dealfig.designers import app, forms

@app.route("/")
def all():
    designers = data.Designers.get_all()
    return render_template("list-designers.html", designers=designers)

@app.route("/<designer_name>")
@app.route("/<designer_name>/info")
def info(designer_name):
    designer = data.Designers.get_by_name(designer_name)
    return render_template("designer-info.html", designer=designer)

@app.route("/new", methods=["GET", "POST"])
@app.route("/<designer_name>/edit", methods=["GET", "POST"])
def configure(designer_name=None):
    designer = data.Designers.get_by_name(designer_name)
    if request.method == "POST":
        contacts = zip(request.form.getlist("names"), request.form.getlist("emails"))
        form = forms.DesignerForm(new=designer_name is None)
        if form.validate_on_submit():
            designer = data.Designers.save(designer_name, form, contacts)
            return redirect(url_for("designers.info", designer_name=designer.name))
    else:
        form = forms.DesignerForm(obj=designer) if designer_name else forms.DesignerForm()
    contacts = designer.contacts if designer_name else []
    return render_template("configure-designer.html", name=designer_name, form=form, contacts=contacts)