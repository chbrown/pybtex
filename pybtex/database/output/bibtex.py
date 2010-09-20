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
from pybtex.bibtex.exceptions import BibTeXError
from pybtex.bibtex.utils import scan_bibtex_string
from pybtex.database.output import WriterBase

file_extension = 'bib'


class Writer(WriterBase):
    """Outputs BibTeX markup"""

    unicode_io = True

    def quote(self, s):
        """
        >>> w = Writer()
        >>> print w.quote('The World')
        "The World"
        >>> print w.quote(r'The \emph{World}')
        "The \emph{World}"
        >>> print w.quote(r'The "World"')
        {The "World"}
        >>> try:
        ...     print w.quote(r'The {World')
        ... except BibTeXError, error:
        ...     print error
        String has unmatched braces: The {World
        """

        self.check_braces(s)
        if '"' not in s:
            return '"%s"' % s
        else:
            return '{%s}' % s

    def check_braces(self, s):
        end_brace_level = list(scan_bibtex_string(s))[-1][1]
        if end_brace_level != 0:
            raise BibTeXError('String has unmatched braces: %s' % s)

    def write_stream(self, bib_data, stream):
        def write_field(type, value):
            stream.write(u',\n    %s = %s' % (type, self.quote(value)))
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
                write_field(role, u' and '.join([format_name(person) for person in persons]))
        def write_preamble(preamble):
            if preamble:
                stream.write(u'@preamble{%s}\n\n' % self.quote(preamble))

        write_preamble(bib_data.preamble())
        for key, entry in bib_data.entries.iteritems():
            stream.write(u'@%s' % entry.type)
            stream.write(u'{\n')
            stream.write(u'    %s' % key)
#            for role in ('author', 'editor'):
            for role, persons in entry.persons.iteritems():
                write_persons(persons, role)
            for type, value in entry.fields.iteritems():
                write_field(type, value)
            stream.write(u'\n}\n\n')
