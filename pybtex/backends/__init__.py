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

import pybtex.io

class BackendBase:
    def __init__(self, encoding=None):
        self.encoding = encoding

    def write_prologue(self, maxlen):
        pass

    def write_epilogue(self):
        pass

    def format_text(self, text):
        return text

    def format_tag(self, tag_name, text):
        """Format a tag with some text inside.

        Text is already formatted with format_text."""

        raise NotImplementedError

    def write_entry(self, label, key, text):
        raise NotImplementedError

    def write_bibliography(self, entries, filename):
        self.f = pybtex.io.open_unicode(filename, "w", self.encoding)
        self.output = self.f.write
        entries = list(entries)

        #FIXME: determine label width proprely
        maxlen = max([len(e.label) for e in entries])

        self.write_prologue(maxlen)
        for entry in entries:
            self.write_entry(entry.key, entry.label, entry.text.render(self))
        self.write_epilogue()

        self.f.close()
