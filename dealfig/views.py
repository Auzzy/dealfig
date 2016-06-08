import flask_wtf
from flask import render_template, request
from flask.ext.user import login_required

from dealfig import app, data
from dealfig.contacts_field import ContactsField

@app.route("/")
def home():
    return "Hello!"

@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        form = TestForm()
        print("VALIDATED: " + str(form.validate_on_submit()))
    else:
        form = TestForm(test=[("name1", "email1"), ("name2", "email2")])

    designer_types = data.DesignerTypes.get_all()

    return render_template("test/test.html", form=form, designer_types=designer_types)

class TestForm(flask_wtf.Form):
    test = ContactsField()