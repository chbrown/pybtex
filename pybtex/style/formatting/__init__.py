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

from pybtex.core import FormattedEntry
from pybtex.style.template import node, join
from pybtex.richtext import Symbol, Text
from pybtex.plugin import Plugin, find_plugin


@node
def toplevel(children, data):
    return join(sep=Symbol('newblock')) [children].format_data(data)


class BaseStyle(Plugin):
    default_plugin = 'unsrt'
    default_label_style = 'number'
    default_name_style = 'plain'

    def __init__(self, label_style=None, name_style=None, abbreviate_names=False, **kwargs):
        if name_style is None:
            name_style = find_plugin('pybtex.style.names', self.default_name_style)
        if label_style is None:
            label_style = find_plugin('pybtex.style.labels', self.default_label_style)
        self.format_label = label_style.LabelStyle().format
        self.format_name = name_style.NameStyle().format
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
