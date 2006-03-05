#!/usr/bin/env python
import filters
import aux
from formatters import label

__version__ = 0.1

def import_style(name):
    m = __import__('pybtex.formatters.latex', globals(), locals(), [name])
    return getattr(m, name)

def prepare_entries(bib_data, aux_data):
    n = 1
    entries = []
    for key in aux_data.citations:
        print key
        entry = bib_data[key]
        entry.number = n
        entry.key = key
        entry.label = label.number(entry)
        entries.append(entry)
        n += 1
    def l(e):
        return e.label
    entries.sort(key=l)
    return entries

def parse_filename(filename):
    dot = filename.rfind('.')
    if dot == -1:
        return filename, None
    else:
        return (filename[:dot], filename[dot + 1:])

