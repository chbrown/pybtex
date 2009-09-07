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

"""parse LaTeX aux file
"""

from __future__ import with_statement

import re

from pybtex.exceptions import PybtexError
import pybtex.io


class AuxDataError(PybtexError):
    pass


class AuxData:
    def __init__(self, filename):
        self.filename = filename
        self.style = None
        self.data = None
        self.citations = []

    def add_citation(self, s):
        for c in s.split(','):
            if not c in self.citations:
                self.citations.append(c)

    def add_bibstyle(self, style):
        if self.style is not None:
            raise AuxDataError(r'illegal, another \bibstyle command in %s' % self.filename)
        self.style = style

    def add_bibdata(self, bibdata):
        if self.data is not None:
            raise AuxDataError(r'illegal, another \bibdata command in %s' % self.filename)
        self.data = bibdata.split(',')

    def add(self, datatype, value):
        action = getattr(self, 'add_%s' % datatype)
        action(value)


def parse_file(filename, encoding):
    """Parse a file and return an AuxData object."""

    command_re = re.compile(r'\\(citation|bibdata|bibstyle){(.*)}')
    with pybtex.io.open(filename, encoding=encoding) as f:
        s = f.read()
    data = AuxData(filename)
    for datatype, value in command_re.findall(s):
        data.add(datatype, value)
    return data
