# Copyright (C) 2010  Andrey Golovizin
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


from pybtex.style.template import join
from pybtex.style.names import BaseNameStyle, name_part


class NameStyle(BaseNameStyle):
    def format(self, person, abbr=False):
        r"""
        Format names similarly to {vv~}{ll}{, jj}{, f.} in BibTeX.

        >>> from pybtex.core import Person
        >>> name = Person(string=r"Charles Louis Xavier Joseph de la Vall{\'e}e Poussin")
        >>> lastfirst = NameStyle().format
        >>> print lastfirst(name).format().plaintext()
        de<nbsp>la Vall{\'e}e<nbsp>Poussin, Charles Louis Xavier<nbsp>Joseph
        >>> print lastfirst(name, abbr=True).format().plaintext()
        de<nbsp>la Vall{\'e}e<nbsp>Poussin, C.<nbsp>L. X.<nbsp>J.

        >>> name = Person(first='First', last='Last', middle='Middle')
        >>> print lastfirst(name).format().plaintext()
        Last, First<nbsp>Middle
        >>> print lastfirst(name, abbr=True).format().plaintext()
        Last, F.<nbsp>M.

        """
        return join [
            name_part(tie=True) [person.prelast()],
            name_part [person.last()],
            name_part(before=', ') [person.lineage()],
            name_part(before=', ') [person.first(abbr) + person.middle(abbr)],
        ]

