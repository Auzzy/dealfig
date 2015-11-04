import datetime

# While testing, current_user is provided by a constant at the bottom of the page
# from flask.ext.login import current_user

from dealfig import model


##### NOTES #####
# When querying for a Lead by name, it should return the most recent Lead. Older Leads can be retrieved by providing the year
# Lead.status will be some sort of state machine. I don't know how I'm going to re[present it yet, but it's gonna be hard coded - no configuration through the web page


class Designers:
    @staticmethod
    def get_all():
        # return model.Designer.all()
        return [
            _DesignerData("Foo 1"),
            _DesignerData("Foo 2"),
            _DesignerData("Foo 3"),
            _DesignerData("Foo 4"),
            _DesignerData("Foo 5"),
            _DesignerData("Foo 6"),
            _DesignerData("Foo 7"),
            _DesignerData("Foo 8"),
            _DesignerData("Foo 9"),
            _DesignerData("Foo 10"),
            _DesignerData("Foo 11"),
            _DesignerData("Foo 12"),
            _DesignerData("Foo 13")
        ]
    
    @staticmethod
    def get_by_name(name):
        # return model.Designer.query.filter_by(name=name).one()
        return _DesignerData(name)
    
    @staticmethod
    def save(name, form, contacts):
        return _DesignerData(name)

class Leads:
    @staticmethod
    def get_statuses():
        pass
    
    @staticmethod
    def get_all():
        # return model.Lead.all()
        return [
            _LeadData(_DesignerData("Foo 1"), _UserData("Foo", "Bar")),
            _LeadData(_DesignerData("Foo 4"), _UserData("Baz", "Bar")),
            _LeadData(_DesignerData("Foo 5"), _UserData("Foo", "Bat")),
            _LeadData(_DesignerData("Foo 7"), _UserData("Foo", "Baz")),
            _LeadData(_DesignerData("Foo 10"), _UserData("Qux", "Bar")),
            _LeadData(_DesignerData("Foo 13"), _UserData("Foo", "Bar"))
        ]
    
    @staticmethod
    def get_by_designer(name):
        # return model.Lead.query.filter_by(name=name).one()
        return _LeadData(_DesignerData(name), _UserData("Test", "Owner"))
    
    @staticmethod
    def update_status(designer, status):
        Leads.get_by_designer(designer).status = status
        return status

class Comment:
    @staticmethod
    def submit(lead, text, user=None):
        user = user or current_user
        comment = _CommentData(user, text)
        lead.comments.append(comment)
        return comment

class Deals:
    @staticmethod
    def get_all():
        # return model.Deal.all()
        return [
            _DealData(_LeadData(_DesignerData("Foo 1"), _UserData("Foo", "Bar"))),
            _DealData(_LeadData(_DesignerData("Foo 5"), _UserData("Foo", "Bat")), _UserData("Diff", "Owner")),
            _DealData(_LeadData(_DesignerData("Foo 10"), _UserData("Qux", "Bar")))
        ]
    
    @staticmethod
    def get_by_designer(name):
        # return model.Deal.query.filter_by(name=name).one()
        return _DealData(_LeadData(_DesignerData(name), _UserData("Test", "Designer")))

class Showcase:
    @staticmethod
    def get_all():
        return [
            _ShowcaseData(_DesignerData("Foo 2")),
            _ShowcaseData(_DesignerData("Foo 6")),
            _ShowcaseData(_DesignerData("Foo 9")),
            _ShowcaseData(_DesignerData("Foo 11")),
            _ShowcaseData(_DesignerData("Foo 12"))
        ]
    
    @staticmethod
    def get_by_designer(name):
        return _ShowcaseData(_DesignerData(name))

class Contract:
    @staticmethod
    def save_sent(deal, date):
        deal.contract.sent = date
        return deal.contract
    
    @staticmethod
    def save_signed(deal, date):
        deal.contract.signed = date
        return deal.contract

class Invoice:
    @staticmethod
    def save_sent(deal, date):
        deal.invoice.sent = date
        return deal.invoice
    
    @staticmethod
    def save_paid(deal, date):
        deal.invoice.paid = date
        return deal.invoice



class DesignerTypes:
    @staticmethod
    def as_options():
        return [(type.name, type.name) for type in DesignerTypes.get_all()]
    
    @staticmethod
    def get_all():
        # return model.DesignerType.all()
        return [
            _DesignerTypeData("Digital"),
            _DesignerTypeData("Tabletop"),
            _DesignerTypeData("Artist"),
            _DesignerTypeData("Media"),
            _DesignerTypeData("Charity")
        ]

class LeadStatus:
    @staticmethod
    def get_all():
        return [
            _LeadStatusData("To Call"),
            _LeadStatusData("Reached Out"),
            _LeadStatusData("In Talks"),
            _LeadStatusData("Verbal Deal"),
            _LeadStatusData("Declined"),
            _LeadStatusData("Pulled Out")
        ]
    
    @staticmethod
    def get_transitions(status):
        # return [name for name in model.LeadStatus.query.filter_by(name=status).transitions]
        return [
            _LeadStatusData("Verbal Deal"),
            _LeadStatusData("Decline")
        ]
    

##### Model Classes #####
# These classes are serving the purpose of model classes during development

class _DesignerData:
    def __init__(self, name):
        self.name = name
        self.id = 1
        self.type_name = "Digital"
        self.notes = "NOTES"
        self.homepage = "http://google.com"
        
        self.contacts = [_Contact("Foo Bar", "foo@example.com"), _Contact("Baz Gah", "baz@example.com")]
        self.leads = []

class _LeadData:
    def __init__(self, designer, owner):
        self.id = 1
        self.designer = designer
        self.owner = owner
        self.created = datetime.datetime.now()
        self.status = "In Talks"
        
        self.deal = None
        self.contacts = [_Contact("Foo Bar", "foo@example.com")]
        self.comments = [
            _CommentData(_UserData("Test", "One", 1), "testing comment 1", 1445470160),
            _CommentData(_UserData("Test", "One", 1), "testing comment 2", 1445463160),
            _CommentData(_UserData("Test", "Three", 3), "testing comment 3", 1445473160)
        ]

class _DealData:
    def __init__(self, lead, owner=None):
        self.id = 1
        self.lead = lead
        self.owner = owner if owner else lead.owner
        self.level = "Copper"
        self.cash = 300
        self.inkind = 0
        self.notes = "Speacial deal\nprovisions and\n\n\tOTHER STUFF"
        self.contract = _ContractData()
        self.invoice = _InvoiceData()
    
    @property
    def designer(self):
        return self.lead.designer
    
    @property
    def contract_signed(self):
        return bool(self.contract.signed)
    
    @property
    def invoice_paid(self):
        return bool(self.invoice.paid)

class _ShowcaseData:
    def __init__(self, designer):
        self.designer = designer
        self.game_name = "Test game NAME"
        self.game_homepage = "http://amazon.com"
        self.game_description = "Description\nof the game"

class _DesignerTypeData:
    def __init__(self, name):
        self.id = 1
        self.name = name

class _LeadStatusData:
    def __init__(self, name, transitions=[]):
        self.id = 1
        self.name = name
        self.transitions = transitions

class _Contact:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class _CommentData:
    def __init__(self, user, text, created=None):
        self.id = 1
        self.user = user
        self.user_id = self.user.id
        self.created = datetime.datetime.fromtimestamp(created) if created else datetime.datetime.now()
        self.text = text

class _ContractData:
    def __init__(self, sent=None, signed=None):
        self.id = 1
        self.sent = sent
        self.signed = signed

class _InvoiceData:
    def __init__(self, sent=None, paid=None):
        self.id = 1
        self.sent = sent
        self.paid = paid

class _UserData:
    def __init__(self, first_name, last_name, id=None):
        self.id = id or 1
        self.first_name = first_name
        self.last_name = last_name
        self.enabled = True
        self.type_name = "sales"
        self.user_auth = _UserAuth((first_name[0] + last_name).lower())
        self.deals = []
        self.leads = []

class _UserAuth:
    def __init__(self, username):
        self.id = 1
        self.username = username
        self.password = "BLAH"
        self.reset_password_token = ''




current_user = _UserData("Test", "Four", 4)