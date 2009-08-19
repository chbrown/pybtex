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

import re

terminators = '.?!'
dash_re = re.compile(r'-')

def capfirst(s):
    return s[0].upper() + s[1:] if s else s

def is_terminated(s):
    """Return true if s ends with a terminating character.
    """
    return (bool(s) and s[-1] in terminators)

def add_period(s):
    """Add a period to the end of s, if there is none yet.
    """
    if s and not is_terminated(s):
        return s + '.'
    return s

def abbreviate(s):
    """Abbreviate some text.
    Examples:
    abbreviate('Some words') -> "S. w."
    abbreviate('First-Second') -> "F.-S."
    """
    def parts(s):
        start = 0
        length = 0
        for letter in s:
            length += 1
            if not letter.isalpha():
                yield s[start:length], letter
                start += length
                length = 0
        yield s[start:length], ""
    def abbr(part):
        if part[0]:
            if is_terminated(part[1]):
                return part[0][0].upper() + part[1]
            else:
                return part[0][0].upper() + '.'
        else:
            return part[1]
    return ''.join(abbr(part) for part in parts(s))
