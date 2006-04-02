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

"""bibliography processor
"""

from os import path
import auxfile
import utils
import formatters.backends.latex
import filters.input.bibtex
from formatters import find_plugin

__version__ = "0.1"

def make_bibliography(aux_filename,
        bib_format=filters.input.bibtex,
        bib_encoding=None,
        latex_encoding=None,
        label_style=formatters.labels.number,
        name_style=formatters.names.plain,
        output_backend=formatters.backends.latex,
        abbreviate_names=True
        ):
    """This functions extracts all nessessary information from .aux file
    and writes the bibliography.
    """

    filename = path.splitext(aux_filename)[0]
    aux_data = auxfile.parse_file(aux_filename)

    if bib_encoding is not None:
        try:
            bib_format.set_encoding(bib_encoding)
        except AttributeError:
            pass

    bib_filename = path.extsep.join([aux_data.data, bib_format.file_extension])
    bib_data = bib_format.Parser().parse_file(bib_filename)

    entries = prepare_entries(bib_data, aux_data.citations, label_style, name_style, abbreviate_names)
    del bib_data

    formatter = find_plugin('styles', aux_data.style).Formatter()
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
        for person in entry.authors + entry.editors:
            person.text = name_style(person, abbreviate_names)
        entries.append(entry)
    return entries
