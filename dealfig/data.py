import datetime
import random
import string
from enum import Enum

# While testing, current_user is provided by a constant at the bottom of the page
# from flask.ext.login import current_user
from sqlalchemy import and_, not_, or_

from dealfig import model

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
        if designer:
            return designer
        else:
            designer_type = DesignerTypes.get(type_name)
            designer = model.Designer(name=name, type=designer_type)
            model.db.session.add(designer)
            model.db.session.commit()
            return designer
    
    @staticmethod
    def new(name, type_name):
        return data.Designers.get_or_create(name, type_name)
    
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
        contact = Contacts.save(contact_name, contact_email)
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
    def _get(designer, year=None):
        if not designer:
            return None

        year = year or datetime.datetime.today().year
        return model.Lead.query.filter_by(designer_id=designer.id, year=year).first()
    
    @staticmethod
    def get_by_designer(designer_name, year=None):
        designer = Designers.get_by_name(designer_name)
        return Leads._get(designer, year)
    
    @staticmethod
    def get_by_year(year=None):
        year = year or datetime.datetime.today().year
        return model.Lead.query.filter_by(year=year).all()

    @staticmethod
    def get_or_create(designer_name, year=None):
        designer = Designers.get_by_name(designer_name)
        lead = Leads._get(designer, year)
        if lead:
            return lead
        else:
            lead = model.Lead(year=datetime.datetime.today().year, status=LeadStatus.get_initial())
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

class Deals:
    @staticmethod
    def get_by_designer(name, year=None):
        lead = Leads.get_by_designer(name, year)
        if not lead:
            return None
        return lead.deal
    
    @staticmethod
    def get_by_year(year=None):
        year = year or datetime.datetime.today().year
        return model.Deal.query.filter(model.Deal.lead_id == model.Lead.id and model.Lead.year == year).all()
    
    @staticmethod
    def get_or_create(designer, year=None):
        lead = Leads.get_by_designer(designer, year)
        if not lead:
            return None

        deal = lead.deal
        if deal:
            return deal
        else:
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
    def _get(designer, year=None):
        if not designer:
            return None

        year = datetime.datetime.today().year
        return model.Showcase.query.filter_by(designer_id=designer.id).first()
    
    @staticmethod
    def get_all():
        return model.Showcase.query.all()

    @staticmethod
    def get_by_year(year=None):
        year = year or datetime.datetime.today().year
        return model.Showcase.query.filter_by(year=year)
    
    @staticmethod
    def get_by_designer(designer_name, year=None):
        designer = Designers.get_by_name(designer_name)
        return Showcases._get(designer, year)
    
    @staticmethod
    def get_or_create(designer_name):
        designer = Designers.get_by_name(designer_name)
        showcase = Showcases._get(designer)
        if showcase:
            return showcase
        else:
            showcase = model.Showcase(year=datetime.datetime.today().year)
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

class Exhibitor:
    @staticmethod
    def get_all():
        return [
            Exhibitor.get_by_designer("Foo 1"),
            Exhibitor.get_by_designer("Foo 4"),
            Exhibitor.get_by_designer("Foo 9")
        ]
    
    @staticmethod
    def get_by_year(year=None):
        return [
            Exhibitor.get_by_designer("Foo 1"),
            Exhibitor.get_by_designer("Foo 4"),
            Exhibitor.get_by_designer("Foo 9")
        ]
    
    @staticmethod
    def get_by_designer(name):
        if name == "Foo 1":
            return _ExhibitorData(_DesignerData(name), "bronze", "sponsor")
        elif name == "Foo 4":
            return _ExhibitorData(_DesignerData(name), "silver", "sponsor", [
                _AssetData("logo.png", "logo", _FileFormatData("PNG", "png"), id=1),
                _AssetData("foo.png", "image", _FileFormatData("PNG", "png"), _MediaTypeData("Newsletter", "Header"), id=2),
                _AssetData("web.png", "image", _FileFormatData("PNG", "png"), _MediaTypeData("Newsletter"), id=3),
                _AssetData("web.png", "logo", _FileFormatData("PNG", "png"), _MediaTypeData("Website"), id=5),
                _AssetData("description", "text", _FileFormatData("text", "txt"), id=4)
            ])
        else:
            return _ExhibitorData(_DesignerData(name), "showcase", "showcase")

class Contacts:
    @staticmethod
    def get_by_email(email):
        return model.Contact.query.filter_by(email=email).first()
    
    @staticmethod
    def get_or_create(name, email):
        contact = Contacts.get_by_email(email)
        if contact:
            contact.name = name
        else:
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

class AssetDefinition:
    @staticmethod
    def get_by_level(level):
        if level == "silver":
            return [
                _AssetDefinitionData("Newsletter Header", level, "image",
                    [_FileFormatData("PNG", "png"), _FileFormatData("JPEG", "jpeg")],
                    [_MediaTypeData("Newsletter", "Header")]
                ),
                _AssetDefinitionData("Website", level, "logo",
                    [_FileFormatData("PNG", "png"), _FileFormatData("JPEG", "jpeg")],
                    [_MediaTypeData("Website")]
                ),
                _AssetDefinitionData("Description", level, "text",
                    [_FileFormatData("text", "txt")],
                    [_MediaTypeData("Website")]
                )
            ]
        else:
            return [
                _AssetDefinitionData("Logo", level, "logo",
                    [_FileFormatData("PNG", "png")],
                    [_MediaTypeData("Program"), _MediaTypeData("Newsletter"), _MediaTypeData("Website"), _MediaTypeData("Digital Guide")]
                )
            ]
    
    @staticmethod
    def get_matches(asset_definition, assets):
        '''
        # base query
        def_no_location = asset_definition.media_types.filter(model.MediaType.location == None)
        def_with_location = asset_definition.media_types.filter(model.MediaType.location != None)
        matching_assets = assets \
            .filter(model.Asset.type == asset_definition.type) \
            .filter(model.Asset.format.in_(asset_definition.formats)) \
            .filter(or_(model.Asset.media_type == None,
                model.Asset.media_type.name.in_(def_no_location.query(model.MediaType.name)),
                model.Asset.media_type.in_(def_with_location),
                _and(model.Asset.media_type.location == None, model.Asset.media_type.name.in_(def_with_location.query(model.MediaType.name)))
            )) \
        .all()
        '''
        '''
        # splitting the table
        def_no_location = asset_definition.media_types.filter(model.MediaType.location == None)
        def_with_location = asset_definition.media_types.filter(model.MediaType.location != None)
        matching_assets_query = \
            _and(model.Asset.type == asset_definition.type,
                model.Asset.format.in_(asset_definition.formats),
                or_(model.Asset.media_type == None,
                    model.Asset.media_type.name.in_(def_no_location.query(model.MediaType.name)),
                    model.Asset.media_type.in_(def_with_location),
                    _and(model.Asset.media_type.location == None,
                        model.Asset.media_type.name.in_(def_with_location.query(model.MediaType.name)))
                ))
        matches = assets.filter(matching_assets_query).all()
        unmatched_assets = assets.filter(not_(matching_assets_query)).all()
        return matches, unmatched_assets
        '''
        matches = []
        unmatched_assets = []
        for asset in assets:
            if asset.type == asset_definition.type:
                matches.append(asset)
            else:
                unmatched_assets.append(asset)
        return matches, unmatched_assets

class Asset:
    pass


class Users:
    @staticmethod
    def get_all():
        return model.User.query.all()
    
    @staticmethod
    def get_by_role(role_name):
        return model.User.query.filter_by(role_name=role_name).all()
    
    @staticmethod
    def get_by_username(username):
        return model.User.query.filter(model.User.user_auth.has(username=username)).first()

    @staticmethod
    def get_or_create(username, role, first_name=None, last_name=None, email=None):
        user = Users.get_by_username(username)
        if user:
            return user
        else:
            new_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
            user_auth = model.UserAuth(username=username, password=model.user_manager.hash_password(new_password))
            user = model.User(role_name=role, user_auth=user_auth)
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if email:
                user.emails = [UserEmails.get_or_create(user, email)]
            model.db.session.add(user)
            model.db.session.commit()
            
            print(user.emails)
            
            return user
    
    @staticmethod
    def new(first_name, last_name, email, role, username=None):
        username = username or email.split('@')[0]
        return Users.get_or_create(username, role, first_name, last_name, email)
    
    @staticmethod
    def update_name(username, first_name, last_name):
        user = Users.get_by_username(username)
        user.first_name = first_name
        user.last_name = last_name
        model.db.session.commit()
        return user
    
    @staticmethod
    def update_role(username, role):
        user = Users.get_by_username(username)
        user.role = role
        model.db.session.commit()
        return user.role
    
    @staticmethod
    def update_email(username, email):
        user = Users.get_by_username(username)
        user.emails = [UserEmails.get_or_create(user, email)]
        model.db.session.commit()
        return user.emails[0].email
    
    @staticmethod
    def delete(username):
        user = model.User.query.filter(model.User.user_auth.has(username=username)).one()
        model.db.session.delete(user)
        model.db.session.commit()
        return user.username

class UserEmails:
    @staticmethod
    def get_or_create(user, email):
        user_email = model.UserEmail.query.filter_by(user_id=user.id, email=email).first()
        if user_email:
            return user_email
        else:
            user_email = model.UserEmail(email=email, is_primary=True)
            model.db.session.add(user_email)
            model.db.session.commit()
            return user_email


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

######################
# Other, non-DB data #
######################

class UserRoles(Enum):
    ADMIN = "admin"
    SALES = "sales"
    MARKETING = "marketing"
    
    def __init__(self, role):
        self.role = role
    

##### Model Classes #####
# These classes are serving the purpose of model classes during development

import random

class _ShowcaseData:
    def __init__(self, designer):
        self.designer = designer
        self.game_name = "Test game NAME"
        self.game_homepage = "http://amazon.com"
        self.game_description = "Description\nof the game"
    
    @property
    def level(self):
        return "Showcase"

class _ExhibitorData:
    def __init__(self, designer, level, type, assets=[]):
        self.designer = designer
        self.level = level
        self.type = type
        self.assets = assets
        
        for asset in self.assets:
            asset.exhibitor = self

class _AssetDefinitionData:
    def __init__(self, name, level, type, formats, media_types):
        self.id = random.randint(1, 100)
        self.name = name
        self.level = level
        self.type = type # text or image
        self.formats = formats
        self.media_types = media_types

class _FileFormatData:
    def __init__(self, name, ext):
        self.id = random.randint(1, 100)
        self.name = name
        self.ext = ext

class _MediaTypeData:
    def __init__(self, name, location=None):
        self.id = random.randint(1, 100)
        self.name = name
        self.location = location
    
    @property
    def display_name(self):
        if self.location:
            return "{} - {}".format(self.name, self.location)
        else:
            return self.name

class _AssetData:
    def __init__(self, filename, type, format, media_type=None, id=None):
        self.id = id or random.randint(1, 100)
        self.timestamp = datetime.datetime.now()
        self.filename = filename
        self.type = type
        self.format = format
        self.media_type = media_type
    
    def __hash__(self):
        return self.id
    
    def __eq__(self, other):
        return self.id == other.id


def get_or_create_current_user(username="dummy"):
    return Users.get_or_create("dummy", "admin")

current_user = get_or_create_current_user()