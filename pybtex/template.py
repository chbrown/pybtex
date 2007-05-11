#: Copyright 2006 Andrey Golovizin
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

>>> from pybtex.backends import latex
>>> backend = latex.Writer()
>>> class Entry:
...     fields = {'title': 'The Book of Pybtex', 'author': 'Ero-sennin'}
>>> e = Entry()
>>> template = join(' ') [
...     field('title'),
...     ['by', field('author')],
...     '--',
...     (str(i) for i in range(10))
... ]
>>> print template.format(e).render(backend)
The Book of Pybtex by Ero-sennin -- 0 1 2 3 4 5 6 7 8 9

>>> template = join ['Abra', 'kadabra', '!!!']
>>> print template.format(e).render(backend)
Abrakadabra!!!

>>> template = phrase ['one', 'two']
>>> print template.format(e).render(backend)
one, two

>>> template = phrase (sep2 = ' and ', last_sep = ' ,and ') ['one', 'two']
>>> print template.format(e).render(backend)
one and two

>>> template = phrase (sep2 = ' and ', last_sep = ', and ') [
... 'one',
... 'two',
... 'three',
... 'four']
>>> print template.format(e).render(backend)
one, two, three, and four
"""

from pybtex.richtext import Text

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
        
def flatten(l):
    """Flat iterator over nested lists. Also wrap strings into quote objects.

    >>> [i for i in flatten([1, (2, 3, [4, 5])])]
    [1, 2, 3, 4, 5]
    
    >>> for i in flatten([['here we', 'have'], ['some', 'words']]):
    ...     print i.format(None)
    here we
    have
    some
    words
    """
    if isinstance(l, (TemplateElement, TemplateElementProto)):
        yield l
    elif isinstance(l, basestring):
        yield quote(l)
    else:
        try:
            for i in l:
                for tmp in flatten(i):
                    yield tmp
        except TypeError:
            yield l

class TemplateElementProto(object):
    def __init__(self, f):
        self.f = f
    def __call__(self, *args, **kwargs):
        return TemplateElement(self.f)(*args, **kwargs)
    def __getitem__(self, children):
        return TemplateElement(self.f)[children]

class TemplateElement(object):
    def __init__(self, f):
        self.formatter = f
        self.children = []
        self.args = []
        self.kwargs = {}
    def __call__(self, *args, **kwargs):
        self.args.extend(args)
        self.kwargs.update(kwargs)
        return self
    def __getitem__(self, children):
        self.children.extend(flatten(children))
        return self
    def format(self, entry):
        formatted_children = [child.format(entry) for child in self.children]
        return self.formatter(entry, formatted_children, *self.args, **self.kwargs)

def template(f):
    return TemplateElementProto(f)

@template
def quote(entry, children, s):
    """do nothing and return unmodified output"""
    return s

@template
def field(entry, children, name):
    return entry.fields[name]

@template
def join(entry, children, sep=''):
    if children:
        result = Text(children[0])
        for child in children[1:]:
            result.append(sep)
            result.append(child)
        return result
    else:
        return Text()

@template
def phrase(entry, children, sep=', ', last_sep=None, sep2=None):
    if last_sep is None:
        last_sep = sep
    if sep2 is None:
        sep2 = last_sep

#    children = [child.format(entry) for child in children]
    if not children:
        return Text()
    elif len(children) == 1:
        return Text(children[0])
    elif len(children) == 2:
        return Text(children[0], sep2, children[1])
    else:
        result = Text()
        for child in children[:-2]:
            result.append(child)
            result.append(sep)
        result.append(children[-2])
        result.append(last_sep)
        result.append(children[-1])
        return result

#        def output_part(part, sep):
#            if part[1] is not None:
#                sep = part[1]
#            if sep:
#                result.append(sep)
#            result.append(part[0].format(entry))

#        if not self._list:
#            result = Text()
#        elif len(self._list) == 1:
#            result = Text(self._list[0][0].format(entry))
#        elif len(self._list) == 2:
#            sep = self._list[1][1]
#            if sep is None:
#                sep = self.sep2
#            result = Text(self._list[0][0].format(entry), sep, self._list[1][0].format(entry))
#        else:
#            result = Text()
#            output_part(self._list[0], sep='')
#            for part in self._list[1:-1]:
#                output_part(part, self.sep)
#            output_part(self._list[-1], self.last_sep)

#        return result

if __name__ == "__main__":
    class Entry(object):
        fields = {'title': 'The Book of Pybtex', 'author': 'Densetsu no Ero-sennin'}
    e = Entry()
    template = join(' ') [field('title'), ['lopata'], (str(i) for i in range(10))]
    print template.format(e)
