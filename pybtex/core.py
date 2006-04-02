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

"""pybtex' core datatypes
"""

import re
import utils
from richtext import Phrase, Symbol

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

class Entry:
    """Bibliography entry. Important members are:
    - authors (a list of Person objects)
    - editors (like authors, but contains editors)
    - fields (all other information)
    """
    valid_roles = ['author', 'editor'] 
    def __init__(self, type_, fields = None):
        self.type = type_
        if fields == None:
            fields = {}
        self.fields = fields
        self.has_key = self.fields.has_key
        self.authors = []
        self.editors = []

    def __getattr__(self, name):
        try:
            return self.fields[name]
        except KeyError:
            return ""

    def add_person(self, person, role):
        """Add an author or an editor.
        """
        if not isinstance(person, Person):
            person = Person(person)
        list = getattr(self, '%ss' % role)
        list.append(person)
                

class Person:
    """Represents a person (usually human).
    """
    style1_re = re.compile('^(.+),\s*(.+)$')
    style2_re = re.compile('^(.+),\s*(.+),\s*(.+)$')
    def __init__(self, s):
        self._first = []
        self._middle = []
        self._prelast = []
        self._last = []
        self._lineage = []
        self.parse_string(s)

    def parse_string(self, s):
        """Extract various parts of the name from a string.
        Supported formats are:
         - von Last, First
         - von Last, Jr, First
         - First von Last
        (see BibTeX manual for explanation)
        """
        def process_von_last(s):
            for part in s.split():
                if part.islower():
                    self._prelast.append(part)
                else:
                    self._last.append(part)
        match1 = self.style1_re.match(s)
        match2 = self.style2_re.match(s)
        if match2: # von Last, Jr, First
            parts = match2.groups()
            process_von_last(parts[0])
            self._lineage.extend(parts[1].split())
            self._first.extend(parts[2].split())
        elif match1: # von Last, First
            parts = match1.groups()
            process_von_last(parts[0])
            self._first.extend(parts[1].split())
        else: # First von Last
            parts = reversed(s.split())
            self._last.append(parts.next())
            for part in parts:
                if part.islower():
                    self._prelast.insert(0, part)
                else:
                    self._first.insert(0, part)

    def get_part(self, type, abbr=False):
        names = getattr(self, '_' + type)
        if abbr:
            names = [utils.abbreviate(name) for name in names]
        p = Phrase(sep=Symbol('nbsp'))
        p.extend(names)
        return p
    def first(self, abbr=False):
        return self.get_part('first', abbr)
    def middle(self, abbr=False):
        return self.get_part('middle', abbr)
    def prelast(self, abbr=False):
        return self.get_part('middle', abbr)
    def last(self, abbr=False):
        return self.get_part('last', abbr)
    def lineage(self, abbr=False):
        return self.get_part('lineage', abbr)
