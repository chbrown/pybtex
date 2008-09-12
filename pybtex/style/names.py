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

"""name formatting styles
"""
from pybtex.richtext import Symbol
from pybtex.style.template import join, words

def plain(person, abbr=False):
    """
    >>> from pybtex.core import Person
    >>> name = Person(string="Charles Louis Xavier Joseph de la Vall{\'e}e Poussin")
    >>> print plain(name).format().plaintext()
    Charles Louis Xavier Joseph de<nbsp>la Vall{\'e}e Poussin
    >>> print plain(name, abbr=True).format().plaintext()
    C. L. X. J. de<nbsp>la Vall{\'e}e Poussin
    >>> name = Person(first='First', last='Last', middle='Middle')
    >>> print plain(name).format().plaintext()
    First Middle Last
    >>> print plain(name, abbr=True).format().plaintext()
    F. M. Last

    """
    nbsp = Symbol('nbsp')
    return words [
        words [person.first(abbr)],
        words [person.middle(abbr)],
        join(sep=nbsp) [person.prelast()],
        words [person.last()],
        join(sep=nbsp) [person.lineage()]
    ]
