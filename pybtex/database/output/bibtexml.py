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

from pybtex.core import Entry
from pybtex.database.output import WriterBase
from elementtree.SimpleXMLWriter import XMLWriter

file_extension = 'bibtexml'
doctype = """<!DOCTYPE bibtex:file PUBLIC
    "-//BibTeXML//DTD XML for BibTeX v1.0//EN"
        "bibtexml.dtd" >
"""
class Writer(WriterBase):
    """Outputs BibTeXML markup"""

    def write(self, bib_data, filename):
        def newline():
            w.data('\n')
        def write_persons(persons, role):
#            persons = entry.persons[role]
            if persons:
                newline()
                w.start('bibtex:' + role)
                for person in persons:
                    newline()
                    w.start('bibtex:person')
                    for type in ('first', 'middle', 'prelast', 'last', 'lineage'):
                        name = person.get_part_as_text(type)
                        if name:
                            newline()
                            w.element('bibtex:' + type, name)
                    newline()
                    w.end()
                newline()
                w.end()

        f = file(filename, 'w')
        w = XMLWriter(f, self.encoding)
        w.declaration()
        bibtex_file = w.start('bibtex:file', attrib={'xmlns:bibtex': 'http://bibtexml.sf.net/'})
        for key, entry in bib_data.entries.iteritems():
            newline()
            newline()
            w.start('bibtex:entry', id=key)
            newline()
            w.start('bibtex:' + entry.type)
            for field_name, field_value in entry.fields.iteritems():
                w.data('\n')
                w.element('bibtex:' + field_name, field_value)
            for role, persons in entry.persons.iteritems():
                write_persons(persons, role)
            newline()
            w.end()
            newline()
            w.end()
        newline()
        newline()
        w.comment('manual cleanup may be required')
        w.close(bibtex_file)
        w.flush()

        # XMLWriter does not add a newline at the end of file for some reason
        f.write('\n')
