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

import pybtex.io


available_plugins = ('bibtex', 'bibtexml', 'bibyaml')


class WriterBase(object):
    unicode_io = False

    def __init__(self, encoding=None):
        self.encoding = encoding

    def write_file(self, bib_data, filename):
        open_file = pybtex.io.open_unicode if self.unicode_io else pybtex.io.open_raw
        mode = 'w' if self.unicode_io else 'wb'
        with open_file(filename, mode, encoding=self.encoding) as stream:
            self.write_stream(bib_data, stream)

    def write_stream(self, bib_data, stream):
        raise NotImplementedError
