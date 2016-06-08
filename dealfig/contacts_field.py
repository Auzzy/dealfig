import collections
import re

import flask_wtf
from wtforms import Field
from wtforms.widgets import HTMLString, html_params
from wtforms.validators import Email


class _ContactWidget(object):
    def __call__(self, field, *args, **kwargs):
        widget_kwargs = kwargs.pop("widget_kwargs")
        name_name, name_value = widget_kwargs.get("name_args")
        email_name, email_value = widget_kwargs.get("email_args")
        
        name_html = self._text_input(name=name_name, value=name_value, placeholder="Name", **kwargs)
        email_html = self._text_input(name=email_name, value=email_value, placeholder="Email", **kwargs)
        add_contact_html = self._add_contact(widget_kwargs, **kwargs)
        return HTMLString(u''.join(['<div class="entry input-group inline">', name_html, email_html, add_contact_html, '</div>']))
    
    def _text_input(self, **kwargs):
        return HTMLString('<input {}>'.format(html_params(**kwargs)))
    
    def _add_contact(self, widget_kwargs, **kwargs):
        return HTMLString(u'<span class="input-group-btn">{}</span>'.format(self._button(widget_kwargs, **kwargs)))
    
    def _button(self, widget_kwargs, **kwargs):
        if widget_kwargs.get("last"):
            return HTMLString(u'<button class="btn btn-success btn-add-element" type="button"><span class="glyphicon glyphicon-plus"></span></button>')
        else:
            return HTMLString(u'<button class="btn btn-danger btn-remove-element" type="button"><span class="glyphicon glyphicon-minus"></span></button>')
    
class ContactsField(Field):
    EMAIL_RE = Email().regex
    
    def __init__(self, *args, **kwargs):
        super(ContactsField, self).__init__(widget=_ContactWidget(), *args, **kwargs)
        
        self.data = []

    def __call__(self, *args, **kwargs):
        contact_html = []
        self.data.append(("", ""))
        for index, contact in enumerate(self.data):
            widget_kwargs = {
                "name_args": ("{}-{}-name".format(self.name, index), contact[0]),
                "email_args": ("{}-{}-email".format(self.name, index), contact[1]),
                "last": index == len(self.data) - 1
            }
            contact_html.append(super(ContactsField, self).__call__(widget_kwargs=widget_kwargs, *args, **kwargs))
        return HTMLString(u'\n'.join([u'<div id="input-container">'] + contact_html + ['</div>']))

    def process(self, formdata, data=None):
        super(ContactsField, self).process(formdata, data)
        
        if formdata:
            self.raw_data = [(name, formdata.getlist(name)[0]) for name in formdata if name.startswith(self.name)]

            try:
                self.process_formdata(self.raw_data)
            except ValueError as e:
                self.process_errors.append(e.args[0])
    
    def process_formdata(self, valuelist):
        if valuelist:
            contact_map = collections.defaultdict(dict)
            for name, value in valuelist:
                parts = name.rsplit('-', maxsplit=2)
                if len(parts) == 3 and parts[0] == self.name:
                    contact_map[int(parts[1])][parts[2]] = value
                else:
                    raise ValueError("Malformed element id")
            
            new_data = []
            for _, contact in sorted(contact_map.items(), key=lambda item: item[0]):
                name, email = contact.get("name"), contact.get("email")
                if name or email:
                    new_data.append((name, email))
            self.data = new_data
    
    def process_data(self, value):
        if value:
            self.data = value
    
    def pre_validate(self, form):
        new_formdata = []
        for name, email in self.data:
            if name and email:
                if not ContactsField.EMAIL_RE.match(email):
                    raise ValueError("Invalid email(s)")
            else:
                raise ValueError("A name and an email must be provided for each contact")