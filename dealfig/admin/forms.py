import flask_wtf
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Optional, URL, ValidationError
from wtforms.widgets import TextInput
from werkzeug.datastructures import ImmutableMultiDict

from dealfig import data, model

def filter_strip(value):
    return value.strip() if value else value

def filter_username(value):
    return value or form.email.data.split('@')[0]

def validate_role(form, field):
    try:
        data.UserRoles(field.data)
    except KeyError:
        raise ValidationError("An invalid value was provided for the user's role")

def validate_username(form, field):
    if data.Users.get_by_username(field.data):
        raise ValidationError("A designer with that name already exists.")

class UserForm(flask_wtf.Form):
    first_name = StringField(validators=[DataRequired()], filters=[filter_strip])
    last_name = StringField(validators=[DataRequired()], filters=[filter_strip])
    role_name = SelectField("Role", validators=[DataRequired(), validate_role])
    email = StringField(validators=[DataRequired(), Email()], filters=[filter_strip])
    username = StringField(filters=[filter_strip])
    
    def __init__(self, new=True, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        self.role_name.choices = [("", "")] + [(user_role.role, user_role.role) for user_role in data.UserRoles]
        
        if "obj" in kwargs:
            self.email.data = kwargs["obj"].emails[0].email
            self.username.data = kwargs["obj"].username
    
    def process(self, formdata=None, obj=None, data=None, **kwargs):
        if formdata:
            formdata_dict = formdata.to_dict()
            formdata_dict["username"] = formdata_dict["username"] or formdata_dict["email"].split('@')[0]
            formdata = ImmutableMultiDict(formdata_dict)

        return super(UserForm, self).process(formdata, obj, data, **kwargs)