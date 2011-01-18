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

from collections import defaultdict, Mapping, Sequence

from pybtex.exceptions import PybtexError


class BibliographyDataError(PybtexError):
    pass


class BibliographyData(object):
    def __init__(self, entries=None, preamble=None):
        self.entries = {}
        self.entry_keys = []
        self._preamble = []
        if entries:
            if isinstance(entries, Mapping):
                entries = entries.iteritems()
            for (key, entry) in entries:
                self.add_entry(key, entry)
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
        self.entry_keys.append(key)

    def add_entries(self, entries):
        for key, entry in entries:
            self.add_entry(key, entry)

    def get_crossreferenced_citations(self, citations, min_crossrefs):
        """
        Get cititations not cited explicitly but referenced by other citations.

        >>> from pybtex.core import Entry
        >>> data = BibliographyData({
        ...     'main_article': Entry('article', {'crossref': 'xrefd_arcicle'}),
        ...     'xrefd_arcicle': Entry('article'),
        ... })
        >>> list(data.get_crossreferenced_citations([], min_crossrefs=1))
        []
        >>> list(data.get_crossreferenced_citations(['main_article'], min_crossrefs=1))
        ['xrefd_arcicle']
        >>> list(data.get_crossreferenced_citations(['main_article'], min_crossrefs=2))
        []
        >>> list(data.get_crossreferenced_citations(['xrefd_arcicle'], min_crossrefs=1))
        []

        """

        crossref_count = defaultdict(int)
        citation_set = set(citations)
        for citation in citations:
            try:
                entry = self.entries[citation]
            except KeyError:
                continue
            try:
                crossref = entry.fields['crossref']
            except KeyError:
                continue
            crossref_count[crossref] += 1
            if crossref_count[crossref] >= min_crossrefs and crossref not in citation_set:
                citation_set.add(crossref)
                yield crossref

    def expand_wildcard_citations(self, citations):
        """
        Expand wildcard citations (\citation{*} in .aux file).

        >>> from pybtex.core import Entry
        >>> data = BibliographyData((
        ...     ('uno', Entry('article')),
        ...     ('dos', Entry('article')),
        ...     ('tres', Entry('article')),
        ...     ('cuatro', Entry('article')),
        ... ))
        >>> list(data.expand_wildcard_citations([]))
        []
        >>> list(data.expand_wildcard_citations(['*']))
        ['uno', 'dos', 'tres', 'cuatro']
        >>> list(data.expand_wildcard_citations(['uno', '*']))
        ['uno', 'dos', 'tres', 'cuatro']
        >>> list(data.expand_wildcard_citations(['dos', '*']))
        ['dos', 'uno', 'tres', 'cuatro']
        >>> list(data.expand_wildcard_citations(['*', 'uno']))
        ['uno', 'dos', 'tres', 'cuatro']

        """

        citation_set = set()
        for citation in citations:
            if citation == '*':
                for key in self.entry_keys:
                    if key not in citation_set:
                        citation_set.add(key)
                        yield key
            else:
                if citation not in citation_set:
                    citation_set.add(citation)
                    yield citation

    def add_extra_citations(self, citations, min_crossrefs):
        expanded_citations = list(self.expand_wildcard_citations(citations))
        crossrefs = list(self.get_crossreferenced_citations(expanded_citations, min_crossrefs))
        return expanded_citations + crossrefs
