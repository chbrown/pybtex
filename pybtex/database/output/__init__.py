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

class WriterBase:
    def __init__(self, encoding = None):
        if not encoding:
            encoding = pybtex.io.get_default_encoding()
        self.encoding = encoding

    def write_file(self, bib_data, filename):
        with pybtex.io.open_plain(filename, 'w') as stream:
            self.write_stream(bib_data, stream)

    def write_stream(self, bib_data, stream):
        raise NotImplementedError
