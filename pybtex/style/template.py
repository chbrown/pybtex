# vim:fileencoding=utf8

# Copyright (C) 2008, 2009  Andrey Golovizin
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

"""
A template engine for bibliography entries and more.

Inspired by Brevé -- http://breve.twisty-industries.com/

>>> from pybtex.core import Entry, Person
>>> author = Person(first='First', last='Last', middle='Middle')
>>> fields = {
...         'title': 'The Book',
...         'year': '2000',
... }
>>> e = Entry('book', fields=fields)
>>> book_format = sentence(sep=', ') [
...     field('title'), field('year'), optional [field('sdf')]
... ]
>>> print book_format.format_data(e).plaintext()
The Book, 2000.
>>> print words ['one', 'two', words ['three', 'four']].format_data(e).plaintext()
one two three four
"""

from pybtex import richtext

__test__ = {} # for doctest

class Proto(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return Node(*self.args, **self.kwargs)(*args, **kwargs)

    def __getitem__(self, children):
        return Node(*self.args, **self.kwargs)[children]

    def __repr__(self):
        return repr(Node(*self.args, **self.kwargs))

    def format_data(self, *args, **kwargs):
        return Node(*self.args, **self.kwargs).format_data(*args, **kwargs)

    def format(self):
        return self.format_data(None)


class Node(object):
    def __init__(self, name, f):
        self.name = name
        self.f = f
        self.args = []
        self.kwargs = {}
        self.children = []

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs.update(kwargs)
        return self

    def __getitem__(self, children):
        if isinstance(children, (list, tuple)):
            self.children = children
        else:
            self.children.append(children)
        return self

    def __repr__(self):
        """
        >>> join(', ')
        join(', ')
        >>> join
        join
        >>> join ['a']
        join ['a']
        >>> join ['a', 'b', 'c']
        join ['a', 'b', 'c']
        >>> join(' ') ['a', 'b', 'c']
        join(' ') ['a', 'b', 'c']
        >>> join(sep=' ') ['a', 'b', 'c']
        join(sep=' ') ['a', 'b', 'c']
        >>> join(sep=' ') [tag('em') ['a', 'b', 'c']]
        join(sep=' ') [tag('em') ['a', 'b', 'c']]

        """
        params = []
        args_repr = ', '.join(repr(arg) for arg in self.args)
        if args_repr:
            params.append(args_repr)
        kwargs_repr = ', '.join('%s=%s' % (key, repr(value))
                for (key, value) in self.kwargs.iteritems())
        if kwargs_repr:
            params.append(kwargs_repr)
        if params:
            params_repr = '(%s)' % ', '.join(params)
        else:
            params_repr = ''

        if self.children:
            children_repr = ' [%s]' % ', '.join(repr(child)
                    for child in self.children)
        else:
            children_repr = ''

        return ''.join([self.name, params_repr, children_repr])

    def format_data(self, data):
        """Format the given data into a piece of richtext.Text"""

        return self.f(self.children, data, *self.args, **self.kwargs)

    def format(self):
        """A convenience function to be used instead of format_data
        when no data is needed.
        """

        return self.format_data(None)


def _format_data(node, data):
    try:
        f = node.format_data
    except AttributeError:
        return unicode(node)
    else:
        return f(data)

def _format_list(list_, data):
    return [_format_data(part, data) for part in list_]

def node(f):
    if f.__doc__:
        __test__[f.__name__] = f
    return Proto(f.__name__, f)

@node
def join(children, data, sep='', sep2=None, last_sep=None):
    """Join text fragments together.
    >>> print join.format().plaintext()
    <BLANKLINE>
    >>> print join ['a', 'b', 'c', 'd', 'e'].format().plaintext()
    abcde
    >>> print join(sep=', ', sep2=' and ', last_sep=', and ') ['Tom', 'Jerry'].format().plaintext()
    Tom and Jerry
    >>> print join(sep=', ', sep2=' and ', last_sep=', and ') ['Billy', 'Willy', 'Dilly'].format().plaintext()
    Billy, Willy, and Dilly
    """

    if sep2 is None:
        sep2 = sep
    if last_sep is None:
        last_sep = sep
    parts = [part for part in _format_list(children, data) if part]
    if len(parts) <= 1:
        return richtext.Text(*parts)
    elif len(parts) == 2:
        return richtext.Text(sep2).join(parts)
    else:
        return richtext.Text(last_sep).join([richtext.Text(sep).join(parts[:-1]), parts[-1]])

@node
def words(children, data, sep=' '):
    """Join text fragments with spaces or something else."""

    return join(sep) [children].format_data(data)

@node
def together(children, data, last_tie=True):
    """
    Try to keep words together, like BibTeX does.

    >>> print together ['very', 'long', 'road'].format().plaintext()
    very long<nbsp>road
    >>> print together ['a', 'very', 'long', 'road'].format().plaintext()
    a<nbsp>very long<nbsp>road
    """
    from pybtex.bibtex.names import tie_or_space
    tie = richtext.Text(richtext.nbsp)
    space = richtext.Text(' ')
    parts = [part for part in _format_list(children, data) if part]
    if not parts:
        return richtext.Text()
    if len(parts) <= 2:
        tie2 = tie if last_tie else tie_or_space(parts[0], tie, space)
        return tie2.join(parts)
    else:
        last_tie = tie if last_tie else tie_or_space(parts[-1], tie, space)
        return richtext.Text(parts[0], tie_or_space(parts[0], tie, space),
                space.join(parts[1:-1]), last_tie, parts[-1])


@node
def sentence(children, data, capfirst=True, add_period=True, sep=', '):
    """Join text fragments, capitalyze the first letter, add a period to the end.

    >>> print sentence.format().plaintext()
    <BLANKLINE>
    >>> print sentence(sep=' ') ['mary', 'had', 'a', 'little', 'lamb'].format().plaintext()
    Mary had a little lamb.
    >>> print sentence(capfirst=False, add_period=False) ['uno', 'dos', 'tres'].format().plaintext()
    uno, dos, tres
    """

    text = join(sep) [children].format_data(data)
    if capfirst:
        text = text.capfirst()
    if add_period:
        text = text.add_period()
    return text

class FieldIsMissing(Exception):
    pass

@node
def field(children, data, name, apply_func=None):
    """Return the contents of the bibliography entry field."""

    assert not children
    try:
        field = data.fields[name]
    except KeyError:
        raise FieldIsMissing(name)
    else:
        if apply_func:
            field = apply_func(field)
        return field

@node
def names(children, data, role, **kwargs):
    """Return formatted names."""

    assert not children
    persons = data.persons[role]
    return join(**kwargs) [[person.text for person in persons]].format_data(data)

@node
def optional(children, data):
    """If children contain a missing bibliography field, return None.
    Else return formatted children.
    """

    try:
        return richtext.Text(*_format_list(children, data))
    except FieldIsMissing:
        return None

@node
def optional_field(children, data, *args, **kwargs):
    assert not children
    return optional [field(*args, **kwargs)].format_data(data)

@node
def tag(children, data, name):
    """Wrap text into a tag.

    >>> import pybtex.backends.html
    >>> html = pybtex.backends.html.Writer()
    >>> print tag('emph') ['important'].format().render(html)
    <em>important</em>
    >>> print sentence ['ready', 'set', tag('emph') ['go']].format().render(html)
    Ready, set, <em>go</em>.
    """
    parts = _format_list(children, data)
    return richtext.Tag(name, *_format_list(children, data))

@node
def first_of(children, data):
    """Return first nonempty child."""

    for child in _format_list(children, data):
        if child:
            return child
    return richtext.Text()
