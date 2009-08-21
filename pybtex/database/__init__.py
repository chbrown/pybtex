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

from pybtex.exceptions import PybtexError


class BibliographyDataError(PybtexError):
    pass


class BibliographyData(object):
    def __init__(self, entries=None, preamble=None):
        self.entries = {}
        self._preamble = []
        if entries:
            self.entries.update(entries)
        if preamble:
            self.preamble.extend(preamble)

    def __eq__(self, other):
        if not isinstance(other, BibliographyData):
            return super(BibliographyData, self) == other
        return (
            self.entries == other.entries
            and self._preamble == other._preamble
        )

    def add_to_preamble(self, s):
        self._preamble.append(s)

    def preamble(self):
        return ''.join(self._preamble)

    def add_entry(self, key, entry):
        if key in self.entries:
            raise BibliographyDataError('repeated bibliograhpy entry: %s' % key)
        entry.collection = self
        self.entries[key] = entry

    def add_entries(self, entries):
        for key, entry in entries:
            self.add_entry(key, entry)
