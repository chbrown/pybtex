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

from pybtex.utils import dashify
from pybtex.richtext import Text, Phrase, Tag, Symbol
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
            vp = Text(e.volume, Text(':', pages, check=True))
        else:
            vp = Phrase('pages', pages, check=True, sep=' ')
        p.append(Phrase(Tag('emph', e.journal), vp, self.format_date(e)))
        return p
        
    def format_author_or_editor(self, e):
        if e.authors:
            return self.format_names(e.authors)
        else:
            editors = self.format_names(e.editors)
            if len(e.editors) > 1:
                word = 'editors'
            else:
                word = 'editor'
            return Phrase(editors, word)
    
    def format_volume_and_series(self, e):
        p = Phrase(sep=' ')
        if e.volume:
            p.append('Volume')
            p.append(e.volume)
            if e.series:
                p.append('of')
                p.append(Tag('emph', e.series))

        # we can not just use e.number here, because
        # pybtex uses e.number for its own needs
        elif e.fields.has_key('number'):
            p.append('Number')
            p.append(e.fields['number'])
            if e.series:
                p.append('in')
                p.append(e.series)
        elif e.series:
            p.append(e.series)
        return p
    
    def format_book(self, e):
        p = default_phrase(self.format_author_or_editor(e))
        p.append(Tag('emph', e.title))
        p.append(self.format_volume_and_series(e))
        p.append(Phrase(e.publisher, self.format_date(e), add_period=True))
        return p

    def format_booklet(self, e):
        p = default_phrase(self.format_names(e.authors), e.title)
        p.append(Phrase(e.howpublished, e.address, self.format_date(e)), e.note)
        return p

    def format_inbook(self, e):
        p = default_phrase(self.format_author_or_editor(e), e.title)
        p.append(self.format_volume_and_series(e))
        p.append(Phrase(e.publisher, e.address, Phrase(e.edition, 'edition', sep=' ', check=True), self.format_date(e)))
        p.append(e.note)
        return p
