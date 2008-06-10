#!/usr/bin/env python
#vim:fileencoding=utf-8

"""
>>> from pybtex.core import Entry, Person
>>> author = Person(first='First', last='Last', middle='Middle')
>>> fields = {
...         'title': 'The Book',
...         'year': '2000',
... }
>>> e = Entry('book', fields=fields)
>>> book_format = Sentence(sep=', ') [
...     Field('title'), Field('year'), Optional [Field('sdf')]
... ]
>>> print book_format.format_data(e).plaintext()
The Book, 2000.
"""

from pybtex.richtext import Text

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
        return Node(*self.args, **self.kwargs).render(*args, **kwargs)


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
        params = []
        args_repr = ', '.join(repr(arg) for arg in self.args)
        if args_repr:
            params.append(args_repr)
        kwargs_repr = ', '.join('%s=%s' % (key, repr(value))
                for (key, value) in self.kwargs.items())
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
        return self.f(self.children, data, *self.args, **self.kwargs)


def _format_data(node, data):
    try:
        f = node.format_data
    except AttributeError:
        return unicode(node)
    else:
        return f(data)

def _format_list(list_, data):
    return [_format_data(part, data) for part in list_]

def _strip(list_):
    def empty(part):
        return not bool(part)
    from itertools import dropwhile
    tmp = list(dropwhile(empty, reversed(list_)))
    return list(dropwhile(empty, reversed(tmp)))

def node(f):
    return Proto(f.__name__, f)

@node
def Phrase(children, data, sep='', sep2=None, last_sep=None):
    if sep2 is None:
        sep2 = sep
    if last_sep is None:
        last_sep = sep
    parts = _strip(_format_list(children, data))
    if len(parts) <= 1:
        return Text(*parts)
    elif len(parts) == 2:
        return Text(sep2).join(parts)
    else:
        return Text(last_sep).join([Text(sep).join(parts[:-1]), parts[-1]])

List = Phrase(sep=', ')

@node
def Sentence(children, data, sep=' '):
    text = Phrase(sep) [children].format_data(data)
    text.capfirst()
    text.add_period()
    return text

class FieldIsMissing(Exception):
    pass

@node
def Field(children, data, name):
    assert not children
    try:
        field = data.fields[name]
    except KeyError:
        raise FieldIsMissing(name)
    else:
        return field

@node
def Optional(children, data):
    try:
        return Text(*_format_list(children, data))
    except FieldIsMissing:
        return None
