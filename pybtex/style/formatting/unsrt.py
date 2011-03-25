# Copyright (c) 2006, 2007, 2008, 2009, 2010, 2011  Andrey Golovizin
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re

from pybtex.style.formatting import BaseStyle, toplevel
from pybtex.style.template import (
    join, words, field, optional, first_of,
    names, sentence, tag, optional_field
)
from pybtex.richtext import Text, Symbol

def dashify(text):
    dash_re = re.compile(r'-+')
    return Text(Symbol('ndash')).join(dash_re.split(text))

pages = field('pages', apply_func=dashify)

date = words [optional_field('month'), field('year')]

class Style(BaseStyle):
    name = 'unsrt'

    def format_names(self, role):
        return sentence(capfirst=False) [names(role, sep=', ', sep2 = ' and ', last_sep=', and ')]

    def format_article(self, e):
        volume_and_pages = first_of [
            # volume and pages, with optional issue number
            optional [
                join [
                    field('volume'),
                    optional['(', field('number'),')'],
                    ':', pages
                ],
            ],
            # pages only
            words ['pages', pages],
        ]
        template = toplevel [
            self.format_names('author'),
            sentence(capfirst=False) [field('title')],
            sentence(capfirst=False) [
                tag('emph') [field('journal')],
                optional[ volume_and_pages ],
                date],
            optional[ sentence [ field('note') ] ],
        ]
        return template.format_data(e)
        
    def format_author_or_editor(self, e):
        return first_of [
            optional[ self.format_names('author') ],
            self.format_editor(e),
        ]

    def format_editor(self, e):
        editors = self.format_names('editor')
        if 'editor' not in e.persons:
            # when parsing the template, a FieldIsMissing exception
            # will be thrown anyway; no need to do anything now,
            # just return the template that will throw the exception
            return editors
        if len(e.persons['editor']) > 1:
            word = 'editors'
        else:
            word = 'editor'
        return words [editors, word]
    
    def format_volume_and_series(self, e):
        volume_and_series = optional [
            sentence(capfirst=False, sep=' ') [
                'Volume', field('volume'), optional [
                    words ['of', field('series')]
                ]
            ]
        ]
        number_and_series = optional [
            sentence(capfirst=False, sep=' ') [
                join(sep=Symbol('nbsp')) ['Number', field('number')],
                optional [
                    words ['in', field('series')]
                ]
            ]
        ]
        series = optional [ sentence(capfirst=False) [field('series')] ]
        return first_of [
                volume_and_series,
                number_and_series,
                series,
            ]
    
    def format_chapter_and_pages(self, e):
        return join(sep=', ') [
            optional [words ['chapter', field('chapter')]],
            optional [words ['pages', pages]],
        ]

    def format_book(self, e):
        template = toplevel [
            self.format_author_or_editor(e),
            tag('emph') [sentence [field('title')]],
            self.format_volume_and_series(e),
            sentence [field('publisher'), date],
        ]
        return template.format_data(e)

    def format_booklet(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
            sentence [
                optional_field('howpublished'),
                optional_field('address'),
                date,
                optional_field('note'),
            ]
        ]
        return template.format_data(e)

    def format_inbook(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [
                tag('emph') [field('title')],
                self.format_chapter_and_pages(e),
            ],
            self.format_volume_and_series(e),
            sentence [
                field('publisher'),
                optional_field('address'),
                optional [
                    words [field('edition'), 'edition']
                ],
                date,
                optional_field('note'),
            ]
        ]
        return template.format_data(e)

    # TODO quick stub, needs to be completed
    def format_incollection(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
        ]
        return template.format_data(e)

    def format_inproceedings(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
            words [
                'In',
                sentence(capfirst=False) [
                    optional[ self.format_editor(e) ],
                    tag('emph') [field('booktitle')],
                    self.format_volume_and_series(e),
                    optional[ pages ],
                ],
                # small difference from unsrt.bst here: unsrt.bst
                # starts a new sentence only if the address is missing
                # - for simplicity here we always start a new sentence
                first_of[
                    # this will be rendered if there is an address
                    optional[
                        sentence[
                            field('address'),
                            date,
                        ],
                        sentence[
                            optional_field('organization'),
                            optional_field('publisher'),
                        ],
                    ],
                    # if there is no address then we have this
                    sentence[
                        optional_field('organization'),
                        optional_field('publisher'),
                        date,
                    ],
                ],
            ],
            optional[ sentence [field('note')] ],
        ]
        return template.format_data(e)

    # TODO quick stub, needs to be completed
    def format_manual(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
        ]
        return template.format_data(e)

    # TODO quick stub, needs to be completed
    def format_mastersthesis(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
        ]
        return template.format_data(e)

    # TODO quick stub, needs to be completed
    def format_misc(self, e):
        template = toplevel [
            optional[ sentence [self.format_names('author')] ],
            sentence [optional_field('title')],
        ]
        return template.format_data(e)

    # TODO quick stub, needs to be completed
    def format_phdthesis(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
        ]
        return template.format_data(e)

    # TODO quick stub, needs to be completed
    def format_proceedings(self, e):
        template = toplevel [
            sentence [self.format_names('editor')],
            sentence [field('title')],
        ]
        return template.format_data(e)

    # TODO quick stub, needs to be completed
    def format_techreport(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
        ]
        return template.format_data(e)

    # TODO quick stub, needs to be completed
    def format_unpublished(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
            sentence [
                field('note'),
                optional[ date ]
            ],
        ]
        return template.format_data(e)
