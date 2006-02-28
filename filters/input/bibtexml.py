from elementtree import ElementTree as ET
from core import Entry, Author
bibtexns = '{http://bibtexml.sf.net/}'

def remove_ns(s):
    if s.startswith(bibtexns):
        return s[len(bibtexns):]

class Filter:
    def __init__(self):
        self.entries = {}

    def parse_file(self, file):
        t = ET.parse(file)
        for entry in t.findall(bibtexns + 'entry'):
            self.process_entry(entry)
        return self.entries

    def process_entry(self, entry):
        def process_author(author):
            persons = author.findall(bibtexns + 'person')
            if persons:
                for person in persons:
                    e.add_author(Author(person.text))
            else:
                e.add_author(Author(author.text))

        id_ = entry.get('id')
        item = entry.getchildren()[0]
        type = remove_ns(item.tag)
        e = Entry(type)
        for field in item.getchildren():
            field_name = remove_ns(field.tag)
            if field_name == 'author':
                process_author(field)
            else:
                e.fields[field_name] = field.text.strip()
        self.entries[id_] = e
