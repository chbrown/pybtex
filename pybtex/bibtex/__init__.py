# Copyright (C) 2007, 2008, 2009  Andrey Golovizin
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""BibTeX unnamed stack language interpreter and related stuff
"""

import locale


def make_bibliography(aux_filename,
        bib_format=None,
        bib_encoding=locale.getpreferredencoding(),
        output_encoding=locale.getpreferredencoding(),
        bst_encoding=locale.getpreferredencoding(),
        **kwargs
    ):

    import codecs
    from os import path

    from pybtex.bibtex import bst
    from pybtex.bibtex.interpreter import Interpreter
    from pybtex import auxfile
    from pybtex.bibtex.kpathsea import kpsewhich


    if bib_format is None:
        from pybtex.database.input import bibtex as bib_format
    aux_data = auxfile.parse_file(aux_filename, output_encoding)
    bst_filename = kpsewhich(aux_data.style + path.extsep + 'bst')
    bst_script = bst.parse_file(bst_filename, bst_encoding)
    base_filename = path.splitext(aux_filename)[0]
    bbl_filename = base_filename + path.extsep + 'bbl'
    bib_filenames = [filename + path.extsep + bib_format.file_extension for filename in aux_data.data]
    bbl_file = codecs.open(bbl_filename, 'w', encoding=output_encoding)
    Interpreter(bib_format).run(bst_script, aux_data.citations, bib_filenames, bbl_file)
