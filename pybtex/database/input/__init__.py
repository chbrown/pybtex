# Copyright (C) 2006, 2007, 2008, 2009  Andrey Golovizin
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

from __future__ import with_statement

from os import path

import pybtex.io
from pybtex.database import BibliographyData

default = 'bib'
filetypes = {'bib' : 'bibtex'}

class ParserBase:
    def __init__(self, encoding=None, **kwargs):
        self.encoding = encoding
        self.data = BibliographyData()

    def parse_file(self, filename, fileext=None):
        if fileext is not None:
            filename = filename + path.extsep + fileext
        with pybtex.io.open_plain(filename, 'r') as f:
            self.parse_stream(f)
        return self.data

    def parse_files(self, filenames, fileext=None):
        for filename in filenames:
            self.parse_file(filename, fileext)
        return self.data

    def parse_stream(self, stream):
        raise NotImplementedError
