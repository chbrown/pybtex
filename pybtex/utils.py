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

import re
from pybtex.richtext import RichText, Symbol, Phrase

terminators = '.?!'
dash_re = re.compile(r'-')

def is_terminated(s):
    """Return true if s ends with a terminating character.
    """
    try:
        return s.is_terminated()
    except AttributeError:
        return (bool(s) and s[-1] in terminators)

def add_period(s):
    """Add a period to the end of s, if there is none yet.
    """
    try:
        return s.add_period()
    except AttributeError:
        try:
            s = s.rich_text()
        except AttributeError:
            pass
        if s and not is_terminated(s):
            s += '.'
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
        if is_terminated(part[1]):
            return part[0][0].upper() + part[1]
        else:
            return part[0][0].upper() + '.'
    return ''.join(abbr(part) for part in parts(s))

def dashify(s):
    """replace a dash wich Symbol('ndash')
    """
    p = Phrase(sep=Symbol('ndash'))
    for i in dash_re.split(s):
        p.append(i)
    return p.rich_text()

def try_format(s, format = '%s'):
    """If s is an empty string or something then return "",
    Otherwise return something.
    """
    if s:
        tmp = format.split('%s')
        tmp.insert(1, s)
        return RichText(*tmp)
    else:
        return ""
