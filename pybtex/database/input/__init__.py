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
available_plugins = ('bibtex', 'bibtexml', 'bibyaml')


class ParserBase:
    unicode_io = False

    def __init__(self, encoding=None, **kwargs):
        self.encoding = encoding
        self.data = BibliographyData()

    def parse_file(self, filename, fileext=None):
        if fileext is not None:
            filename = filename + path.extsep + fileext
        open_file = pybtex.io.open_unicode if self.unicode_io else pybtex.io.open_raw
        with open_file(filename, encoding=self.encoding) as f:
            self.parse_stream(f)
        return self.data

    def parse_files(self, filenames, fileext=None):
        for filename in filenames:
            self.parse_file(filename, fileext)
        return self.data

    def parse_stream(self, stream):
        raise NotImplementedError
