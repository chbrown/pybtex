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

"""name formatting styles
"""

from pybtex.plugin import Plugin
from pybtex.richtext import Symbol, Text, nbsp
from pybtex.style.template import join, together, node, _format_list


available_plugins = ('plain', 'lastfirst')


class BaseNameStyle(Plugin):
    default_plugin = 'plain'

    def format(self, person, abbr=False):
        raise NotImplementedError


def tie_or_space(word, tie='~', space = ' ', enough_chars=3):
    if len(word) < enough_chars:
        return tie
    else:
        return space
    

@node
def name_part(children, data, before='', tie=False):
    parts = together [children].format_data(data)
    if not parts:
        return Text()
    if tie:
        return Text(before, parts, tie_or_space(parts, nbsp, ' '))
    else:
        return Text(before, parts)
