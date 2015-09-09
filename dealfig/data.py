import datetime

from dealfig import model


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
    def get_all():
        # return model.Lead.all()
        return [
            _LeadData(_DesignerData("Foo 1")),
            _LeadData(_DesignerData("Foo 4")),
            _LeadData(_DesignerData("Foo 5")),
            _LeadData(_DesignerData("Foo 7")),
            _LeadData(_DesignerData("Foo 10")),
            _LeadData(_DesignerData("Foo 13"))
        ]
    
    @staticmethod
    def get_by_designer(name):
        # return model.Lead.query.filter_by(name=name).one()
        return _LeadData(_DesignerData("Foo 10"))


class DesignerTypes(object):
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
            _DesignerTypeData("Media")
        ]


##### Model Classes #####
# These classes are serving the purpose of model classes during development

class _DesignerData:
    def __init__(self, name):
        self.name = name
        self.id = 1
        self.type_name = "TYPE"
        self.notes = "NOTES"
        self.homepage = "http://google.com"
        self.contacts = [_Contact("Foo Bar", "foo@example.com"), _Contact("Baz Gah", "baz@example.com")]
        self.past_deals = []

class _DesignerTypeData:
    def __init__(self, name):
        self.id = 1
        self.name = name

class _Contact:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class _LeadData:
    def __init__(self, designer):
        self.id = 1
        self.created = datetime.datetime.now()
        self.designer = designer
        self.status = "In Talks"
        self.last_sent = datetime.datetime.now() - datetime.timedelta(days=1)
        self.last_received = datetime.datetime.now()
        self.contacts = [_Contact("Foo Bar", "foo@example.com")]
        self.comments = [
            _CommentData(_UserData("Test", "One", 1), "testing comment 1"),
            _CommentData(_UserData("Test", "One", 1), "testing comment 2"),
            _CommentData(_UserData("Test", "Three", 3), "testing comment 3")
        ]

class _CommentData:
    def __init__(self, user, text):
        self.id = 1
        self.user = user
        self.user_id = self.user.id
        self.timestamp = datetime.datetime.now()
        self.text = text

class _UserData:
    def __init__(self, first_name, last_name, id=None):
        self.id = id or 1
        self.first_name = first_name
        self.last_name = last_name
        self.enabled = True
        self.type_name = "sales"
        self.user_auth = _UserAuth((first_name[0] + last_name).lower())

class _UserAuth:
    def __init__(self, username):
        self.id = 1
        self.username = username
        self.password = "BLAH"
        self.reset_password_token = ''