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

import yaml
from pybtex.database.input import ParserBase
from pybtex.core import Entry, Person

file_extension = 'yaml'

class Parser(ParserBase):
    def parse_stream(self, stream):
        t = yaml.safe_load(stream)

        entries = ((key, self.process_entry(entry))
                for (key, entry) in t['entries'].iteritems())

        try:
            self.data.add_to_preamble(t['preamble'])
        except KeyError:
            pass

        self.data.add_entries(entries)

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
