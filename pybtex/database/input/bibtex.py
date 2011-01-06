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

"""BibTeX parser

>>> import StringIO
>>> parser = Parser()
>>> bib_data = parser.parse_stream(StringIO.StringIO('''
... @String{SCI = "Science"}
... 
... @String{JFernandez = "Fernandez, Julio M."}
... @String{HGaub = "Gaub, Hermann E."}
... @String{MGautel = "Gautel, Mathias"}
... @String{FOesterhelt = "Oesterhelt, Filipp"}
... @String{MRief = "Rief, Matthias"}
... 
... @Article{rief97b,
...   author =       MRief #" and "# MGautel #" and "# FOesterhelt
...                  #" and "# JFernandez #" and "# HGaub,
...   title =        "Reversible Unfolding of Individual Titin
...                  Immunoglobulin Domains by {AFM}",
...   journal =      SCI,
...   volume =       276,
...   number =       5315,
...   pages =        "1109--1112",
...   year =         1997,
...   doi =          "10.1126/science.276.5315.1109",
...   URL =          "http://www.sciencemag.org/cgi/content/abstract/276/5315/1109",
...   eprint =       "http://www.sciencemag.org/cgi/reprint/276/5315/1109.pdf",
... }
... '''))
>>> rief97b = parser.data.entries['rief97b']
>>> authors = rief97b.persons['author']
>>> for author in authors:
...     print unicode(author)
Rief, Matthias
Gautel, Mathias
Oesterhelt, Filipp
Fernandez, Julio M.
Gaub, Hermann E.

"""

import babybib

import pybtex.io
from pybtex.core import Entry, Person
from pybtex.database.input import BaseParser
from pybtex.bibtex.utils import split_name_list
from pybtex.exceptions import PybtexError
from pybtex import textutils

month_names = {
    'jan': 'January',
    'feb': 'February',
    'mar': 'March',
    'apr': 'April',
    'may': 'May',
    'jun': 'June',
    'jul': 'July',
    'aug': 'August',
    'sep': 'September',
    'oct': 'October',
    'nov': 'November',
    'dec': 'December'
}


def normalize_whitespace(s, loc, toks):
    return [textutils.normalize_whitespace(tok) for tok in toks]


def flatten_bibtex_string(parts, macros):
    def _convert_to_string(parts):
        for part in parts:
            if isinstance(part, basestring):
                yield part
            elif isinstance(part, babybib.btparse.Macro):
                try:
                    yield macros[part.name]
                except KeyError:
                    raise PybtexError('undefined macro %s' % part.name)
            elif isinstance(part, list):
                yield '{'
                for result in _convert_to_string(part):
                    yield result
                yield '}'
            else:
                raise NotImplementedError(part) 

    return textutils.normalize_whitespace(''.join(_convert_to_string(parts)))


class Parser(BaseParser):
    name = 'bibtex'
    suffixes = '.bib',
    unicode_io = True

    def __init__(self, encoding=None, macros=month_names, person_fields=Person.valid_roles, **kwargs):
        BaseParser.__init__(self, encoding)

        self.default_macros = dict(macros)
        self.person_fields = person_fields

    def process_preamble(self, toks):
        self.data.add_to_preamble(toks[0])

    def process_entry(self, entry_type, key, fields, macros):
        entry = Entry(entry_type)

        if key is None:
            key = 'unnamed-%i' % self.unnamed_entry_counter
            self.unnamed_entry_counter += 1

        for field_name, field_values in fields.items():
            field_value = flatten_bibtex_string(field_values, macros)
            if field_name in self.person_fields:
                for name in split_name_list(field_value):
                    entry.add_person(Person(name), field_name)
            else:
                entry.fields[field_name] = field_value
#        return (key, entry)
        self.data.add_entry(key, entry)

    def substitute_macro(self, s, loc, toks):
        key = toks[0].lower()
        try:
            return self.macros[key]
        except KeyError:
            raise PybtexError('undefined macro %s' % key)

    def process_macro(self, s, loc, toks):
        self.macros[toks[0][0].lower()] = toks[0][1]

    def parse_stream(self, stream):
        parser = babybib.btparse.BibTeXParser(debug=False)
        results = parser.parse(stream.read())
        self.data.add_to_preamble(*results.preamble)
        macros = dict(self.default_macros)
        macros.update(results.defined_macros)
        for key, fields in results.entries.items():
            entry_type = fields.pop('entry type').lower()
            self.process_entry(entry_type, key, fields, macros)
        return self.data
