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

"""parse LaTeX aux file
"""

from __future__ import with_statement

import re
import codecs


class AuxData:
    def __init__(self):
        self.style = None
        self.data = None
        self.citations = []

    def add_citation(self, s):
        for c in s.split(','):
            if not c in self.citations:
                self.citations.append(c)

    def add_bibstyle(self, s):
        self.style = s

    def add_bibdata(self, s):
        self.data = s.split(',')

    def add(self, datatype, value):
        action = getattr(self, 'add_%s' % datatype)
        action(value)


def parse_file(filename, encoding):
    """Parse a file and return an AuxData object."""

    command_re = re.compile(r'\\(citation|bibdata|bibstyle){(.*)}')
    with codecs.open(filename, encoding=encoding) as f:
        s = f.read()
    data = AuxData()
    for datatype, value in command_re.findall(s):
        data.add(datatype, value)
    return data
