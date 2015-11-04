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


designers_to_contacts = db.Table('designers_to_contacts',
    db.Column('designer_id', db.Integer, db.ForeignKey('designer.id')),
    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'))
)

leads_to_contacts = db.Table('leads_to_contacts',
    db.Column('lead_id', db.Integer, db.ForeignKey('lead.id')),
    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'))
)

showcase_to_contacts = db.Table('showcase_to_contacts',
    db.Column('showcase_id', db.Integer, db.ForeignKey('showcase.id')),
    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'))
)

class Designer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    type_name = db.Column("type", db.String(50), nullable=False)
    notes = db.Column(db.Text(), default="")
    homepage = db.Column(db.String(200))
    contacts = db.relationship("Contact", secondary=designers_to_contacts)
    leads = db.relationship("Lead", cascade="all, delete-orphan", passive_updates=False, backref="designer", lazy="dynamic")
    showcase = db.relationship("Deal", uselist=False, backref="designer")

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designer_id = db.Column(db.Integer, db.ForeignKey('designer.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship("User", backref="leads")
    created = db.Column(db.DateTime(), default=datetime.datetime.now, nullable=False)
    status = db.Column("status", db.String(50), nullable=False)
    comments = db.relationship("Comment", cascade="all, delete-orphan", passive_updates=False, backref="lead", lazy="dynamic")
    contacts = db.relationship("Contact", secondary=leads_to_contacts)
    deal = db.relationship("Deal", uselist=False, backref="lead")

class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship("User", backref="deals")
    level = db.Column(db.String(30))
    cash = db.Column(db.Integer, default=0)
    inkind = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text())
    contract = db.relationship("Contract", uselist=False, backref="deal")
    invoice = db.relationship("Invoice", uselist=False, backref="deal")
    
    @property
    def designer(self):
        return self.lead.designer
    
    @property
    def contract_signed(self):
        return bool(self.contract.signed)
    
    @property
    def invoice_paid(self):
        return bool(self.invoice.paid)

class Showcase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designer_id = db.Column(db.Integer, db.ForeignKey('designer.id'), nullable=False)
    game_name = db.Column(db.String(160))
    game_homepage = db.Column(db.String(200))
    game_description = db.Column(db.Text())

class DesignerType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

class LeadStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    status_id = db.Column(db.Integer, db.ForeignKey('leadstatus.id'))
    transitions = db.relationship("LeadStatus")

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(40))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User")
    created = db.Column(db.DateTime(), nullable=False)
    text = db.Column(db.Text(), nullable=False)

class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sent = db.Column(db.Date)
    signed = db.Column(db.Date)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sent = db.Column(db.Date)
    paid = db.Column(db.Date)

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


def password_validator(form, field):
    password = field.data
    if len(password) < 6:
        raise ValidationError("Password must have at least 6 characters.")

if not hasattr(app, "user_manager"):
    db_adapter = SQLAlchemyAdapter(db, User, UserAuthClass=UserAuth, UserEmailClass=UserEmail)
    user_manager = UserManager(db_adapter, app, password_validator=password_validator)


if __name__ == '__main__':
    manager.run()
