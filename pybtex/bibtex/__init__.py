# Copyright (C) 2006, 2007, 2008  Andrey Golovizin
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

"""BibTeX unnamed stack language interpreter and related stuff
"""

import codecs
from os import path

from pybtex.bibtex import bst
from pybtex.bibtex.interpreter import Interpreter
from pybtex import auxfile
from pybtex.bibtex.kpathsea import kpsewhich
import locale


def make_bibliography(aux_filename,
        bib_format=None,
        bib_encoding=locale.getpreferredencoding(),
        output_encoding=locale.getpreferredencoding(),
        bst_encoding=locale.getpreferredencoding(),
        **kwargs):
    if bib_format is None:
        from pybtex.database.input import bibtex as bib_format
    aux_data = auxfile.parse_file(aux_filename, output_encoding)
    bst_filename = kpsewhich(aux_data.style + path.extsep + 'bst')
    bst_script = bst.parse_file(bst_filename, bst_encoding)
    base_filename = path.splitext(aux_filename)[0]
    bbl_filename = base_filename + path.extsep + 'bbl'
    bib_filename = aux_data.data + path.extsep + bib_format.file_extension
    bbl_file = codecs.open(bbl_filename, 'w', encoding=output_encoding)
    Interpreter(bib_format).run(bst_script, aux_data.citations, bib_filename, bbl_file)
