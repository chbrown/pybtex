import utils
from formatters import base, latex

class Formatter(base.Formatter):
    def format_authors(self, authors):
        l = []
        for author in authors:
            l.append(author.format([['f'], ['ll']]))
        return utils.add_period(", ".join(l))

    def format_title(self, title):
        return utils.add_period(title)
       
    def format_article(self, entry):
        l = []
        l.append(self.format_authors(entry.authors))
        l.append(self.format_title(entry['title']))
        j = latex.emph(entry['journal'])
        y = utils.format(entry['year'], ', %s')
        l.append("%s%s" % (j, y))
        return l
        
    def format_book(self, entry):
        l = []
        l.append(self.format_authors(entry.authors))
        l.append(latex.emph(self.format_title(entry['title'])))
        p = utils.format(entry['publisher'])
        y = utils.format(entry['year'], ', %s')
        l.append("%s%s" % (p, y))
        return l
        
