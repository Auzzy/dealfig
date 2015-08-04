from flask.ext.user import SQLAlchemyAdapter, UserManager
from flaskext.uploads import configure_uploads, UploadSet

from dealfig import model, model_events
from dealfig.app import app

# Patch Flask Uploads lack of spport for Python 3
class PatchedDict(dict):
    def itervalues(self):
        return self.values()
app.upload_set_config = PatchedDict()

configure_uploads(app, (preview_uploader))

from . import views