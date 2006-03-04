import utils

class Entry:
    def __init__(self, type_, fields = None):
        self.type = type_
        if fields == None:
            fields = {}
        self.fields = fields
        self.has_key = self.fields.has_key
        self.authors = []
        self.editors = []

    def __getitem__(self, name):
        try:
            return self.fields[name]
        except KeyError:
            return ""

    def add_author(self, author):
        self.add_person(author, 'author')

    def add_editor(self, editor):
        self.add_person(editor, 'editor')
    
    def add_person(self, person, role):
        if not isinstance(person, Person):
            person = Person(person)
        list = getattr(self, '%ss' % role)
        list.append(person)
                

class Person:
    def __init__(self, s):
        # TODO parse 'von' and 'jr'
        names = s.split()
        if len(names) == 1:
            self.first = []
            self.last = names
        else:
            self.first = names[:-1]
            self.last = [names[-1]]
    def get_part(self, type):
        parts = {'f' : self.first, 'l' : self.last}
        if len(type) == 1:
            return [utils.abbreviate(s) for s in parts[type]]
        else:
            return parts[type[0]]

    def format(self, format):
        """format is like this:
        [['ff'], [
        """
        s = []
        space = '~'
        separator = ''
        for item in format:
            if len(item) == 1:
                type = item[0]
            elif len(item) == 2:
                separator, type = item
            elif len(item) == 3:
                separator, type, space = item
            else:
                # TODO proper error message
                return "wrong format"
            part = self.get_part(type)
            if part:
                s.append(separator + space.join(part))
            separator = ' '
        return "".join(s)
