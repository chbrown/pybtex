# Copyright (C) 2006, 2007, 2008, 2009  Andrey Golovizin
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""pybtex' core datatypes
"""

import re

from pybtex.exceptions import PybtexError
from pybtex.bibtex.utils import split_tex_string

class FormattedEntry:
    """Formatted bibliography entry. Consists of
    - key (which is used for sorting);
    - label (which appears in the resulting bibliography)
    - text (usually RichText)
    """
    def __init__(self, key, text, label=None):
        self.key = key
        self.text = text
        self.label = label


class FieldDict(dict):
    def __init__(self, parent, *args, **kwargw):
        self.parent = parent
        dict.__init__(self, *args, **kwargw)
    def __missing__(self, key):
        if key in self.parent.persons:
            persons = self.parent.persons[key]
            return ' and '.join(unicode(person) for person in persons)
        elif 'crossref' in self:
            return self.parent.get_crossref().fields[key]
        else:
            raise KeyError(key)


class Entry(object):
    """Bibliography entry. Important members are:
    - persons (a dict of Person objects)
    - fields (all dict of string)
    """

    def __init__(self, type_, fields=None, persons=None, collection=None):
        if fields is None:
            fields = {}
        if persons is None:
            persons = {}
        self.type = type_
        self.fields = FieldDict(self, fields)
        self.persons = dict(persons)
        self.collection = collection

        # for BibTeX interpreter
        self.vars = {}

    def get_crossref(self):
        return self.collection.entries[self.fields['crossref']]

    def __eq__(self, other):
        if not isinstance(other, Entry):
            return super(Entry, self) == other
        return (
                self.fields == other.fields
                and self.persons == other.persons
        )

    def add_person(self, person, role):
        self.persons.setdefault(role, []).append(person)

class Person(object):
    """Represents a person (usually human).

    >>> p = Person('Avinash K. Dixit')
    >>> print p.first()
    ['Avinash']
    >>> print p.middle()
    ['K.']
    >>> print p.prelast()
    []
    >>> print p.last()
    ['Dixit']
    >>> print p.lineage()
    []
    >>> print unicode(p)
    Dixit, Avinash K.
    >>> p == Person(unicode(p))
    True
    >>> p = Person('Dixit, Jr, Avinash K. ')
    >>> print p.first()
    ['Avinash']
    >>> print p.middle()
    ['K.']
    >>> print p.prelast()
    []
    >>> print p.last()
    ['Dixit']
    >>> print p.lineage()
    ['Jr']
    >>> print unicode(p)
    Dixit, Jr, Avinash K.
    >>> p == Person(unicode(p))
    True

    >>> p = Person('abc')
    >>> print p.first(), p.middle(), p.prelast(), p.last(), p.lineage()
    [] [] [] ['abc'] []
    >>> p = Person('Viktorov, Michail~Markovitch')
    >>> print p.first(), p.middle(), p.prelast(), p.last(), p.lineage()
    ['Michail'] ['Markovitch'] [] ['Viktorov'] []
    """
    valid_roles = ['author', 'editor'] 
    style1_re = re.compile('^(.+),\s*(.+)$')
    style2_re = re.compile('^(.+),\s*(.+),\s*(.+)$')
    def __init__(self, string="", first="", middle="", prelast="", last="", lineage=""):
        self._first = []
        self._middle = []
        self._prelast = []
        self._last = []
        self._lineage = []
        string = string.strip()
        if string:
            self.parse_string(string)
        self._first.extend(split_tex_string(first))
        self._middle.extend(split_tex_string(middle))
        self._prelast.extend(split_tex_string(prelast))
        self._last.extend(split_tex_string(last))
        self._lineage.extend(split_tex_string(lineage))

    def parse_string(self, name):
        """Extract various parts of the name from a string.
        Supported formats are:
         - von Last, First
         - von Last, Jr, First
         - First von Last
        (see BibTeX manual for explanation)
        """
        def process_first_middle(parts):
            try:
                self._first.append(parts[0])
                self._middle.extend(parts[1:])
            except IndexError:
                pass

        def process_von_last(parts):
            i = 0
            for i, part in enumerate(reversed(parts[:-1])):
                if part.islower():
                    break
            pos = len(parts) - i - 1
            von = parts[:pos]
            last = parts[pos:]
            self._prelast.extend(von)
            self._last.extend(last)

        def split_at(lst, pred):
            """Split the given list into two parts.

            The second part starts with the first item for which the given
            predicate is True. If the predicate is False for all items, the
            last element still comes to the last part. This is how BibTeX
            parses names.

            """
            for i, item in enumerate(lst):
                if pred(item):
                    break
            return lst[:i], lst[i:]

        parts = split_tex_string(name, ',')
        if len(parts) == 3: # von Last, Jr, First
            process_von_last(split_tex_string(parts[0]))
            self._lineage.extend(split_tex_string(parts[1]))
            process_first_middle(split_tex_string(parts[2]))
        elif len(parts) == 2: # von Last, First
            process_von_last(split_tex_string(parts[0]))
            process_first_middle(split_tex_string(parts[1]))
        elif len(parts) == 1: # First von Last
            parts = split_tex_string(name)
            first_middle, von_last = split_at(parts, lambda part: part.islower())
            process_first_middle(first_middle)
            process_von_last(von_last)
        else:
            raise PybtexError('Invalid name format: %s' % name)

    def __eq__(self, other):
        if not isinstance(other, Person):
            return super(Person, self) == other
        return (
                self._first == other._first
                and self._middle == other._middle
                and self._prelast == other._prelast
                and self._last == other._last
                and self._lineage == other._lineage
        )

    def __unicode__(self):
        # von Last, Jr, First
        von_last = ' '.join(self._prelast + self._last)
        jr = ' '.join(self._lineage)
        first = ' '.join(self._first + self._middle)
        return ', '.join(part for part in (von_last, jr, first) if part)

    def get_part_as_text(self, type):
        names = getattr(self, '_' + type)
        return ' '.join(names)

    def get_part(self, type, abbr=False):
        names = getattr(self, '_' + type)
        if abbr:
            from pybtex.textutils import abbreviate
            names = [abbreviate(name) for name in names]
        return names

    #FIXME needs some thinking and cleanup
    def bibtex_first(self):
        """Return first and middle names together.
        (BibTeX treats all middle names as first)
        """
        return self._first + self._middle

    def first(self, abbr=False):
        return self.get_part('first', abbr)
    def middle(self, abbr=False):
        return self.get_part('middle', abbr)
    def prelast(self, abbr=False):
        return self.get_part('prelast', abbr)
    def last(self, abbr=False):
        return self.get_part('last', abbr)
    def lineage(self, abbr=False):
        return self.get_part('lineage', abbr)
