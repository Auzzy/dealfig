from flask import Blueprint, current_app
from flask.ext.security import current_user, login_required
from flaskext.uploads import configure_uploads, UploadSet

from dealfig.app import app
from dealfig import extensions

from dealfig import admin, benefit_tracker, deals, designers, events, filters, leads, showcase, users

app.register_blueprint(admin.app, url_prefix='/admin')
app.register_blueprint(benefit_tracker.app, url_prefix='/benefit_tracker')
app.register_blueprint(deals.app, url_prefix='/deals')
app.register_blueprint(designers.app, url_prefix='/designers')
app.register_blueprint(events.app, url_prefix='/events')
app.register_blueprint(leads.app, url_prefix='/leads')
app.register_blueprint(showcase.app, url_prefix='/showcase')
app.register_blueprint(users.app, url_prefix='/users')

# Patch Flask-Uploads lack of spport for Python 3
class PatchedDict(dict):
    def itervalues(self):
        return self.values()
app.upload_set_config = PatchedDict()

# configure_uploads(app, (preview_uploader))

from dealfig import views

# Require the user to be logged in to access any endpoint, except /login
for endpoint in app.view_functions.keys():
    if app.view_functions[endpoint].__name__ != "login":
        app.view_functions[endpoint] = login_required(app.view_functions[endpoint])