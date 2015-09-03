from flask import render_template, request
from flask.ext.user import login_required

from dealfig import data
from dealfig.designers import app, forms

@app.route("/")
def all():
    designers = data.Designers.get_all()
    return render_template("list-designers.html", designers=designers)

@app.route("/<name>")
@app.route("/<name>/info")
def info(name):
    designer = data.Designers.get_by_name(name)
    return render_template("designer-info.html", designer=designer)

@app.route("/new", methods=["GET", "POST"])
@app.route("/<name>/edit", methods=["GET", "POST"])
def configure(name=None):
    designer = data.Designers.get_by_name(name)
    if request.method == "POST":
        contacts = zip(request.form.getlist("names"), request.form.getlist("emails"))
        form = forms.DesignerForm(new=name is None)
        if form.validate_on_submit():
            designer = data.Designers.save(name, form, contacts)
            return redirect(url_for("designer_info", name=designer.name))
    else:
        form = forms.DesignerForm(obj=designer) if name else forms.DesignerForm()
    contacts = designer.contacts if name else []
    return render_template("configure-designer.html", name=name, form=form, contacts=contacts)

@app.route("/test-post", methods=["POST"])
def test_post():
    print(list(zip(request.form.getlist("emails"), request.form.getlist("names"))))
    return ""