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
        Format names similarly to {ff~}{vv~}{ll}{, jj} in BibTeX.  

        >>> from pybtex.core import Person
        >>> name = Person(string=r"Charles Louis Xavier Joseph de la Vall{\'e}e Poussin")
        >>> plain = NameStyle().format
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

