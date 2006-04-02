# Copyright 2006 Andrey Golovizin
#
# This file is part of pybtex.
#
# pybtex is free software; you can redistribute it and/or modify
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# pybtex is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rdiff-backup; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

from pybtex.utils import try_format, dashify
from pybtex.richtext import RichText, Phrase, Tag
from pybtex.formatters.styles import FormatterBase

class Formatter(FormatterBase):
    def format_authors(self, authors):
        p = Phrase(sep=', ', sep2 = ' and ', last_sep=', and ')
        for author in authors:
            a = Phrase(sep = ' ')
            a.append(author.get_part('f'))
            a.append(author.get_part('last'))
            p.append(a)
        return p

    def format_article(self, e):
        p = self.default_phrase(self.format_authors(e.authors), e.title)
        pages = dashify(e.pages)
        if e.has_key('volume'):
            vp = RichText(e.volume, try_format(pages, ':%s'))
        else:
            vp = try_format(pages, 'pages %s')
        p.append(Phrase(Tag('emph', e.journal), vp, e.year))
        return p
        
    def format_book(self, e):
        p = self.default_phrase()
        if e.authors:
            p.append(self.format_authors(e.authors))
        else:
            editors = self.format_authors(e.editors)
            if e.editors.count > 1:
                editors.append('editors')
            else:
                editors.append('editor')
            p.append(editors)
        p.append(Tag('emph', e.title))
        p.append(Phrase(e.publisher, e.year, add_period=True))
        return p
