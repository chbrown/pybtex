# Copyright (c) 2006, 2007, 2008, 2009, 2010, 2011  Andrey Golovizin
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from collections import defaultdict

from pybtex.exceptions import PybtexError


class BibliographyDataError(PybtexError):
    pass


class BibliographyData(object):
    def __init__(self, entries=None, preamble=None):
        self.entries = {}
        self._preamble = []
        self.crossref_counts = defaultdict(int)
        if entries:
            self.entries.update(entries)
        if preamble:
            self._preamble.extend(preamble)

    def __eq__(self, other):
        if not isinstance(other, BibliographyData):
            return super(BibliographyData, self) == other
        return (
            self.entries == other.entries
            and self._preamble == other._preamble
        )

    def add_to_preamble(self, s):
        self._preamble.append(s)

    def __repr__(self):
        return 'BibliographyData(entries={entries}, preamble={preamble})'.format(
            entries=repr(self.entries),
            preamble=repr(self._preamble),
        )

    def preamble(self):
        return ''.join(self._preamble)

    def add_entry(self, key, entry):
        if key in self.entries:
            raise BibliographyDataError('repeated bibliograhpy entry: %s' % key)
        entry.collection = self
        entry.key = key
        self.entries[key] = entry
        if 'crossref' in entry.fields:
            self.crossref_counts[entry.fields['crossref']] += 1

    def add_entries(self, entries):
        for key, entry in entries:
            self.add_entry(key, entry)

    def get_extra_citations(self, min_crossrefs):
        citations = (
            citation
            for citation, crossref_count in self.crossref_counts.items()
            if crossref_count >= min_crossrefs
        )
        return sorted(citations)
