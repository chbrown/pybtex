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

"""BibTeX unnamed stack language interpreter and related stuff
"""

import bst
from interpreter import Interpreter
from pybtex import auxfile

class BibTeX:
    def __init__(self):
        self.interpreter = Interpreter()
    def run(self, aux_filename):
        aux_data = auxfile.parse_file(aux_filename)
        bst_script = bst.parse_file(aux_data.style + '.bst')
        self.interpreter.run(bst_script, aux_data.citations, aux_data.data, aux_filename + '.bbl')


if __name__ == '__main__':
    import sys
    b = BibTeX()
    b.run(sys.argv[1])
    print b.i.vars
