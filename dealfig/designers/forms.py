import flask_wtf
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Optional, URL, ValidationError

from dealfig import data, model


def filter_strip(value):
    return value.strip() if value else value
    
def validate_designer(form, field):
    if model.Designer.query.filter_by(name=field.data).one():
        raise ValidationError("A designer with that name already exists.")

class DesignerForm(flask_wtf.Form):
    name = StringField(validators=[DataRequired(), validate_designer], filters=[filter_strip])
    type_name = SelectField("Designer Type", validators=[DataRequired(), Optional()])
    link = StringField("Home page", validators=[URL(), Optional()], filters=[filter_strip])
    notes = TextAreaField(validators=[Optional()], filters=[filter_strip])
    
    def __init__(self, new=True, *args, **kwargs):
        super(DesignerForm, self).__init__(*args, **kwargs)
        
        self.type_name.choices = [("", "")] + data.DesignerTypes.as_options()
        
        if not new:
            self.name.validators = [DataRequired()]