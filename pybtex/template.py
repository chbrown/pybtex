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
# along with pybtex; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""template micro-language

>>> class entry:
...     fields = {'title': 'Some Title', 'author': 'Some Author'}
>>> template = AddPeriod(Phrase(Field('author'), Text('Lopata')))
>>> print template.format(entry())
['Some Author', ', ', 'Lopata', '.']
"""

from richtext import Text

class TextElementMissing(Exception):
    def __init__(self, errors = []):
        self.errors = errors

class RequiredElementMissing(TextElementMissing):
    pass

class CoreElementMissing(TextElementMissing):
    pass

class OptionalElementMissing(TextElementMissing):
    pass

class FieldMissing(OptionalElementMissing):
    pass

class TextNode:
    def __init__(self, data):
        self.data = data
    def __or__(self, other):
        return Or(self, other)
    def __add__(self, other):
        return ComplexTemplate(self, other)

class AddPeriod(TextNode):
    def format(self, entry):
        return self.data.format(entry).add_period()

class Field(TextNode):
    def format(self, entry):
        try:
            return Text(entry.fields[self.data])
        except KeyError:
            raise FieldMissing(errors=['%s field missing' % self.data])

#class String(TextNode):
#    def format(self, entry):
#        return self.data

class Required(TextNode):
    def format(self, entry):
        try:
            return self.data.format(entry)
        except TextElementMissing, s:
            raise RequiredElementMissing(s.errors)

class Core(TextNode):
    def format(self, entry):
        try:
            return self.data.format(entry)
        except TextElementMissing, s:
            raise CoreElementMissing(s.errors)

class TextNodeList(TextNode):
    def __init__(self, *items):
        self._list = []
        self._list += items
    def __repr__(self):
        return self._list.__repr__()
    def append(self, item):
        self._list.append(item)
    def extend(self, items):
        self._list.extend(items)

class ComplexTemplate(TextNodeList):
    def __add__(self, other):
        self.append(other)
        return self

    def format(self, entry):
        result = Text()
        for i in self._list:
            try:
                result.append(i.format(entry))
            except OptionalElementMissing:
                continue
        if result:
            return result
        else:
            raise OptionalElementMissing

class Group(TextNodeList):
    def format(self, entry):
        try:
            return Text(*[i.format(entry) for i in self._list])
        except CoreElementMissing:
            return ''

class Or(TextNodeList):
    def __or__(self, other):
        self.append(other)
        return self
    def __repr__(self):
        return 'Or' + TextNodeList.__repr__(self)
    def format(self, entry):
        errors = []
        for item in self._list:
            try:
                return item.format(entry)
            except OptionalElementMissing, e:
                errors += e.errors
                continue
        # no valid elements found
        raise OptionalElementMissing(errors)
        

class Phrase(TextNodeList):
    """Phrase is a helper class for easy construction of phrases.
    Examples:
        Phrase('One', 'two', 'three', add_period=True) -> 'One, two, three.'
        Phrase('Her', 'me', sep2=' and ') -> 'Her and me'
    More complex example:
        p = Phrase(sep2=' and ', last_sep=', and ', add_period=True)
        p.append('Her')               # "Her."
        p.append('her parents')       # "Her and her parents."
        p.append('her little sister') # "Her, her parents, and her little sister."
        p.append('me')                # "Her, her parents, her little sister, and me."
    """

    def __init__(self, *args, **kwargs):
        """Construct a phrase from all non-keyword arguments.
        Available keyword arguments are:
        - sep (default separator);
        - last_sep (separatos used before the last part of the phrase), defaults to sep;
        - sep2 (separator used if a phrase consists of exactly two parts), defaults to last_sep;
        - add_period (add a period at the end of phrase if there is none yet)
        - add_periods (add a period to every part of the phrase)
        """

        TextNodeList.__init__(self)

        self.sep = kwargs.get('sep', ', ')
        self.last_sep = kwargs.get('last_sep', self.sep)
        self.sep2 = kwargs.get('sep2', self.last_sep)
        self.period = kwargs.get('add_period', False)
        self.periods = kwargs.get('add_periods', False)
        self.sep_after = None
        
        for text in args:
            self.append(text)

    def append(self, text, sep_before=None, sep_after=None):
        if text:
            if self.sep_after is not None:
                sep_before = self.sep_after
                self.sep_after = None
            if sep_after is not None:
                self.sep_after = sep_after

            self._list.append((text, sep_before))

    def format(self, entry):
        """Create a Text representation of the phrase
        """
        def output_part(part, sep):
            if part[1] is not None:
                sep = part[1]
            if sep:
                result.append(sep)
            result.append(part[0].format(entry))

        if not self._list:
            result = Text()
        elif len(self._list) == 1:
            result = Text(self._list[0][0].format(entry))
        elif len(self._list) == 2:
            sep = self._list[1][1]
            if sep is None:
                sep = self.sep2
            result = Text(self._list[0][0].format(entry), sep, self._list[1][0].format(entry))
        else:
            result = Text()
            output_part(self._list[0], sep='')
            for part in self._list[1:-1]:
                output_part(part, self.sep)
            output_part(self._list[-1], self.last_sep)

        return result

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
