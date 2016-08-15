import collections
import datetime
import re
import sys

from sqlalchemy.ext.declarative import declared_attr
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from wtforms.validators import ValidationError

from dealfig import forms
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

showcase_benefit_to_image_asset_definition = db.Table('showcase_benefit_to_image_asset_definition',
    db.Column('showcase_beneit_id', db.Integer, db.ForeignKey('showcase_benefit.id')),
    db.Column('image_asset_definition_id', db.Integer, db.ForeignKey('image_asset_definition.id'))
)

showcase_benefit_to_text_asset_definition = db.Table('showcase_benefit_to_text_asset_definition',
    db.Column('showcase_benefit_id', db.Integer, db.ForeignKey('showcase_benefit.id')),
    db.Column('text_asset_definition_id', db.Integer, db.ForeignKey('text_asset_definition.id'))
)

sponsor_benefit_to_image_asset_definition = db.Table('sponsor_benefit_to_image_asset_definition',
    db.Column('sponsor_beneit_id', db.Integer, db.ForeignKey('sponsor_benefit.id')),
    db.Column('image_asset_definition_id', db.Integer, db.ForeignKey('image_asset_definition.id'))
)

sponsor_benefit_to_text_asset_definition = db.Table('sponsor_benefit_to_text_asset_definition',
    db.Column('sponsor_id', db.Integer, db.ForeignKey('sponsor_benefit.id')),
    db.Column('text_asset_definition_id', db.Integer, db.ForeignKey('text_asset_definition.id'))
)

image_asset_definition_to_file_format = db.Table('asset_definition_to_file_format',
    db.Column('image_asset_definition_id', db.Integer, db.ForeignKey('image_asset_definition.id')),
    db.Column('file_format_id', db.Integer, db.ForeignKey('file_format.id'))
)

asset_to_image_asset_definition = db.Table('asset_to_image_asset_definition',
    db.Column('image_asset_id', db.Integer, db.ForeignKey('image_asset.id')),
    db.Column('image_asset_definition_id', db.Integer, db.ForeignKey('image_asset_definition.id'))
)

user_to_role = db.Table('user_to_role',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('user_role_id', db.Integer(), db.ForeignKey('user_role.id'))
)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    location = db.Column(db.String(200), default="")
    description = db.Column(db.Text, default="")
    active = db.Column(db.Boolean)
    
    leads = db.relationship("Lead", backref="event", lazy="dynamic")
    showcase = db.relationship("Showcase", backref="event", lazy="dynamic")
    
    __table_args__ = (
        db.Index('one_active_event', id, active, unique=True, postgresql_where=(~active)),
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

    @property
    def active_lead(self):
        return self.leads.join(Lead.event).filter_by(active=True).first()

    @property
    def active_deal(self):
        return self.active_lead.deal
    
    @property
    def deals(self):
        return [lead.deal for lead in self.leads if lead.deal]
    
    @property
    def active_showcase(self):
        return self.showcase.join(Showcase.event).filter_by(active=True).first()

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
    
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

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
    def event(self):
        return self.lead.event
    
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
    
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(40), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="comments")
    created = db.Column(db.DateTime(), nullable=False)
    edited = db.Column(db.DateTime())
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

class Benefit:
    id = db.Column(db.Integer, primary_key=True)

class ShowcaseBenefit(db.Model, Benefit):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    image_assets = db.relationship("ImageAssetDefinition", secondary=showcase_benefit_to_image_asset_definition)
    text_assets = db.relationship("TextAssetDefinition", secondary=showcase_benefit_to_text_asset_definition)

class SponsorBenefit(db.Model, Benefit):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    image_assets = db.relationship("ImageAssetDefinition", secondary=sponsor_benefit_to_image_asset_definition)
    text_assets = db.relationship("TextAssetDefinition", secondary=sponsor_benefit_to_text_asset_definition)
    level_id = db.Column(db.Integer, db.ForeignKey('deal_level.id'), nullable=False)
    level = db.relationship("DealLevel")

class ImageAssetDefinition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    palette = db.Column(db.Enum("color", "black & white", native_enum=False))
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    size_unit = db.Column(db.Enum("inches", "pixels", native_enum=False))
    dpi = db.Column(db.Integer)
    formats = db.relationship("FileFormat", secondary=image_asset_definition_to_file_format)

    __table_args__ = (
        db.CheckConstraint("(width IS NULL AND height IS NULL AND size_unit IS NULL) OR (width IS NOT NULL AND height IS NOT NULL AND size_unit IS NOT NULL)"),
    )

class TextAssetDefinition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    max_length = db.Column(db.Integer)

class FileFormat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    ext = db.Column(db.String(10), unique=True)

class ImageAsset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    filename = db.Column(db.String(256), nullable=False)
    definitions = db.relationship('ImageAssetDefinition', secondary=asset_to_image_asset_definition, backref=db.backref('assets', lazy='dynamic'))

class TextAsset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text(), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(255), unique=True, index=True)
    password = db.Column(db.String(255), nullable=False, default='')
    active = db.Column(db.Boolean(), nullable=False, default=True)
    roles = db.relationship('UserRole', secondary=user_to_role, backref=db.backref('users', lazy='dynamic'))
    
    comments = db.relationship("Comment", back_populates="user", cascade="all, delete-orphan")

    @property
    def role_names(self):
        return [role.name for role in self.roles]

    @property
    def role_names_str(self):
        return ", ".join(self.role_names)
    
    @property
    def key(self):
        return self.username

    def __str__(self):
        return "{first} {last}".format(first=self.first_name, last=self.last_name)

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

class UserRole(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(255))

def password_validator(form, field):
    password = field.data
    if len(password) < 6:
        raise ValidationError("Password must have at least 6 characters.")

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, UserRole)
user_manager = Security(app, user_datastore, login_form=forms.UsernameEmailLoginForm)

def _create():
    db.create_all()
    _init_lead_status()
    _init_designer_type()
    _init_deal_level()
    _init_user_role()
    _init_benefits()

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
    
    _add_if_missing([call, reached_out, talking, verbal, declined, pulled_out], LeadStatus, "name")

def _init_designer_type():
    digital = DesignerType(name="digital")
    tabletop = DesignerType(name="tabletop")
    artist = DesignerType(name="artist")
    media = DesignerType(name="media")
    charity = DesignerType(name="charity")
    
    _add_if_missing([digital, tabletop, artist, media, charity], DesignerType, "name")

def _init_deal_level():
    indie = DealLevel(name="indie")
    indie = DealLevel(name="indie plus")
    bronze = DealLevel(name="bronze")
    silver = DealLevel(name="silver")
    gold = DealLevel(name="gold")
    platinum = DealLevel(name="platinum")
    
    _add_if_missing([indie, bronze, silver, gold, platinum], DealLevel, "name")

def _init_user_role():
    admin = UserRole(name="admin", description="An administrator of the site. They have full permissions to see and modify everything.")
    sales = UserRole(name="sales", description="A member of the sales team. Can be assigned a lead or deal, as well as update its status.")
    marketing = UserRole(name="marketing", description="Able to see the deal's state, as well as the benefits that deal affords them. Can also upload assets assocaited with a deal.")
    
    _add_if_missing([admin, sales, marketing], UserRole, "name")

def _init_benefits():
    def _init_benefits_file_formats():
        png_format = FileFormat(name="PNG", ext="png")
        pdf_format = FileFormat(name="PDF", ext="pdf")
        
        _add_if_missing([png_format, pdf_format], FileFormat, "ext")
    
    def _init_benefits_asset_definitions():
        png_format = FileFormat.query.filter_by(ext="png").one()
        pdf_format = FileFormat.query.filter_by(ext="pdf").one()
        
        description_def = TextAssetDefinition(name="Description")
        website_def = TextAssetDefinition(name="Website")
        logo_def = ImageAssetDefinition(name="Logo", palette="color", formats=[png_format])
        quarter_page_ad = ImageAssetDefinition(name="Quarter Page Ad", palette="black & white", width="8.5", height="2.5", size_unit="inches", formats=[png_format, pdf_format])
        half_page_ad = ImageAssetDefinition(name="Half Page Ad", palette="black & white", width="8.5", height="5.5", size_unit="inches", formats=[png_format, pdf_format])
        full_page_ad = ImageAssetDefinition(name="Full Page Ad", palette="color", width="8", height="11", size_unit="inches", formats=[png_format, pdf_format])
        two_page_ad = ImageAssetDefinition(name="Double-wide Ad", palette="color", width="16", height="11", size_unit="inches",  formats=[png_format, pdf_format])
        
        _add_if_missing([logo_def, quarter_page_ad, half_page_ad, full_page_ad, two_page_ad], ImageAssetDefinition, "name")
        _add_if_missing([description_def, website_def], TextAssetDefinition, "name")
    
    _init_benefits_file_formats()
    _init_benefits_asset_definitions()

    description_def = TextAssetDefinition.query.filter_by(name="Description").one()
    website_def = TextAssetDefinition.query.filter_by(name="Website").one()
    logo_def = ImageAssetDefinition.query.filter_by(name="Logo").one()
    quarter_page_ad = ImageAssetDefinition.query.filter_by(name="Quarter Page Ad").one()
    half_page_ad = ImageAssetDefinition.query.filter_by(name="Half Page Ad").one()
    full_page_ad = ImageAssetDefinition.query.filter_by(name="Full Page Ad").one()
    two_page_ad = ImageAssetDefinition.query.filter_by(name="Double-wide Ad").one()

    indie = SponsorBenefit(name="Indie Benefits", level=DealLevel.query.filter_by(name="indie").one(), image_assets=[logo_def], text_assets=[description_def, website_def])
    indie_plus = SponsorBenefit(name="Indie Plus Benefits", level=DealLevel.query.filter_by(name="indie plus").one(), image_assets=indie.image_assets, text_assets=indie.text_assets)
    bronze = SponsorBenefit(name="Bronze Benefits", level=DealLevel.query.filter_by(name="bronze").one(), image_assets=indie.image_assets + [quarter_page_ad], text_assets=indie.text_assets)
    silver = SponsorBenefit(name="Silver Benefits", level=DealLevel.query.filter_by(name="silver").one(), image_assets=indie.image_assets + [half_page_ad], text_assets=indie.text_assets)
    gold = SponsorBenefit(name="Gold Benefits", level=DealLevel.query.filter_by(name="gold").one(), image_assets=indie.image_assets + [full_page_ad], text_assets=indie.text_assets)
    platinum = SponsorBenefit(name="Platinum Benefits", level=DealLevel.query.filter_by(name="platinum").one(), image_assets=indie.image_assets + [two_page_ad], text_assets=indie.text_assets)
    showcase = ShowcaseBenefit(name="Showcase Benefits", image_assets=indie.image_assets, text_assets=indie.text_assets)

    _add_if_missing([indie, indie_plus, bronze, silver, gold, platinum], SponsorBenefit, "name")
    _add_if_missing([showcase], ShowcaseBenefit, "name")

def _add_if_missing(rows, Table, column="name"):
    for row in rows:
        if not db.session.query(db.exists().where(getattr(Table, column) == getattr(row, column))).scalar():
            db.session.add(row)
    db.session.commit()