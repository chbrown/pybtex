from pybtex import utils
from pybtex.utils import Pack
from pybtex.formatters.backends import latex
from pybtex.formatters.styles import FormatterBase

class Formatter(FormatterBase):
    def format_authors(self, authors):
        p = Pack()
        for author in authors:
            p.append(author.format([['f'], ['ll']]))
        return p

    def format_title(self, title):
        return utils.add_period(title)
       
    def format_article(self, e):
        p = Pack(sep=' ', add_period=True, add_periods=True)
        p.append(self.format_authors(e.authors))
        p.append(self.format_title(e['title']))
        pages = latex.dashify(e['pages'])
        if e.has_key('volume'):
            vp = "".join([e['volume'], utils.format(pages, ':%s')])
        else:
            vp = utils.format(pages, 'pages %s')
        p2 = Pack()
        p2.append(e['journal'], format=latex.emph)
        p2.append(vp)
        p2.append(e['year'])
        p.append(p2)
        return p
        
    def format_book(self, e):
        p = Pack(sep=' ', add_period=True, add_periods=True)
        if e.authors:
            p.append(self.format_authors(e.authors))
        else:
            editors = self.format_authors(e.editors)
            if e.editors.count > 1:
                editors.append('editors')
            else:
                editors.append('editor')
            p.append(editors)
        p.append(self.format_title(e['title']), format=latex.emph)
        p.append(Pack(e['publisher'], e['year'], add_period=True))
        return p
