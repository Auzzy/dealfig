from flaskext.uploads import configure_uploads, UploadSet

from dealfig.app import app
from dealfig import assets, deals, designers, leads, showcase

app.register_blueprint(assets.app, url_prefix='/assets')
app.register_blueprint(deals.app, url_prefix='/deals')
app.register_blueprint(designers.app, url_prefix='/designers')
app.register_blueprint(leads.app, url_prefix='/leads')
app.register_blueprint(showcase.app, url_prefix='/showcase')

# Patch Flask Uploads lack of spport for Python 3
class PatchedDict(dict):
    def itervalues(self):
        return self.values()
app.upload_set_config = PatchedDict()

# configure_uploads(app, (preview_uploader))

from dealfig import views