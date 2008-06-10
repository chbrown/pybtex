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

from copy import deepcopy

r"""(simple but) rich text formatting tools

Usage:
>>> from pybtex.backends import latex
>>> backend = latex.Writer()
>>> t = Text('This ', 'is a ', Tag('emph', 'very'), Text(' rich', ' text.'))
>>> print t.render(backend)
This is a \emph{very} rich text.

>>> t = Text('Some ', Tag('emph', Text('nested ', Tag('texttt', 'Text', Text(' objects')))), '.')
>>> print t.render(backend)
Some \emph{nested \texttt{Text objects}}.
"""

class Text(list):
    """
    Rich text is basically a list of
    - plain strings
    - Tag objects
    - other Text objects
    Text is used as an internal formatting language of Pybtex,
    being rendered to to HTML or LaTeX markup or whatever in the end.
    """

    def __init__(self, *parts):
        r"""Create a Text consisting one or more parts."""

        list.__init__(self, parts)

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
            if isinstance(item, basestring):
                text.append(item)
            else:
                text.append(item.render(backend))
        return "".join(text)

    def enumerate(self):
        for n, child in enumerate(self):
            try:
                for p in child.enumerate():
                    yield p
            except AttributeError:
                yield self, n

    def reversed(self):
        for n, child in reversed(self):
            try:
                for p in child.reversed():
                    yield p
            except AttributeError:
                yield self, n

    def apply(self, f):
        for l, i in self.enumerate():
            l[i] = f(l[i])

    def apply_to_start(self, f):
        l, i = self.enumerate().next()
        l[i] = f(l[i])

    def apply_to_end(self, f):
        l, i = self.reversed().next()
        l[i] = f(l[i])

    def join(self, parts):
        joined = Text()
        for part in parts[:-1]:
            joined.extend([part, deepcopy(self)])
        joined.append(parts[-1])
        return joined

    def plaintext(self):
        return ''.join(l[i] for l, i in self.enumerate())


class Tag(Text):
    """A tag is somethins like <foo>some text</foo> in HTML
    or \\foo{some text} in LaTeX. 'foo' is the tag's name, and
    'some text' is tag's text.
    """
    def __init__(self, name, *args):
        self.name = name
        Text.__init__(self, *args)
    def render(self, backend):
        text = super(Tag, self).render(backend)
        return backend.format_tag(self.name, text)

def main():
    import string
    from backends import latex
    backend = latex.Writer()
    text = Text('foo', ' bar ', Tag('emph', 'some other words'))
    text.append(' 42')
    text.append(' football')
    print text.render(backend)
    text.apply(string.upper)
    text.apply_to_start(string.lower)
    print text.render(backend)
    print Text(', ').join([Tag('b', 'a'), 'b']).render(backend)



if __name__ == '__main__':
    main()
