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

import pybtex.io
from pybtex.database.output import WriterBase

file_extension = 'bib'

class Writer(WriterBase):
    """Outputs BibTeX markup"""

    def quote(self, s):
        return '"%s"' % s.replace('"', "''")

    def write_stream(self, bib_data, stream):
        def write_field(type, value):
            f.write(',\n    %s = %s' % (type, self.quote(value)))
        def format_name(person):
            def join(l):
                return ' '.join([name for name in l if name])
            first = person.get_part_as_text('first')
            middle = person.get_part_as_text('middle')
            prelast = person.get_part_as_text('prelast')
            last = person.get_part_as_text('last')
            lineage = person.get_part_as_text('lineage')
            s = '' 
            if last:
                s += join([prelast, last])
            if lineage:
                s += ', %s' % lineage
            if first or middle:
                s += ', '
                s += join([first, middle])
            return s
        def write_persons(persons, role):
#            persons = getattr(entry, role + 's')
            if persons:
                write_field(role, ' and '.join([format_name(person) for person in persons]))
        def write_preamble(preamble):
            if preamble:
                f.write('@preamble{%s}\n\n' % self.quote(preamble))

        f = pybtex.io.writer(stream, self.encoding)
        write_preamble(bib_data.preamble())
        for key, entry in bib_data.entries.iteritems():
            f.write('@%s' % entry.type)
            f.write('{\n')
            f.write('    %s' % key)
#            for role in ('author', 'editor'):
            for role, persons in entry.persons.iteritems():
                write_persons(persons, role)
            for type, value in entry.fields.iteritems():
                write_field(type, value)
            f.write('\n}\n\n')
