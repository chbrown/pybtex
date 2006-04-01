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

"""rich text formatting and more
"""

import utils

class RichText(list):
    """Rich text is basically a list of
    - strings
    - Tag objects
    - Symbol object
    - other RichText objects
    RichText is used as an internal formatting language of pybtex,
    being rendered to to HTML or LaTeX markup or whatever in the end.
    """
    def __init__(self, *args):
        """All the non-keyword arguments form the content of the RichText object.
        E. g. RichText('This ', 'is a', Tag('emph', 'very'), RichText(' rich', ' text.')
        Note the spaces. After rendering you will probably get something like
        "This is a \emph{very} rich text". Isn't that simple? =)
        """
        list.__init__(self)
        for i in args:
            self.append(i)
    def append(self, item):
        """Appends some text or something.
        Empty strings and similar things are ignored.
        """
        if item:
            list.append(self, item)
    def render(self, backend):
        """Return textual representation of the RichText.
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
        return RichText(self).add_period()


class Symbol:
    """A symbol is used to represent some special characters.
    Example: Symbol('ndash') produces '&ndash;' when rendered to HTML
    and '--' when rendered to LaTeX.
    """
    def __init__(self, name):
        self.name = name
    def render(self, backend):
        return backend.symbols[self.name]


class Phrase:
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
        def getarg(key, default=None):
            try:
                return kwargs[key]
            except KeyError:
                return default

        self.sep = getarg('sep', ', ')
        self.last_sep = getarg('last_sep', self.sep)
        self.sep2 = getarg('sep2', self.last_sep)
        self.period = getarg('add_period', False)
        self.periods = getarg('add_periods', False)
        self.sep_after = None
        self.parts = []

        for text in args:
            if isinstance(text, list):
                for i in text:
                    self.append(i)
            else:
                self.append(text)

        self.__str__ = self.parts.__str__
        self.__repr__ = self.parts.__repr__

    def append(self, text, sep_before=None, sep_after=None):
        try:
            text = text.rich_text()
        except AttributeError:
            pass
        if text:
            if self.periods:
                text = utils.add_period(text)

            if self.sep_after is not None:
                sep_before = self.sep_after
                self.sep_after = None
            if sep_after is not None:
                self.sep_after = sep_after

            if isinstance(text, list):
                self.parts.append((text[0], sep_before))
                for part in text[1:]:
                    self.parts.append((part, ''))
            else:
                self.parts.append((text, sep_before))

    def rich_text(self):
        """Return a RichText representation of the phrase
        """
        def output_part(part, sep):
            if part[1] is not None:
                sep = part[1]
            if sep:
                result.append(sep)
            result.append(part[0])

        if not self.parts:
            return RichText()
        elif len(self.parts) == 1:
            result = RichText(self.parts[0][0])
        elif len(self.parts) == 2:
            sep = self.parts[1][1]
            if sep is None:
                sep = self.sep2
            result = RichText(self.parts[0][0], sep, self.parts[1][0])
        else:
            result = RichText()
            output_part(self.parts[0], sep='')
            for part in self.parts[1:-1]:
                output_part(part, self.sep)
            output_part(self.parts[-1], self.last_sep)
        if self.period:
            result.add_period()
        return result


def main():
    t = RichText('This is a ', Tag('emph', 'very'), ' rich text.')
    t.append(' Another sentense. ')
    t.append(RichText(' Another text. ', Tag('textbf', 'Some bold text.')))
    print t
    print t.render(None) 
    print t.is_terminated()

if __name__ == '__main__':
    main()
