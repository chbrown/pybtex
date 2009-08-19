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

try:
    import cElementTree as ET
except ImportError:
    try:
        from elementtree import ElementTree as ET
    except ImportError:
        from xml.etree import ElementTree as ET

from pybtex.core import Entry
from pybtex.database.output import WriterBase

file_extension = 'bibtexml'
doctype = """<!DOCTYPE bibtex:file PUBLIC
    "-//BibTeXML//DTD XML for BibTeX v1.0//EN"
        "bibtexml.dtd" >
"""

class PrettyTreeBuilder(ET.TreeBuilder):

    def __init__(self):
        ET.TreeBuilder.__init__(self)
        self.stack = []

    def newline(self):
        self.data('\n')

    def indent_line(self):
        self.data(' ' * len(self.stack) * 4)

    def start(self, tag, attrs=None, newline=True):
        if attrs is None:
            attrs = {}
        self.indent_line()
        self.stack.append(tag)
        ET.TreeBuilder.start(self, tag, attrs)
        if newline:
            self.newline()

    def end(self, indent=True):
        tag = self.stack.pop()
        if indent:
            self.indent_line()
        ET.TreeBuilder.end(self, tag)
        self.newline()

    def element(self, tag, data):
        self.start(tag, newline=False)
        self.data(data)
        self.end(indent=False)


class Writer(WriterBase):
    """Outputs BibTeXML markup"""

    def write_stream(self, bib_data, stream):
        def write_persons(persons, role):
            if persons:
                w.start('bibtex:' + role)
                for person in persons:
                    w.start('bibtex:person')
                    for type in ('first', 'middle', 'prelast', 'last', 'lineage'):
                        name = person.get_part_as_text(type)
                        if name:
                            w.element('bibtex:' + type, name)
                    w.end()
                w.end()

        w = PrettyTreeBuilder()
        bibtex_file = w.start('bibtex:file', {'xmlns:bibtex': 'http://bibtexml.sf.net/'})
        w.newline()

        for key, entry in bib_data.entries.iteritems():
            w.start('bibtex:entry', dict(id=key))
            w.start('bibtex:' + entry.type)
            for field_name, field_value in entry.fields.iteritems():
                w.element('bibtex:' + field_name, field_value)
            for role, persons in entry.persons.iteritems():
                write_persons(persons, role)
            w.end()
            w.end()
            w.newline()
        w.end()

        tree = ET.ElementTree(w.close())
        tree.write(stream, self.encoding)
        stream.write('\n')
