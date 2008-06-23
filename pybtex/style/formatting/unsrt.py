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

#from pybtex.utils import dashify
import re

from pybtex.style.formatting import FormatterBase, Toplevel
from pybtex.style.template import (
    Join, List, Words, Field, Optional, FirstOf,
    Names, Sentence, Tag, OptionalField
)
from pybtex.richtext import Text, Symbol

def dashify(text):
    dash_re = re.compile(r'-+')
    return Text(Symbol('ndash')).join(dash_re.split(text))

pages = Field('pages', apply_func=dashify)

date = Words [OptionalField('month'), Field('year')]

class Formatter(FormatterBase):
    def format_names(self, role):
        return Sentence(capfirst=False) [Names(role, sep=', ', sep2 = ' and ', last_sep=', and ')]

    def format_article(self, e):
        if e.fields['volume']:
            vp = Join [Field('volume'), Optional [':', pages]]
        else:
            vp = Words ['pages', Optional [pages]]
        format = Toplevel [
            self.format_names('author'),
            Sentence [Field('title')],
            Sentence [
                Tag('emph') [Field('journal')], vp, date],
        ]
        return format.format_data(e)
        
    def format_author_or_editor(self, e):
        if e.persons['author']:
            return self.format_names('author')
        else:
            editors = self.format_names('editors')
            if len(e.persons['editors']) > 1:
                word = 'editors'
            else:
                word = 'editor'
            return Words [editors, word]
    
    def format_volume_and_series(self, e):
        volume_and_series = Optional [
            Sentence(capfirst=False, sep=' ') [
                'Volume', Field('volume'), Optional [
                    Words ['of', Field('series')]
                ]
            ]
        ]
        number_and_series = Optional [
            Sentence(capfirst=False, sep=' ') [
                'Number', Field('number'), Optional [
                    Words ['in', Field('series')]
                ]
            ]
        ]
        series = Optional [ Sentence(capfirst=False) [Field('series')] ]
        return FirstOf [
                volume_and_series,
                number_and_series,
                series,
            ]
    
    def format_chapter_and_pages(self, e):
        return List [
            Optional [Words ['chapter', Field('chapter')]],
            Optional [Words ['pages', pages]],
        ]

    def format_book(self, e):
        format = Toplevel [
            self.format_author_or_editor(e),
            Tag('emph') [Sentence [Field('title')]],
            self.format_volume_and_series(e),
            Sentence [Field('publisher'), date],
        ]
        return format.format_data(e)

    def format_booklet(self, e):
        format = Toplevel [
            Sentence [self.format_names('author')],
            Sentence [Field('title')],
            Sentence [
                OptionalField('howpublished'),
                OptionalField('address'),
                date,
                OptionalField('note'),
            ]
        ]
        return format.format_data(e)

    def format_inbook(self, e):
        format = Toplevel [
            Sentence [self.format_names('author')],
            Sentence [
                Tag('emph') [Field('title')],
                self.format_chapter_and_pages(e),
            ],
            self.format_volume_and_series(e),
            Sentence [
                Field('publisher'),
                OptionalField('address'),
                Optional [
                    Words [Field('edition'), 'edition']
                ],
                date,
                OptionalField('note'),
            ]
        ]
        return format.format_data(e)
