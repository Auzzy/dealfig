from flaskext.uploads import configure_uploads, UploadSet

from dealfig.app import app
from dealfig import extensions
from dealfig import asset_tracker, benefit_tracker, config, deals, designers, filters, leads, showcase, users

app.register_blueprint(asset_tracker.app, url_prefix='/asset_tracker')
app.register_blueprint(benefit_tracker.app, url_prefix='/benefit_tracker')
app.register_blueprint(config.app, url_prefix='/config')
app.register_blueprint(deals.app, url_prefix='/deals')
app.register_blueprint(designers.app, url_prefix='/designers')
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