import utils
from formatters import base, latex

class Formatter(base.Formatter):
    def format_authors(self, authors):
        l = []
        for author in authors:
            l.append(author.format([['f'], ['ll']]))
        return l

    def format_title(self, title):
        return utils.add_period(title)
       
    def format_article(self, e):
        l = []
        l.append(self.format_authors(e.authors))
        l.append(self.format_title(e['title']))
        pages = latex.dashify(e['pages'])
        if e.has_key('volume'):
            vp = "".join([e['volume'], utils.format(pages, ':%s')])
        else:
            vp = utils.format(pages, 'pages %s')
        l.append([latex.emph(e['journal']), vp, e['year']])
        return l
        
    def format_book(self, e):
        l = []
        if e.authors:
            l.append(self.format_authors(e.authors))
        else:
            editors = self.format_authors(e.editors)
            editors.append('editor')
            l.append(editors)
        l.append(latex.emph(self.format_title(e['title'])))
        p = utils.format(e['publisher'])
        y = utils.format(e['year'], '%s')
        l.append([e['publisher'], e['year']])
        return l
