#!/usr/bin/env python

from os import path
import filters
import auxfile
import utils
from formatters import label, find_plugin
from formatters.backends import latex

__version__ = "0.1"

def make_bibliography(aux_filename, bib_format='bib', bib_encoding=None, latex_encoding=None,
        output_backend='latex'):
    filename = path.splitext(aux_filename)[0]
    aux_data = auxfile.parse_file(aux_filename)

    backend = find_plugin('backends', output_backend)
    bib_parser = filters.find_filter('input', bib_format)
    if bib_encoding is not None:
        try:
            bib_parser.set_encoding(bib_encoding)
        except AttributeError:
            pass

    bib_data = bib_parser.parse_file(path.extsep.join([aux_data.data, bib_parser.file_extension]))
    
    entries = prepare_entries(bib_data, aux_data)
    del bib_data

    #utils.set_backend(output_backend)
    formatter = find_plugin('styles', aux_data.style).Formatter() #import_style(aux_data.style).Formatter()
    formatted_entries = formatter.format_entries(entries)
    del entries
    backend.Writer(latex_encoding).write_bibliography(formatted_entries, path.extsep.join([filename, backend.file_extension]))

def prepare_entries(bib_data, aux_data):
    n = 1
    entries = []
    for key in aux_data.citations:
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
