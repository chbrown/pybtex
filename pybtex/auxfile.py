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
# along with rdiff-backup; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

"""parse latex' aux file
"""

import re

class AuxData:
    def __init__(self):
        self.style = None
        self.data = None
        self.citations = []
    def new_citation(self, s):
        for c in s.split(','):
            if not c in self.citations:
                self.citations.append(c)
    def new_style(self, s):
        self.style = s
    def new_data(self, s):
        self.data = s

def parse_file(filename):
    """parse a file and return an AuxData object
    FIXME: add an option to specify aux file encoding in command line
    """
    command = re.compile(r'\\(citation|bibdata|bibstyle){(.*)}')
    f = open(filename)
    s = f.read()
    f.close()
    b = AuxData()
    actions = {
        "citation" : b.new_citation,
        "bibstyle" : b.new_style,
        "bibdata" : b.new_data
    }
    for i in command.findall(s):
        actions[i[0]](i[1])
    return b
