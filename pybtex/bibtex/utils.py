# Copyright (C) 2007, 2008, 2009  Andrey Golovizin
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

def bibtex_len(s):
    """Return the number of characters in s, taking TeX' special chars into accoount.
    """
    #FIXME stub
    return len(s)

def split_name_list(string):
    """
    Split a list of names, separated by ' and '.

    >>> split_name_list('Johnson and Peterson')
    ['Johnson', 'Peterson']
    >>> split_name_list('Armand and Peterson')
    ['Armand', 'Peterson']
    >>> split_name_list('Armand and anderssen')
    ['Armand', 'anderssen']
    >>> split_name_list('What a Strange{ }and Bizzare Name! and Peterson')
    ['What a Strange{ }and Bizzare Name!', 'Peterson']
    >>> split_name_list('What a Strange and{ }Bizzare Name! and Peterson')
    ['What a Strange and{ }Bizzare Name!', 'Peterson']
    """
    return split_tex_string(string, ' and ')

def split_tex_string(string, sep, strip=True):
    """Split a string using the given separator, ignoring separators at brace level > 0."""

    brace_level = 0
    name_start = 0
    result = []
    end = len(string) - 1
    sep_len = len(sep)
    for pos, char in enumerate(string):
        if char == '{':
            brace_level += 1
        elif char == '}':
            brace_level -= 1
        elif (
            brace_level == 0 and
            string[pos:pos + len(sep)].lower() == sep and
            pos > 0 and
            pos + len(sep) < end
        ):
            result.append(string[name_start:pos])
            name_start = pos + len(sep)
    result.append(string[name_start:])
    if strip:
        return [part.strip() for part in result]
    else:
        return result
