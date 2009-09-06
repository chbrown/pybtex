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
from pybtex.richtext import Symbol, Text, nbsp
from pybtex.style.template import join, together, node, _format_list


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


def plain(person, abbr=False):
    r"""
    Format names similarly to {ff~}{vv~}{ll}{, jj} in BibTeX.  

    >>> from pybtex.core import Person
    >>> name = Person(string=r"Charles Louis Xavier Joseph de la Vall{\'e}e Poussin")
    >>> print plain(name).format().plaintext()
    Charles Louis Xavier<nbsp>Joseph de<nbsp>la Vall{\'e}e<nbsp>Poussin
    >>> print plain(name, abbr=True).format().plaintext()
    C.<nbsp>L. X.<nbsp>J. de<nbsp>la Vall{\'e}e<nbsp>Poussin

    >>> name = Person(first='First', last='Last', middle='Middle')
    >>> print plain(name).format().plaintext()
    First<nbsp>Middle Last
    >>> print plain(name, abbr=True).format().plaintext()
    F.<nbsp>M. Last
    >>> print plain(Person('de Last, Jr., First Middle')).format().plaintext()
    First<nbsp>Middle de<nbsp>Last, Jr.
    """
    return join [
        name_part(tie=True) [person.first(abbr) + person.middle(abbr)],
        name_part(tie=True) [person.prelast()],
        name_part [person.last()],
        name_part(before=', ') [person.lineage()]
    ]

def last_first(person, abbr=False):
    r"""
    Format names similarly to {vv~}{ll}{, jj}{, f.} in BibTeX.

    >>> from pybtex.core import Person
    >>> name = Person(string=r"Charles Louis Xavier Joseph de la Vall{\'e}e Poussin")
    >>> print last_first(name).format().plaintext()
    de<nbsp>la Vall{\'e}e<nbsp>Poussin, Charles Louis Xavier<nbsp>Joseph
    >>> print last_first(name, abbr=True).format().plaintext()
    de<nbsp>la Vall{\'e}e<nbsp>Poussin, C.<nbsp>L. X.<nbsp>J.

    >>> name = Person(first='First', last='Last', middle='Middle')
    >>> print last_first(name).format().plaintext()
    Last, First<nbsp>Middle
    >>> print last_first(name, abbr=True).format().plaintext()
    Last, F.<nbsp>M.

    """
    return join [
        name_part(tie=True) [person.prelast()],
        name_part [person.last()],
        name_part(before=', ') [person.lineage()],
        name_part(before=', ') [person.first(abbr) + person.middle(abbr)],
    ]
