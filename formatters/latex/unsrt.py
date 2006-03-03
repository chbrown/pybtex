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
       
    def format_article(self, e):
        l = []
        l.append(self.format_authors(e.authors))
        l.append(self.format_title(e['title']))
        if e.has_key('volume'):
            vp = "".join([e['volume'], utils.format(e['pages'], ':%s')])
        else:
            vp = utils.format(e['pages'], 'pages %s')
        l.append([latex.emph(e['journal']), vp, e['year']])
        return l
        
    def format_book(self, entry):
        l = []
        l.append(self.format_authors(entry.authors))
        l.append(latex.emph(self.format_title(entry['title'])))
        p = utils.format(entry['publisher'])
        y = utils.format(entry['year'], '%s')
        l.append([entry['publisher'], entry['year']])
        return l
