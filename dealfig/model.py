import collections
import datetime
import re
import sys

from flask.ext.sqlalchemy import event, SQLAlchemy
from flask.ext.user import SQLAlchemyAdapter, UserManager, UserMixin
from wtforms.validators import ValidationError

from dealfig.app import app

db = SQLAlchemy(app)

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

lead_status_to_lead_status = db.Table('lead_status_to_lead_status',
    db.Column('status_from_id', db.Integer, db.ForeignKey('lead_status.id'), primary_key=True),
    db.Column('status_to_id', db.Integer, db.ForeignKey('lead_status.id'), primary_key=True)
)

asset_definition_to_file_format = db.Table('asset_definition_to_file_format',
    db.Column('asset_definition_id', db.Integer, db.ForeignKey('asset_definition.id')),
    db.Column('file_format_id', db.Integer, db.ForeignKey('file_format.id'))
)

asset_definition_to_media_type = db.Table('asset_definition_to_media_type',
    db.Column('asset_definition_id', db.Integer, db.ForeignKey('asset_definition.id')),
    db.Column('media_type_id', db.Integer, db.ForeignKey('media_type.id'))
)

class Designer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    type_id = db.Column(db.Integer, db.ForeignKey('designer_type.id'), nullable=False)
    type = db.relationship("DesignerType")
    notes = db.Column(db.Text(), default="")
    homepage = db.Column(db.String(200), default="")
    contacts = db.relationship("Contact", secondary=designers_to_contacts, lazy="dynamic")
    leads = db.relationship("Lead", cascade="all, delete-orphan", passive_updates=False, backref="designer", lazy="dynamic")
    showcase = db.relationship("Showcase", uselist=False, backref="designer")
    exhibitor = db.relationship("Exhibitor", uselist=False, backref="designer")

    @property
    def active_lead(self):
        return self.leads.filter_by(year=datetime.datetime.today().year).first()
    
    @property
    def active_deal(self):
        return self.active_lead.deal
    
    @property
    def deals(self):
        return [lead.deal for lead in self.leads if lead.deal]
    
    @property
    def active_showcase(self):
        if self.showcase and self.showcase.year == datetime.datetime.today().year:
            return self.showcase
        else:
            return None

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designer_id = db.Column(db.Integer, db.ForeignKey('designer.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship("User", backref="leads")
    status_id = db.Column(db.Integer, db.ForeignKey('lead_status.id'), nullable=False)
    status = db.relationship("LeadStatus")
    created = db.Column(db.DateTime(), default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.DateTime(), default=datetime.datetime.now, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    comments = db.relationship("Comment", cascade="all, delete-orphan", passive_updates=False, backref="lead", lazy="dynamic")
    contacts = db.relationship("Contact", secondary=leads_to_contacts)
    deal = db.relationship("Deal", uselist=False, backref="lead")

class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship("User", backref="deals")
    level_id = db.Column(db.Integer, db.ForeignKey('deal_level.id'))
    level = db.relationship("DealLevel")
    cash = db.Column(db.Integer, default=0)
    inkind = db.Column(db.Text(), default="")
    notes = db.Column(db.Text(), default="")
    contract = db.relationship("Contract", uselist=False, backref="deal")
    invoice = db.relationship("Invoice", uselist=False, backref="deal")
    
    @property
    def designer(self):
        return self.lead.designer
    
    @property
    def year(self):
        return self.lead.year
    
    @property
    def contract_signed(self):
        return bool(self.contract.signed)
    
    @property
    def invoice_paid(self):
        return bool(self.invoice.paid)

class Showcase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designer_id = db.Column(db.Integer, db.ForeignKey('designer.id'), unique=True)
    year = db.Column(db.Integer, nullable=False)
    game_name = db.Column(db.String(160), default="")
    game_homepage = db.Column(db.String(200), default="")
    game_description = db.Column(db.Text(), default="")

class Exhibitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designer_id = db.Column(db.Integer, db.ForeignKey('designer.id'), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('deal_level.id'))
    level = db.relationship("DealLevel")
    type = db.Column(db.String(20))
    assets = db.relationship("Asset", cascade="all, delete-orphan", passive_updates=False, backref="exhibitor", lazy="dynamic")

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(40), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="comments", cascade="all")
    created = db.Column(db.DateTime(), nullable=False)
    text = db.Column(db.Text(), nullable=False)

class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deal_id = db.Column(db.Integer, db.ForeignKey('deal.id'), nullable=False)
    sent = db.Column(db.Date)
    signed = db.Column(db.Date)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deal_id = db.Column(db.Integer, db.ForeignKey('deal.id'), nullable=False)
    sent = db.Column(db.Date)
    paid = db.Column(db.Date)

class AssetDefinition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('deal_level.id'), nullable=False)
    level = db.relationship("DealLevel")
    type = db.Column(db.String(20), nullable=False) # text, logo, or image
    media_types = db.relationship("MediaType", secondary=asset_definition_to_media_type)
    formats = db.relationship("FileFormat", secondary=asset_definition_to_file_format)

class FileFormat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    ext = db.Column(db.String(10), unique=True)

class MediaType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50))
    
    @property
    def display_name(self):
        if self.location:
            return "{} - {}".format(self.name, self.location)
        else:
            return self.name

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exhibitor_id = db.Column(db.Integer, db.ForeignKey('exhibitor.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    filename = db.Column(db.String(256), nullable=False)
    type = db.Column(db.String(20), nullable=False) # text, logo, or image
    media_type_id = db.Column(db.Integer, db.ForeignKey('media_type.id'))
    media_type = db.relationship("MediaType") # A value of null indicates no restrictions on usage
    format_id = db.Column(db.Integer, db.ForeignKey('file_format.id'), nullable=False)
    format = db.relationship("FileFormat")

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')
    enabled = db.Column(db.Boolean(), nullable=False, default=False)
    role_name = db.Column("role", db.String(50), nullable=False)
    emails = db.relationship("UserEmail", cascade="all, delete-orphan")
    user_auth = db.relationship("UserAuth", uselist=False, cascade="all, delete-orphan")
    
    comments = db.relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    
    def is_active(self):
        return self.enabled

    @property
    def username(self):
        return self.user_auth.username

    @property
    def key(self):
        return self.username

    def __str__(self):
        return "{first} {last}".format(first=self.first_name, last=self.last_name)

class UserEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    email = db.Column(db.String(255), nullable=False, unique=True)
    is_primary = db.Column(db.Boolean(), nullable=False, default=False)
    confirmed_at = db.Column(db.DateTime())
    user = db.relationship('User', uselist=False)

    def __str__(self):
        return self.email

class UserAuth(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    reset_password_token = db.Column(db.String(100), nullable=False, default='')


class DesignerType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    @property
    def key(self):
        return self.name

    def __str__(self):
        return self.name

class LeadStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    deal_ready = db.Column(db.Boolean(), nullable=False, default=False)
    transitions = db.relationship("LeadStatus",
        secondary=lead_status_to_lead_status,
        primaryjoin=id==lead_status_to_lead_status.c.status_from_id,
        secondaryjoin=id==lead_status_to_lead_status.c.status_to_id,
        backref="prior_status"
    )
    
    @property
    def start(self):
        return LeadStatus.query.filter_by(name="To Call").one()

    def __str__(self):
        return self.name

class DealLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    @property
    def key(self):
        return self.name

    def __str__(self):
        return self.name

def password_validator(form, field):
    password = field.data
    if len(password) < 6:
        raise ValidationError("Password must have at least 6 characters.")

if not hasattr(app, "user_manager"):
    db_adapter = SQLAlchemyAdapter(db, User, UserAuthClass=UserAuth, UserEmailClass=UserEmail)
    user_manager = UserManager(db_adapter, app, password_validator=password_validator)



def _create():
    db.create_all()
    _init_lead_status()
    _init_designer_type()
    _init_deal_level()

def _init_lead_status():
    call = LeadStatus(name="To Call")
    reached_out = LeadStatus(name="Reached Out")
    talking = LeadStatus(name="In Talks")
    verbal = LeadStatus(name="Verbal Deal", deal_ready=True)
    declined = LeadStatus(name="Declined")
    pulled_out = LeadStatus(name="Pulled Out")
    
    call.transitions = [reached_out, talking, verbal, declined]
    reached_out.transitions = [talking, verbal, declined, call]
    talking.transitions = [verbal, declined, reached_out]
    verbal.transitions = [pulled_out, talking]
    declined.transitions = [talking]
    pulled_out.transitions = [talking]
    
    db.session.add(call)
    db.session.add(reached_out)
    db.session.add(talking)
    db.session.add(verbal)
    db.session.add(declined)
    db.session.add(pulled_out)
    db.session.commit()

def _init_designer_type():
    digital = DesignerType(name="digital")
    tabletop = DesignerType(name="tabletop")
    artist = DesignerType(name="artist")
    media = DesignerType(name="media")
    charity = DesignerType(name="charity")
    
    db.session.add(digital)
    db.session.add(tabletop)
    db.session.add(artist)
    db.session.add(media)
    db.session.add(charity)
    db.session.commit()

def _init_deal_level():
    indie = DealLevel(name="indie")
    copper = DealLevel(name="copper")
    silver = DealLevel(name="silver")
    gold = DealLevel(name="gold")
    platinum = DealLevel(name="platinum")
    
    db.session.add(indie)
    db.session.add(copper)
    db.session.add(silver)
    db.session.add(gold)
    db.session.add(platinum)
    db.session.commit()