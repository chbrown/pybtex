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
from pybtex.core import Entry
from pybtex.database.output import WriterBase

file_extension = 'yaml'
doctype = """<!DOCTYPE bibtex:file PUBLIC
    "-//BibTeXML//DTD XML for BibTeX v1.0//EN"
        "bibtexml.dtd" >
"""
class Writer(WriterBase):
    """Outputs YAML markup"""

    def write_stream(self, bib_data, stream):
        def process_person_roles(entry):
            for role, persons in entry.persons.iteritems():
                yield role, list(process_persons(persons))

        def process_person(person):
            for type in ('first', 'middle', 'prelast', 'last', 'lineage'):
                name = person.get_part_as_text(type)
                if name:
                    yield type, name

        def process_persons(persons):
            for person in persons:
                yield dict(process_person(person))
                
        def process_entries(bib_data):
            for key, entry in bib_data.iteritems():
                fields = dict(entry.fields)
                fields['type'] = entry.type
                fields.update(process_person_roles(entry))
                yield key, fields

        data = {'entries': dict(process_entries(bib_data.entries))}
        preamble = bib_data.preamble()
        if preamble:
            data['preamble'] = preamble
        yaml.safe_dump(data, stream, allow_unicode=True, default_flow_style=False, indent=4)
