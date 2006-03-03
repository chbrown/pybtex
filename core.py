import utils

class Entry:
    def __init__(self, type_, fields = None, authors = []):
        self.type = type_
        if fields == None:
            fields = {}
        self.fields = fields
	self.authors = []
	for author in authors:
            self.add_author(author)

    def __getitem__(self, name):
        try:
            return self.fields[name]
        except IndexError:
            return ""

    def add_author(self, author):
        if not isinstance(author, Author):
            author = Author(author)
        self.authors.append(author)

class Author:
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
