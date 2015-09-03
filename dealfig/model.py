import collections
import datetime
import re

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import event, SQLAlchemy
from flask.ext.user import SQLAlchemyAdapter, UserManager, UserMixin
from wtforms.validators import ValidationError

from dealfig.app import app

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=app.config["MIGRATIONS_DIRECTORY"])
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Designer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    type_name = db.Column("type", db.String(50), nullable=False)
    notes = db.Column(db.Text(), default="")
    homepage = db.Column(db.String(200))
    contacts = db.relationship("Contact", cascade="all, delete-orphan", passive_updates=False, backref="designer", lazy="dynamic")
    past_deals = db.relationship("PastDeal", cascade="all, delete-orphan", passive_updates=False, backref="designer", lazy="dynamic")

class DesignerType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designer_id = db.Column(db.Integer, db.ForeignKey('designer.id'))
    email = db.Column(db.String(80))
    name = db.Column(db.String(40))

class PastDeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designer_id = db.Column(db.Integer, db.ForeignKey('designer.id'))
    year = db.Column(db.Integer)
    owner_name = db.Column(db.String(60))
    level_name = db.Column(db.String(20))
    cash = db.Column(db.Integer, default=0)
    inkind = db.Column(db.Integer, default=0)


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20))
    notes = db.Column(db.Text())
    emails = db.relationship("Email", cascade="all, delete-orphan", passive_updates=False, backref="lead", lazy="dynamic")
    
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime())
    notes = db.Column(db.Text())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')
    enabled = db.Column(db.Boolean(), nullable=False, default=False)
    type_name = db.Column("type", db.String(50), nullable=False)
    emails = db.relationship("UserEmail", lazy="dynamic")
    user_auth = db.relationship("UserAuth", uselist=False)
    
    def is_active(self):
        return self.enabled

class UserEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    email = db.Column(db.String(255), nullable=False, unique=True)
    is_primary = db.Column(db.Boolean(), nullable=False, default=False)
    confirmed_at = db.Column(db.DateTime())
    user = db.relationship('User', uselist=False)

class UserAuth(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    reset_password_token = db.Column(db.String(100), nullable=False, default='')
    user = db.relationship('User', uselist=False, foreign_keys=user_id)

@event.listens_for(User, 'load')
def load_user(target, context):
    # target.type = data.UserType[target.type_name] if target.type_name in data.UserType.__members__ else None
    pass



def password_validator(form, field):
    password = field.data
    if len(password) < 6:
        raise ValidationError("Password must have at least 6 characters.")

if not hasattr(app, "user_manager"):
    db_adapter = SQLAlchemyAdapter(db, User, UserAuthClass=UserAuth, UserEmailClass=UserEmail)
    user_manager = UserManager(db_adapter, app, password_validator=password_validator)


if __name__ == '__main__':
    manager.run()
