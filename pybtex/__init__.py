#!/usr/bin/env python

from os import path
import filters
import auxfile
from formatters import label
from formatters.backends import latex

__version__ = "0.1"

def make_bibliography(aux_filename, bib_format='bib', bib_encoding=None, latex_encoding=None):
    filename = path.splitext(aux_filename)[0]
    aux_data = auxfile.parse_file(aux_filename)

    bib_parser = filters.find_filter('input', bib_format)
    if bib_encoding is not None:
        try:
            bib_parser.set_encoding(bib_encoding)
        except AttributeError:
            pass

    bib_data = bib_parser.parse_file(path.extsep.join([aux_data.data, bib_parser.extension]))
    
    entries = prepare_entries(bib_data, aux_data)
    del bib_data

    backend = latex
    style = import_style(aux_data.style).Formatter(backend)
    formatted_entries = style.format_entries(entries)
    del entries
    backend.Writer(latex_encoding).write_bibliography(formatted_entries, path.extsep.join([filename, 'bbl']))

def import_style(name):
    m = __import__('pybtex.formatters.styles', globals(), locals(), [name])
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

