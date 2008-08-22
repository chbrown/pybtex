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

r"""(simple but) rich text formatting tools

Usage:
>>> from pybtex.backends import latex
>>> backend = latex.Writer()
>>> t = Text('this ', 'is a ', Tag('emph', 'very'), Text(' rich', ' text'))
>>> print t.render(backend)
this is a \emph{very} rich text
>>> print t.plaintext()
this is a very rich text
>>> t.capfirst()
>>> t.add_period()
>>> print t.render(backend)
This is a \emph{very} rich text.
>>> print t.plaintext()
This is a very rich text.
>>> print Symbol('ndash').render(backend)
--
>>> t = Text('Some ', Tag('emph', Text('nested ', Tag('texttt', 'Text', Text(' objects')))), '.')
>>> print t.render(backend)
Some \emph{nested \texttt{Text objects}}.
>>> print t.plaintext()
Some nested Text objects.
>>> from string import upper, lower
>>> t.apply(upper)
>>> print t.render(backend)
SOME \emph{NESTED \texttt{TEXT OBJECTS}}.
>>> print t.plaintext()
SOME NESTED TEXT OBJECTS.

>>> t = Text(', ').join(['one', 'two', Tag('emph', 'three')])
>>> print t.render(backend)
one, two, \emph{three}
>>> print t.plaintext()
one, two, three
>>> t = Text(Symbol('nbsp')).join(['one', 'two', Tag('emph', 'three')])
>>> print t.render(backend)
one~two~\emph{three}
>>> print t.plaintext()
one<nbsp>two<nbsp>three
"""

from copy import deepcopy
from pybtex import textutils

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
        r"""Create a Text consisting of one or more parts."""

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
        """Return backend-dependent textual representation of this Text."""

        text = []
        for item in self:
            if isinstance(item, basestring):
                text.append(backend.format_text(item))
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
        for n, child in reversed(list(enumerate(self))):
            try:
                for p in child.reversed():
                    yield p
            except AttributeError:
                yield self, n

    def apply(self, f):
        """Apply a function to each part of the text."""  

        for l, i in self.enumerate():
            l[i] = f(l[i])

    def apply_to_start(self, f):
        """Apply a function to the last part of the text"""

        l, i = self.enumerate().next()
        l[i] = f(l[i])

    def apply_to_end(self, f):
        """Apply a function to the last part of the text"""

        l, i = self.reversed().next()
        l[i] = f(l[i])

    def join(self, parts):
        """Join a list using this text (like string.join)"""

        joined = Text()
        for part in parts[:-1]:
            joined.extend([part, deepcopy(self)])
        joined.append(parts[-1])
        return joined

    def plaintext(self):
        return ''.join(unicode(l[i]) for l, i in self.enumerate())

    def capfirst(self):
        """Capitalize the first letter of the text"""

        self.apply_to_start(textutils.capfirst)

    def add_period(self):
        """Add a period to the end of text, if necessary"""

        self.apply_to_end(textutils.add_period)

class Tag(Text):
    """A tag is somethins like <foo>some text</foo> in HTML
    or \\foo{some text} in LaTeX. 'foo' is the tag's name, and
    'some text' is tag's text.

    >>> emph = Tag('emph', 'emphasized text')
    >>> from pybtex.backends import latex, html
    >>> print emph.render(latex.Writer())
    \emph{emphasized text}
    >>> print emph.render(html.Writer())
    <em>emphasized text</em>
    """

    def __init__(self, name, *args):
        self.name = name
        Text.__init__(self, *args)
    def render(self, backend):
        text = super(Tag, self).render(backend)
        return backend.format_tag(self.name, text)

class Symbol(object):
    """A special symbol.

    Examples of special symbols are non-breaking spaces and dashes.

    >>> nbsp = Symbol('nbsp')
    >>> from pybtex.backends import latex, html
    >>> print nbsp.render(latex.Writer())
    ~
    >>> print nbsp.render(html.Writer())
    &nbsp;
    """

    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return u'<%s>' % self.name

    def render(self, backend):
        return backend.symbols[self.name]
