from elementtree.SimpleXMLWriter import XMLWriter

doctype = """<!DOCTYPE bibtex:file PUBLIC
    "-//BibTeXML//DTD XML for BibTeX v1.0//EN"
        "bibtexml.dtd" >
"""
class Writer:
    """Outputs BibTeXML markup"""

    def __init__(self, encoding = 'utf-8'):
        self.encoding = encoding

    def write(self, bib_data, filename):
        def newline():
            w.data('\n')
        def write_persons(entry, role):
            persons = getattr(entry, role + 's')
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
        for key, entry in bib_data.iteritems():
            newline()
            w.start('bibtex:entry', id=key)
            newline()
            w.start('bibtex:' + entry.type)
            for field_name, field_value in entry.fields.iteritems():
                w.data('\n')
                w.element('bibtex:' + field_name, field_value)
            for role in ('author', 'editor'):
                write_persons(entry, role)
            newline()
            w.end()
            newline()
            w.end()
        newline()
        w.close(bibtex_file)
        w.flush()

        # XMLWriter does not add a newline at the end of file for some reason
        f.write('\n')
