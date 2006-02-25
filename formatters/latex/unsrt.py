from formatters import utils, base

class Formatter(base.Formatter):
    def write_authors(self, authors):
        l = []
        for author in authors:
            l.append(author.last)
        self.output(utils.add_period(", ".join(l)))

    def write_title(self, title):
        self.output(utils.add_period(title))
       
    def write_article(self, entry):
        self.write_authors(entry.authors)
        self.newblock()
        self.write_title(entry['TITLE'])
        self.newblock()
        self.output('{\em ')
        self.output(entry['JOURNAL'])
        self.output('}')
        try:
            self.output(", " + utils.add_period(entry['YEAR']))
        except KeyError:
            pass
        
    def write_book(self, entry):
        self.write_authors(entry.authors)
        self.newblock()
        self.output('{\em ')
        self.write_title(entry['TITLE'])
        self.output('}')
        self.newblock()
        try:
            self.output(entry['PUBLISHER'])
            self.output(', ')
        except KeyError:
            pass
        try:
            self.output(utils.add_period(entry['YEAR']))
        except KeyError:
            pass
        
