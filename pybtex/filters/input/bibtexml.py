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

from elementtree import ElementTree as ET
from pybtex.core import Entry
bibtexns = '{http://bibtexml.sf.net/}'

def remove_ns(s):
    if s.startswith(bibtexns):
        return s[len(bibtexns):]

class Filter:
    file_extension = 'bibtexml'
    def __init__(self):
        self.entries = {}

    def parse_file(self, file):
        t = ET.parse(file)
        for entry in t.findall(bibtexns + 'entry'):
            self.process_entry(entry)
        return self.entries

    def process_entry(self, entry):
        def process_person(person_entry, role):
            persons = person_entry.findall(bibtexns + 'person')
            if persons:
                for person in persons:
                    e.add_person(person.text, role)
            else:
                e.add_person(person_entry.text, role)

        id_ = entry.get('id')
        item = entry.getchildren()[0]
        type = remove_ns(item.tag)
        e = Entry(type)
        for field in item.getchildren():
            field_name = remove_ns(field.tag)
            if field_name in Entry.valid_roles:
                process_person(field, field_name)
            else:
                e.fields[field_name] = field.text.strip()
        self.entries[id_] = e
