from dealfig import model

class _DesignerData(object):
    def __init__(self, name):
        self.name = name
        self.id = 1
        self.type_name = "TYPE"
        self.notes = "NOTES"
        self.homepage = "http://google.com"
        self.contacts = [_Contact("Foo Bar", "foo@example.com"), _Contact("Baz Gah", "baz@example.com")]
        self.past_deals = []

class _DesignerTypeData(object):
    def __init__(self, name):
        self.id = 1
        self.name = name

class _Contact(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email

class Designers(object):
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