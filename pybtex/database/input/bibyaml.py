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

import yaml
from pybtex.core import Entry, Person

file_extension = 'yaml'

class Parser:
    def __init__(self, encoding=None):
        self.entries = {}

    def parse_file(self, filename):
        f = open(filename)
        t = yaml.load(f)
        entries = ((key, self.process_entry(entry)) for (key, entry) in t['data'].iteritems())
        d = dict(entries)
        return d

    def process_entry(self, entry):
        e = Entry(entry['type']) 
        for (k, v) in entry.iteritems():
            if k in Entry.valid_roles:
                for names in v:
                    e.add_person(Person(**names), k)
            elif k == 'type':
                pass
            else:
                e.fields[k] = v
        return e
