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
# along with pybtex; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

from pybtex.utils import dashify
from pybtex.richtext import Text, Phrase, Tag, Symbol
from pybtex.styles.formatting import FormatterBase, default_phrase

class Formatter(FormatterBase):
    def format_names(self, persons):
        p = Phrase(sep=', ', sep2 = ' and ', last_sep=', and ')
        p.extend(person.text for person in persons)
        return p

    def format_date(self, e):
        return Phrase(e.fields['month'], e.fields['year'], sep=' ')
    
    def format_article(self, e):
        p = default_phrase(self.format_names(e.persons['author']), e.fields['title'])
        pages = dashify(e.fields['pages'])
        if e.fields['volume']:
            vp = Text(e.fields['volume'], Text(':', pages, check=True))
        else:
            vp = Phrase('pages', pages, check=True, sep=' ')
        p.append(Phrase(Tag('emph', e.fields['journal']), vp, self.format_date(e)))
        return p
        
    def format_author_or_editor(self, e):
        if e.persons['author']:
            return self.format_names(e.persons['author'])
        else:
            editors = self.format_names(e.persons['editors'])
            if len(editors) > 1:
                word = 'editors'
            else:
                word = 'editor'
            return Phrase(editors, word)
    
    def format_volume_and_series(self, e):
        p = Phrase(sep=' ')
        if e.fields['volume']:
            p.append('Volume')
            p.append(e.fields['volume'])
            if e.fields['series']:
                p.append('of')
                p.append(Tag('emph', e.fields['series']))

        elif e.fields.has_key('number'):
            p.append('Number')
            p.append(e.fields['number'])
            if e.fields['series']:
                p.append('in')
                p.append(e.fields['series'])
        elif e.fields['series']:
            p.append(e.fields['series'])
        return p
    
    def format_chapter_and_pages(self, e):
        p = Phrase()
        p.append(Phrase('chapter', e.fields['chapter'], sep=' '))
        p.append(Phrase('pages', dashify(e.fields['pages'])))
        return p

    def format_book(self, e):
        p = default_phrase(self.format_author_or_editor(e))
        p.append(Tag('emph', e.fields['title']))
        p.append(self.format_volume_and_series(e))
        p.append(Phrase(e.fields['publisher'], self.format_date(e), add_period=True))
        return p

    def format_booklet(self, e):
        p = default_phrase(self.format_names(e.persons['author']), e.fields['title'])
        p.append(Phrase(e.fields['howpublished'], e.fields['address'], self.format_date(e)), e.fields['note'])
        return p

    def format_inbook(self, e):
        p = default_phrase(self.format_author_or_editor(e))
        p.append(Phrase(Tag('emph', e.fields['title']), self.format_chapter_and_pages(e)))
        p.append(self.format_volume_and_series(e))
        p.append(Phrase(e.fields['publisher'], e.fields['address'], Phrase(e.fields['edition'], 'edition', sep=' ', check=True), self.format_date(e)))
        p.append(e.fields['note'])
        return p

    def format_incollection(self, e):
        p = default_phrase(self.format_names(e.persons['author']), e.fields['title'])
        tmp = Phrase()
        if e.fields['booktitle']:
            tmp.append('In', sep_after=' ')
            tmp.append(self.format_names(e.persons['editors']))
            tmp.append(Tag('emph', e.fields['booktitle']))
        tmp.append(self.format_volume_and_series(e))
        tmp.append
