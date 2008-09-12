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

import locale
import codecs

class BackendBase:
    def __init__(self, encoding=None):
        if encoding is None:
            encoding = locale.getpreferredencoding()
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
        self.f = codecs.open(filename, "w", self.encoding)
        self.output = self.f.write
        entries = list(entries)

        #FIXME: determine label width proprely
        maxlen = max([len(e.label) for e in entries])

        self.write_prologue(maxlen)
        for entry in entries:
            self.write_entry(entry.key, entry.label, entry.text.render(self))
        self.write_epilogue()

        self.f.close()
