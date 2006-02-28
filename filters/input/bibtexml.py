from elementtree import ElementTree as ET
from core import Entry, Author
bibtexns = '{http://bibtexml.sf.net/}'

def remove_ns(s):
    if s.startswith(bibtexns):
        return s[len(bibtexns):]

class Data:
    def __init__(self):
        self.records = {}
        self.strings = {}

class Filter:
    def __init__(self):
        self.data = Data()

    def parse_file(self, file):
        t = ET.parse(file)
        for entry in t.findall(bibtexns + 'entry'):
            self.process_entry(entry)
        return self.data

    def process_entry(self, entry):
        def process_author(author):
            persons = author.findall(bibtexns + 'person')
            if persons:
                for person in persons:
                    e.authors.append(Author(person.text))
            else:
                e.authors.append(Author(author.text))

        id_ = entry.get('id')
        item = entry.getchildren()[0]
        type = remove_ns(item.tag)
        e = Entry(type)
        for field in item.getchildren():
            field_name = remove_ns(field.tag)
            if field_name == 'AUTHOR':
                process_author(field)
            else:
                e.fields[field_name] = field.text.strip()
        self.data.records[id_] = e
