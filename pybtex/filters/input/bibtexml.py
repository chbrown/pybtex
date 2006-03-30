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
