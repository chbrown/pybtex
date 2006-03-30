from pybtex import utils
from pybtex.utils import Phrase
from pybtex.richtext import Tag, Character
from pybtex.formatters.styles import FormatterBase

class Formatter(FormatterBase):
    def format_authors(self, authors):
        p = Phrase()
        for author in authors:
            p.append(author.format([['f'], ['ll']]))
        return p

    def format_title(self, title):
        return utils.add_period(title)
       
    def format_article(self, e):
        p = Phrase(sep=' ', add_period=True, add_periods=True)
        p.append(self.format_authors(e.authors))
        p.append(Tag('emph', self.format_title(e['title'])))
        pages = utils.dashify(e['pages'])
        if e.has_key('volume'):
            vp = "".join([e['volume'], utils.format(pages, ':%s')])
        else:
            vp = utils.format(pages, 'pages %s')
        p.append(Phrase(e['journal'], vp, e['year']))
        return p
        
    def format_book(self, e):
        p = Phrase(sep=' ', add_period=True, add_periods=True)
        if e.authors:
            p.append(self.format_authors(e.authors))
        else:
            editors = self.format_authors(e.editors)
            if e.editors.count > 1:
                editors.append('editors')
            else:
                editors.append('editor')
            p.append(editors)
        p.append(Tag('emph', self.format_title(e['title'])))
        p.append(Phrase(e['publisher'], e['year'], add_period=True))
        return p
