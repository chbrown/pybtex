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

import utils

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

    def __getitem__(self, name):
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
    def __init__(self, s):
        # TODO parse 'von' and 'jr'
        names = s.split()
        if len(names) == 1:
            self.first = []
            self.last = names
        else:
            self.first = names[:-1]
            self.last = [names[-1]]
    def get_part(self, type):
        parts = {'f' : self.first, 'l' : self.last}
        if len(type) == 1:
            return [utils.abbreviate(s) for s in parts[type]]
        else:
            return parts[type[0]]

    def format(self, format):
        """FIXME: create a class for formatting names instead of this
        """
        s = []
        space = '~'
        separator = ''
        for item in format:
            if len(item) == 1:
                type = item[0]
            elif len(item) == 2:
                separator, type = item
            elif len(item) == 3:
                separator, type, space = item
            else:
                # TODO proper error message
                return "wrong format"
            part = self.get_part(type)
            if part:
                s.append(separator + space.join(part))
            separator = ' '
        return "".join(s)
