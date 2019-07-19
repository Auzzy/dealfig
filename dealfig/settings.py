import os
basedir = os.path.abspath(os.path.dirname(__file__))

PROPAGATE_EXCEPTIONS = True

# Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql:///dealfig")

# Flask-WTForms
WTF_CSRF_ENABLED = True
SECRET_KEY = "e211788b-355d-4da4-844c-d7a244992a43"

# Flask-Uploads
UPLOADS_DEFAULT_DEST = os.path.join(basedir, "uploads")

# Flask-Security
# SECURITY_USER_IDENTITY_ATTRIBUTES = "username"    # I can enable this to allow login via username (http://stackoverflow.com/a/36929329/6516357)
# SECURITY_USER_IDENTITY_ATTRIBUTES = ("username", "email")
SECURITY_PASSWORD_HASH = "bcrypt"
SECURITY_PASSWORD_SALT = "hello"
SECURITY_EMAIL_SENDER = "sponsors@bostonfig.com"
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_TRACKABLE = False # Maybe check out tracking once I get this running
SECURITY_CONFIRM_EMAIL_WITHIN = "1 days"
SECURITY_RESET_PASSWORD_WITHIN = "1 days"

# Flask-Mail
MAIL_USERNAME = "sponsors@bostonfig.com"
MAIL_PASSWORD = "2016bfig!"
MAIL_DEFAULT_SENDER = ("Boston FIG Sponsor Coordinator", "sponsors@bostonfig.com")
DEFAULT_MAIL_SENDER = ("Boston FIG Sponsor Coordinator", "sponsors@bostonfig.com")
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_SSL = True

# Custom
S3_BUCKET = os.environ.get("S3_BUCKET", "bfig-dealfigurator")