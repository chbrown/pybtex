# Copyright (c) 2006, 2007, 2008, 2009, 2010, 2011  Andrey Golovizin
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import pybtex.io
from pybtex.plugin import Plugin


available_plugins = ('latex', 'html', 'plaintext')


class BaseBackend(Plugin):
    default_plugin = 'latex'

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
