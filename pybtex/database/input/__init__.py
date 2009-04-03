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

default = 'bib'
filetypes = {'bib' : 'bibtex'}
import locale

class ParserBase:
    def __init__(self, encoding=None, **kwargs):
        if encoding is None:
            encoding = locale.getpreferredencoding()
        self.encoding = encoding

    def parse_file(self, filename):
        with open(filename, 'r') as f:
            result = self.parse_stream(f)
        return result
