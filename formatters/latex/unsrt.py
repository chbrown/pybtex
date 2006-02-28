import utils
from formatters import base

class Formatter(base.Formatter):
    def write_authors(self, authors):
        l = []
        for author in authors:
            l.append(author.format([['f'], ['ll']]))
        self.output(utils.add_period(", ".join(l)))

    def write_title(self, title):
        self.output(utils.add_period(title))
       
    def write_article(self, entry):
        self.write_authors(entry.authors)
        self.newblock()
        self.write_title(entry['title'])
        self.newblock()
        self.output('{\em ')
        self.output(entry['title'])
        self.output('}')
        try:
            self.output(", " + utils.add_period(entry['year']))
        except KeyError:
            pass
        
    def write_book(self, entry):
        self.write_authors(entry.authors)
        self.newblock()
        self.output('{\em ')
        self.write_title(entry['title'])
        self.output('}')
        self.newblock()
        try:
            self.output(entry['publisher'])
            self.output(', ')
        except KeyError:
            pass
        try:
            self.output(utils.add_period(entry['year']))
        except KeyError:
            pass
        
