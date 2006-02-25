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
        return self.fields[name]

    def add_author(self, author):
        self.authors.append(author)

class Author:
    def __init__(self, s):
        # TODO parse 'von' and 'jr'
        names = s.split()
        if len(names) == 1:
            self.first = None
            self.last = names[0]
        else:
            self.first = names[:-1]
            self.last = names[-1]
