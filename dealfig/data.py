import datetime
import random
import string
from enum import Enum

# While testing, current_user is provided by a constant at the bottom of the page
from flask.ext.security import current_user, utils
from sqlalchemy import and_, not_, or_

from dealfig import model

# Note that this object doesn't currently expose the end_date, start_time, or
# end_time properties of the underlying Event table. They are present in the
# model only to make future implementation super easy.
class Events:
    @staticmethod
    def get_all():
        return model.Event.query.all()
    
    @staticmethod
    def _get(name):
        return model.Event.query.filter_by(name=name).first()
    
    @staticmethod
    def get_by_name(event_name):
        return Events._get(event_name) if event_name else Events.active()

    @staticmethod
    def get_or_create(name, start_date):
        event = Events._get(name)
        if not event:
            event = model.Event(name=name, start_date=start_date)
            model.db.session.add(event)
            model.db.session.commit()
        return event
    
    @staticmethod
    def active():
        return model.Event.query.filter_by(active=True).first()
    
    @staticmethod
    def new(name, start_date):
        return Events.get_or_create(name, start_date)

    @staticmethod
    def update_start_date(name, start_date):
        event = Events._get(name)
        event.start_date = start_date
        model.db.session.commit()
        return event.start_date
    
    @staticmethod
    def update_end_date(name, end_date):
        event = Events._get(name)
        event.end_date = end_date
        model.db.session.commit()
        return event.end_date
    
    @staticmethod
    def update_start_time(name, start_time):
        event = Events._get(name)
        event.start_time = start_time
        model.db.session.commit()
        return event.start_time
    
    @staticmethod
    def update_end_time(name, end_time):
        event = Events._get(name)
        event.end_time = end_time
        model.db.session.commit()
        return event.end_time
    
    @staticmethod
    def update_location(name, location):
        event = Events._get(name)
        event.location = location
        model.db.session.commit()
        return event.location
    
    @staticmethod
    def update_description(name, description):
        event = Events._get(name)
        event.description = description
        model.db.session.commit()
        return event.description

class Designers:
    @staticmethod
    def get_all():
        return model.Designer.query.all()
    
    @staticmethod
    def get_by_name(name):
        return model.Designer.query.filter_by(name=name).first()
    
    @staticmethod
    def get_or_create(name, type_name):
        designer = Designers.get_by_name(name)
        if not designer:
            designer_type = DesignerTypes.get(type_name)
            designer = model.Designer(name=name, type=designer_type)
            model.db.session.add(designer)
            model.db.session.commit()
        return designer
    
    @staticmethod
    def new(name, type_name):
        return Designers.get_or_create(name, type_name)
    
    @staticmethod
    def update_type(name, designer_type):
        designer = Designers.get_by_name(name)
        designer.type = DesignerTypes.get(designer_type)
        model.db.session.commit()
        return str(designer.type)
    
    @staticmethod
    def update_homepage(name, homepage):
        designer = Designers.get_by_name(name)
        designer.homepage = homepage
        model.db.session.commit()
        return designer.homepage

    @staticmethod
    def update_notes(name, notes):
        designer = Designers.get_by_name(name)
        designer.notes = notes
        model.db.session.commit()
        return designer.notes
    
    @staticmethod
    def add_contact(name, contact_name, contact_email):
        designer = Designers.get_by_name(name)
        contact = Contacts.get_or_create(contact_name, contact_email)
        designer_contact_emails = [contact.email for contact in designer.contacts]
        if contact.email not in designer_contact_emails:
            designer.contacts.append(contact)
            model.db.session.commit()
        return contact
    
    @staticmethod
    def delete_contact(name, contact_email):
        designer = Designers.get_by_name(name)
        contact = designer.contacts.filter_by(email=contact_email).one()
        designer.contacts.remove(contact)
        model.db.session.commit()
        return contact.email

class Leads:
    @staticmethod
    def get_all():
        return model.Lead.query.all()

    @staticmethod
    def _get(designer, event):
        if not designer or not event:
            return None

        return event.leads.filter_by(designer_id=designer.id).first()

    @staticmethod
    def get_by_designer(designer_name, event_name=None):
        designer = Designers.get_by_name(designer_name)
        event = Events.get_by_name(event_name)
        return Leads._get(designer, event)

    @staticmethod
    def get_by_event(event_name=None):
        return Events.get_by_name(event_name).leads

    @staticmethod
    def get_or_create(designer_name):
        designer = Designers.get_by_name(designer_name)
        event = Events.active()
        lead = Leads._get(designer, event)
        if not lead:
            lead = model.Lead(year=datetime.datetime.today().year, status=LeadStatus.get_initial(), event=event)
            designer.leads.append(lead)
            model.db.session.commit()
        return lead
    
    @staticmethod
    def update_status(designer_name, status_name):
        lead = Leads.get_by_designer(designer_name)
        status = LeadStatus.get(status_name)
        if status not in lead.status.transitions:
            return lead.status
        lead.status = status
        model.db.session.commit()
        return status
    
    @staticmethod
    def update_owner(designer_name, owner_username):
        lead = Leads.get_by_designer(designer_name)
        lead.owner = Users.get_by_username(owner_username)
        model.db.session.commit()
        return str(lead.owner)

class Comments:
    @staticmethod
    def create(designer_name, text, user=None):
        lead = Leads.get_by_designer(designer_name)
        user = user or current_user
        comment = model.Comment(user_id=user.id, text=text, created=datetime.datetime.now())
        lead.comments.append(comment)
        model.db.session.commit()
        return comment
    
    @staticmethod
    def edit(id, text):
        comment = model.Comment.query.get(id)
        comment.text = text
        comment.edited = datetime.datetime.now()
        model.db.session.commit()
        return comment

    @staticmethod
    def delete(id):
        comment = model.Comment.query.get(id)
        model.db.session.delete(comment)
        model.db.session.commit()

class Deals:
    @staticmethod
    def get_by_designer(name, event_name=None):
        lead = Leads.get_by_designer(name, event_name)
        if not lead:
            return None
        return lead.deal

    @staticmethod
    def get_by_event(event_name=None):
        event = Events.get_by_name(event_name)
        return [lead.deal for lead in event.leads if lead.deal]

    @staticmethod
    def get_or_create(designer):
        lead = Leads.get_by_designer(designer)
        if not lead:
            return None

        deal = lead.deal
        if not deal:
            lead.deal = Deals.create()
            model.db.session.commit()
        return deal
    
    @staticmethod
    def create():
        deal = model.Deal()
        deal.contract = model.Contract()
        deal.invoice = model.Invoice()
        model.db.session.add(deal)
        model.db.session.commit()
        return deal
    
    @staticmethod
    def get_all():
        return model.Deal.query.all()

    @staticmethod
    def update_owner(designer_name, owner_username):
        deal = Deals.get_by_designer(designer_name)
        if not deal:
            return ""
        
        deal.owner = Users.get_by_username(owner_username)
        model.db.session.commit()
        return str(deal.owner)

    @staticmethod
    def update_level(designer_name, level_name):
        deal = Deals.get_by_designer(designer_name)
        if not deal:
            return ""
        
        deal.level = DealLevels.get(level_name)
        model.db.session.commit()
        return str(deal.level)

    @staticmethod
    def update_cash(designer_name, cash):
        deal = Deals.get_by_designer(designer_name)
        if not deal:
            return ""
        
        deal.cash = int(cash)
        model.db.session.commit()
        return str(deal.cash)

    @staticmethod
    def update_inkind(designer_name, inkind):
        deal = Deals.get_by_designer(designer_name)
        if not deal:
            return ""
        
        deal.inkind = inkind
        model.db.session.commit()
        return deal.inkind

    @staticmethod
    def update_notes(designer_name, notes):
        deal = Deals.get_by_designer(designer_name)
        if not deal:
            return ""
        
        deal.notes = notes
        model.db.session.commit()
        return deal.notes

class Showcases:
    @staticmethod
    def _get(designer, event):
        if not designer or not event:
            return None
        
        return event.showcase.filter_by(designer_id=designer.id).first()
    
    @staticmethod
    def get_all():
        return model.Showcase.query.all()

    @staticmethod
    def get_by_event(event_name=None):
        return Events.get_by_name(event_name).showcase
    
    @staticmethod
    def get_by_designer(designer_name, event_name=None):
        designer = Designers.get_by_name(designer_name)
        event = Events.get_by_name(event_name)
        return Showcases._get(designer, event)
    
    @staticmethod
    def get_or_create(designer_name):
        designer = Designers.get_by_name(designer_name)
        event = Events.active()
        showcase = Showcases._get(designer, event)
        if not showcase:
            showcase = model.Showcase(year=datetime.datetime.today().year, event=event)
            designer.showcase = showcase
            model.db.session.commit()
        return showcase

    def update_name(designer_name, game_name):
        showcase = Showcases.get_by_designer(designer_name)
        if not showcase:
            return ""
        
        showcase.game_name = game_name
        model.db.session.commit()
        return str(showcase.game_name)
    
    @staticmethod
    def update_homepage(designer_name, homepage):
        showcase = Showcases.get_by_designer(designer_name)
        if not showcase:
            return ""

        showcase.game_homepage = homepage
        model.db.session.commit()
        return showcase.game_homepage

    def update_description(designer, description):
        showcase = Showcases.get_by_designer(designer)
        if not showcase:
            return ""
        
        showcase.game_description = description
        model.db.session.commit()
        return str(showcase.game_description)

class Contacts:
    @staticmethod
    def get_by_email(email):
        return model.Contact.query.filter_by(email=email).first()
    
    @staticmethod
    def get_or_create(name, email):
        contact = Contacts.get_by_email(email)
        if not contact:
            contact = model.Contact(name=name, email=email)
            model.db.session.add(contact)
            model.db.session.commit()
        return contact
    
    @staticmethod
    def save(name, email):
        return Contacts.get_or_create(name, email)

class Contract:
    @staticmethod
    def save_sent(designer, date):
        deal = Deals.get_by_designer(designer)
        deal.contract.sent = date
        model.db.session.commit()
        return deal.contract.sent
    
    @staticmethod
    def save_signed(designer, date):
        deal = Deals.get_by_designer(designer)
        deal.contract.signed = date
        model.db.session.commit()
        return deal.contract.signed

class Invoice:
    @staticmethod
    def save_sent(designer, date):
        deal = Deals.get_by_designer(designer)
        deal.invoice.sent = date
        model.db.session.commit()
        return deal.invoice.sent
    
    @staticmethod
    def save_paid(designer, date):
        deal = Deals.get_by_designer(designer)
        deal.invoice.paid = date
        model.db.session.commit()
        return deal.invoice.paid

class Users:
    @staticmethod
    def get_all():
        return model.User.query.all()
    
    @staticmethod
    def get_by_role(role):
        return UserRoles.get(role).users
    
    @staticmethod
    def get_by_username(username):
        return model.User.query.filter_by(username=username).first()
    
    @staticmethod
    def create(username, email, role_names, first_name=None, last_name=None):
        new_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
        new_password_hash = utils.encrypt_password(new_password)
        user = model.user_datastore.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=new_password_hash)
        user.roles = [UserRoles.get(role_name) for role_name in role_names]
        model.db.session.commit()
        return user

    @staticmethod
    def get_or_create(username, email, role_names, first_name=None, last_name=None):
        user = Users.get_by_username(username)
        if user:
            return user
        else:
            return Users.create(username, email, role_names, first_name, last_name)
    
    @staticmethod
    def new(first_name, last_name, email, role_names, username=None):
        username = username or email.split('@')[0]
        return Users.get_or_create(username, email, role_names, first_name, last_name)
    
    @staticmethod
    def update_name(username, first_name, last_name):
        user = Users.get_by_username(username)
        user.first_name = first_name
        user.last_name = last_name
        model.db.session.commit()
        return user
    
    @staticmethod
    def update_roles(username, role_names):
        user = Users.get_by_username(username)
        if role_names:
            user.roles = [UserRoles.get(role_name) for role_name in role_names]
            model.db.session.commit()
        return user.role_names_str
    
    @staticmethod
    def update_email(username, email):
        user = Users.get_by_username(username)
        user.email = email
        model.db.session.commit()
        return user.email
    
    @staticmethod
    def delete(username):
        user = model.User.query.filter_by(username=username).one()
        model.db.session.delete(user)
        model.db.session.commit()
        return user.username

class DesignerTypes:
    @staticmethod
    def as_options():
        return [(type.name, type.name) for type in DesignerTypes.get_all()]
    
    @staticmethod
    def get_all():
        return model.DesignerType.query.all()

    @staticmethod
    def get(name):
        return model.DesignerType.query.filter_by(name=name).one()

class LeadStatus:
    @staticmethod
    def get_transition_names(status):
        return [state.name for state in model.LeadStatus.query.filter_by(name=status).one().transitions]
    
    @staticmethod
    def get(name):
        return model.LeadStatus.query.filter_by(name=name).one()

    @staticmethod
    def get_initial():
        return LeadStatus.get("To Call")

class DealLevels:
    @staticmethod
    def get_all():
        return model.DealLevel.query.all()
    
    @staticmethod
    def get(name):
        return model.DealLevel.query.filter_by(name=name).one()

class UserRoles:
    @staticmethod
    def get_all():
        return model.UserRole.query.all()
    
    @staticmethod
    def get(name):
        return model.UserRole.query.filter_by(name=name).one()

class Benefits:
    @staticmethod
    def get_by_level(deal_level):
        pass
    
    @staticmethod
    def get_by_showcase():
        pass