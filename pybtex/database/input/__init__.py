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

from __future__ import with_statement

import locale
from os import path

from pybtex.database import BibliographyData

default = 'bib'
filetypes = {'bib' : 'bibtex'}

class ParserBase:
    def __init__(self, encoding=None, **kwargs):
        if encoding is None:
            encoding = locale.getpreferredencoding()
        self.encoding = encoding
        self.data = BibliographyData()

    def parse_file(self, filename, fileext=None):
        if fileext is not None:
            filename = filename + path.extsep + fileext
        with open(filename, 'r') as f:
            self.parse_stream(f)
        return self.data

    def parse_files(self, filenames, fileext=None):
        for filename in filenames:
            self.parse_file(filename, fileext)
        return self.data
