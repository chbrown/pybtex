#!/usr/bin/env python
#vim:fileencoding=utf-8

from pybtex.core import Entry

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
        kwargs_repr = ', '.join('%s=%s' % (key, repr(value)) for (key, value) in self.kwargs.items())
        if kwargs_repr:
            params.append(kwargs_repr)
        if params:
            params_repr = '(%s)' % ', '.join(params)
        else:
            params_repr = ''

        if self.children:
            children_repr = ' [%s]' % ', '.join(repr(child) for child in self.children)
        else:
            children_repr = ''

        return ''.join([self.name, params_repr, children_repr])

    def format_data(self, data):
        return self.f(self.children, data, *self.args, **self.kwargs)

def format_data(node, data):
    try:
        f = node.format_data
    except AttributeError:
        return unicode(node)
    else:
        return f(data)

def node(f):
    return Proto(f.__name__, f)

@node
def phrase(children, data, sep=', ', sep2=None, last_sep=None):
    if sep2 is None:
        sep2 = sep
    if last_sep is None:
        last_sep = sep
    parts = [format_data(child, data) for child in children]
    if len(parts) <= 1:
        return ''.join(parts)
    elif len(parts) == 2:
        return sep2.join(parts)
    else:
        return sep.join(parts[:-1]) + last_sep + parts[-1]

text = phrase(sep='')
