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
# along with pybtex; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""bibliography processor
"""

from os import path
import auxfile
import styles
import backends.latex
import database.input.bibtex

__version__ = "20060416"

class FindPluginError(Exception):
    pass

def find_plugin(type, name):
    def import_(s):
        m = __import__(type, globals(), locals(), [s])
        try:
            return getattr(m, s)
        except AttributeError:
            return None

    f = import_(name)
    if f is None:
        raise FindPluginError('plugin %s not found in %s' % (name, type))
    return f

def make_bibliography(aux_filename,
        bib_format=database.input.bibtex,
        bib_encoding=None,
        latex_encoding=None,
        label_style=styles.labels.number,
        name_style=styles.names.plain,
        output_backend=backends.latex,
        abbreviate_names=True
        ):
    """This functions extracts all nessessary information from .aux file
    and writes the bibliography.
    """

    filename = path.splitext(aux_filename)[0]
    aux_data = auxfile.parse_file(aux_filename)

    bib_filename = path.extsep.join([aux_data.data, bib_format.file_extension])
    bib_data = bib_format.Parser(bib_encoding).parse_file(bib_filename)

    entries = prepare_entries(bib_data, aux_data.citations, label_style, name_style, abbreviate_names)
    del bib_data

    formatter = find_plugin('styles.formatting', aux_data.style).Formatter()
    formatted_entries = formatter.format_entries(entries)
    del entries

    output_filename = path.extsep.join([filename, output_backend.file_extension])
    output_backend.Writer(latex_encoding).write_bibliography(formatted_entries, output_filename)

def prepare_entries(bib_data, citations, label_style, name_style, abbreviate_names):
    entries = []
    for number, key in enumerate(citations):
        entry = bib_data[key]
        entry.number = number + 1 # entry numbers start with 1
        entry.key = key
        entry.label = label_style(entry)
        for persons in entry.persons.itervalues():
            for person in persons:
                person.text = name_style(person, abbreviate_names)
        entries.append(entry)
    return entries
