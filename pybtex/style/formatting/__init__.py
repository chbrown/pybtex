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

from pybtex.core import FormattedEntry
from pybtex.style.template import node, join
from pybtex.richtext import Symbol, Text
from pybtex.plugin import Plugin, find_plugin


@node
def toplevel(children, data):
    return join(sep=Symbol('newblock')) [children].format_data(data)


class BaseStyle(Plugin):
    default_plugin = 'unsrt'

    def __init__(self, label_style=None, name_style=None, abbreviate_names=False, **kwargs):
        if name_style is None:
            name_style = find_plugin('pybtex.style.names')
        if label_style is None:
            label_style = find_plugin('pybtex.style.labels')
        self.format_label = label_style().format
        self.format_name = name_style().format
        self.abbreviate_names = abbreviate_names

    def format_entries(self, entries):
        for number, (key, entry) in enumerate(entries):
            entry.number = number + 1
            for persons in entry.persons.itervalues():
                for person in persons:
                    person.text = self.format_name(person, self.abbreviate_names)

            f = getattr(self, "format_" + entry.type)
            text = f(entry)
            label = self.format_label(entry)
            yield FormattedEntry(key, text, label)
