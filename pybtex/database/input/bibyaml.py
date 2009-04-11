# Copyright (C) 2006, 2007, 2008  Andrey Golovizin
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
from pybtex.database.input import ParserBase
from pybtex.core import Entry, Person
from pybtex.database import BibliographyData

file_extension = 'yaml'

class Parser(ParserBase):
    def parse_stream(self, stream):
        t = yaml.safe_load(stream)

        data = BibliographyData()
        entries = ((key, self.process_entry(entry))
                for (key, entry) in t['entries'].iteritems())

        try:
            data.add_to_preamble(t['preamble'])
        except KeyError:
            pass

        data.add_entries(entries)
        return data

    def process_entry(self, entry):
        e = Entry(entry['type']) 
        for (k, v) in entry.iteritems():
            if k in Person.valid_roles:
                for names in v:
                    e.add_person(Person(**names), k)
            elif k == 'type':
                pass
            else:
                e.fields[k] = unicode(v)
        return e
