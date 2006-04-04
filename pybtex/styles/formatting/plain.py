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
from pybtex.styles.formatting import FormatterBase, default_phrase

class Formatter(FormatterBase):
    def format_names(self, persons):
        p = Phrase(sep=', ', sep2 = ' and ', last_sep=', and ')
        p.extend(person.text for person in persons)
        return p

    def format_date(self, entry):
        return Phrase(entry.month, entry.year, sep=' ')
    
    def format_article(self, e):
        p = default_phrase(self.format_names(e.authors), e.title)
        pages = dashify(e.pages)
        if e.volume:
            vp = RichText(e.volume, try_format(pages, ':%s'))
        else:
            vp = try_format(pages, 'pages %s')
        p.append(Phrase(Tag('emph', e.journal), vp, self.format_date(e)))
        return p
        
    def format_book(self, e):
        p = default_phrase()
        if e.authors:
            p.append(self.format_names(e.authors))
        else:
            editors = self.format_names(e.editors)
            if len(e.editors) > 1:
                word = 'editors'
            else:
                word = 'editor'
            p.append(Phrase(editors, word))
        p.append(Tag('emph', e.title))
        p.append(Phrase(e.publisher, self.format_date(e), add_period=True))
        return p
    def format_booklet(self, e):
        p = default_phrase(self.format_names(e.authors), e.title)
        p.append(Phrase(e.howpublished, e.address, self.format_date(e)))
        return p
