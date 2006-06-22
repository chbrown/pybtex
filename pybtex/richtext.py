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

"""rich text formatting and more
"""

import utils

class Text(list):
    """Rich text is basically a list of
    - strings
    - Tag objects
    - Symbol object
    - other Text objects
    Text is used as an internal formatting language of pybtex,
    being rendered to to HTML or LaTeX markup or whatever in the end.
    """

    def __init__(self, *args, **kwargs):
        """All the non-keyword arguments form the content of the Text object.
        E. g. Text('This ', 'is a', Tag('emph', 'very'), Text(' rich', ' text.')
        Note the spaces. After rendering you will probably get something like
        "This is a \emph{very} rich text". Isn't that simple? =)
        """

        if kwargs.get('check', False) and False in (bool(arg) for arg in args):
            args = []

        list.__init__(self)

        for i in args:
            self.append(i)

    def append(self, item):
        """Appends some text or something.
        Empty strings and similar things are ignored.
        """
        if item:
            list.append(self, item)

    def extend(self, list):
        for item in list:
            self.append(item)

    def render(self, backend):
        """Return textual representation of the Text.
        The representation is obviously backend-dependent.
        """
        text = []
        for item in self:
            try:
                text.append(item.render(backend))
            except AttributeError:
                text.append(item)
        return "".join(text)

    def is_terminated(self):
        """Return true if the text ends with period or something.
        """
        try:
            item = self[-1]
        except IndexError:
            return False
        try:
            return item.is_terminated()
        except AttributeError:
            return utils.is_terminated(item)

    def add_period(self):
        """Add period if possible
        """
        if not self.is_terminated():
            self.append('.')
        return self

class Tag:
    """A tag is somethins like <foo>some text</foo> in HTML
    or \\foo{some text} in LaTeX. 'foo' is the tag's name, and
    'some text' is tag's text.
    """
    def __init__(self, name, text):
        self.name = name
        self.text = text
    def is_terminated(self):
        return utils.is_terminated(self.text)
    def render(self, backend):
        try:
            text = self.text.render(backend)
        except AttributeError:
            text = self.text
        return backend.format_tag(self.name, text)
    def add_period(self):
        return Text(self).add_period()


class Symbol:
    """A symbol is used to represent some special characters.
    Example: Symbol('ndash') produces '&ndash;' when rendered to HTML
    and '--' when rendered to LaTeX.
    """
    def __init__(self, name):
        self.name = name
    def render(self, backend):
        return backend.symbols[self.name]


class Phrase(Text):
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

        self.sep = kwargs.get('sep', ', ')
        self.last_sep = kwargs.get('last_sep', self.sep)
        self.sep2 = kwargs.get('sep2', self.last_sep)
        self.period = kwargs.get('add_period', False)
        self.periods = kwargs.get('add_periods', False)
        self.sep_after = None
        self.parts = []

        if kwargs.get('check', False) and False in (bool(arg) for arg in args):
            args = []

        for text in args:
            self.append(text)

    def append(self, text, sep_before=None, sep_after=None):
        if text:
            if self.periods:
                text = utils.add_period(text)

            if self.sep_after is not None:
                sep_before = self.sep_after
                self.sep_after = None
            if sep_after is not None:
                self.sep_after = sep_after

            self.parts.append((text, sep_before))

    def extend(self, list):
        for item in list:
            self.append(item)

    def add_period(self):
        return Text(self).add_period()
    
    def _rebuild(self):
        """Return a Text representation of the phrase
        """
        def output_part(part, sep):
            if part[1] is not None:
                sep = part[1]
            if sep:
                result.append(sep)
            result.append(part[0])

        if not self.parts:
            result = Text()
        elif len(self.parts) == 1:
            result = Text(self.parts[0][0])
        elif len(self.parts) == 2:
            sep = self.parts[1][1]
            if sep is None:
                sep = self.sep2
            result = Text(self.parts[0][0], sep, self.parts[1][0])
        else:
            result = Text()
            output_part(self.parts[0], sep='')
            for part in self.parts[1:-1]:
                output_part(part, self.sep)
            output_part(self.parts[-1], self.last_sep)
        if self.period:
            result.add_period()
        self[:] = result

    def __repr__(self):
        return self[:].__repr__()
    def _rebuild_and_do(f):
        def my_f(self, *args, **kwargs):
            self._rebuild()
            return f(self, *args, **kwargs)
        return my_f

    __len__ = _rebuild_and_do(Text.__len__)
    __getitem__ = _rebuild_and_do(Text.__getitem__)
    __getslice__ = _rebuild_and_do(Text.__getslice__)
    __iter__ = _rebuild_and_do(Text.__iter__)


def main():
    p = Phrase(Phrase('first'), 'second', add_periods=True)
    print p

if __name__ == '__main__':
    main()
