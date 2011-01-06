# Copyright (c) 2007, 2008, 2009, 2010, 2011  Andrey Golovizin
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

from pybtex.bibtex.exceptions import BibTeXError
from pybtex.bibtex.builtins import builtins
from pybtex.bibtex.utils import wrap
#from pybtex.database.input import bibtex


class Variable(object):

    def _undefined(self):
        raise NotImplementedError

    default = property(_undefined)
    value_type = property(_undefined)

    def __init__(self, value=None):
        self.set(value)
    def set(self, value):
        if value is None:
            value = self.default
        self.validate(value)
        self._value = value
    def validate(self, value):
        if not (isinstance(value, self.value_type) or value is None):
            raise ValueError('Invalid value for BibTeX %s: %s' % (self.__class__.__name__, value))
    def execute(self, interpreter):
        interpreter.push(self.value())
    def value(self):
        return self._value


class EntryVariable(Variable):
    def __init__(self, interpreter, name):
        Variable.__init__(self)
        self.interpreter = interpreter
        self.name = name
    def set(self, value):
        if value is not None:
            self.validate(value)
            self.interpreter.current_entry.vars[self.name] = value
    def value(self):
        try:
            return self.interpreter.current_entry.vars[self.name]
        except KeyError:
            return None


class Integer(Variable):
    value_type = int
    default = 0
    def __repr__(self):
        return str(self.value())


class EntryInteger(Integer, EntryVariable):
    pass


class String(Variable):
    value_type = basestring
    default = ''
    def __repr__(self):
        if self.value() is None:
            return '<empty>'
        #FIXME encodings
        return '"%s"' % self.value().encode('UTF-8')


class EntryString(String, EntryVariable):
    pass


class MissingField(str):
    def __new__(cls, name):
        self = str.__new__(cls)
        self.name = name
        return self
    def __repr__(self):
        return 'MISSING<%s>' % self.name
    def __nonzero__(self):
        return False


class Field(object):
    def __init__(self, interpreter, name):
        self.interpreter = interpreter
        self.name = name

    def execute(self, interpreter):
        self.interpreter.push(self.value())

    def value(self):
        try:
            return self.interpreter.current_entry.fields[self.name]
        except KeyError:
            return MissingField(self.name)


class Crossref(Field):
    def __init__(self, interpreter):
        super(Crossref, self).__init__(interpreter, 'crossref')

    def value(self):
        entry = self.interpreter.current_entry
        interpreter = self.interpreter
        crossref = interpreter.current_entry.fields.get('crossref')
        crossrefs = interpreter.bib_data.crossref_counts.get(crossref, 0)
        if (
            crossref in self.interpreter.citations
            or crossrefs >= self.interpreter.min_crossrefs
        ):
            return super(Crossref, self).value()
        else:
            return MissingField(self.name)


class Identifier(Variable):
    value_type = basestring
    def execute(self, interpreter):
        try:
            f = interpreter.vars[self.value()]
        except KeyError:
            raise BibTeXError('can not execute undefined function %s' % self)
        f.execute(interpreter)
    def __repr__(self):
        return self.value()


class QuotedVar(Variable):
    value_type = basestring
    def execute(self, interpreter):
        try:
            var = interpreter.vars[self.value()]
        except KeyError:
            raise BibTeXError('can not push undefined variable %s' % self.value())
        interpreter.push(var)
    def __repr__(self):
        return "'%s" % self.value()


class Function(object):
    def __init__(self, body=None):
        if body is None:
            body = []
        self.body = body
    def execute(self, interpreter):
#        print 'executing function', self.body
        for element in self.body:
            element.execute(interpreter)
    def __repr__(self):
        return repr(self.body)


class FunctionLiteral(Function):
    def execute(self, interpreter):
        interpreter.push(Function(self.body))


class Interpreter(object):
    def __init__(self, bib_format, bib_encoding):
        self.bib_format = bib_format
        self.bib_encoding = bib_encoding
        self.stack = []
        self.vars = dict(builtins)
        #FIXME is 10000 OK?
        self.add_variable('global.max$', Integer(10000))
        self.add_variable('entry.max$', Integer(10000))
        self.add_variable('sort.key$', EntryString(self, 'sort.key$'))
        self.macros = {}
        self.output_buffer = []

    def push(self, value):
#        print 'push <%s>' % value
        self.stack.append(value)
#        print 'stack:', self.stack

    def pop(self):
        try:
            value = self.stack.pop()
        except IndexError:
            raise BibTeXError('pop from empty stack')
#        print 'pop <%s>' % value
        return value

    def get_token(self):
        return self.bst_script.next()

    def add_variable(self, name, value):
        if name in self.vars:
            raise BibTeXError('variable %s already declared' % name)
        self.vars[name] = value

    def output(self, string):
        self.output_buffer.append(string)

    def newline(self):
        output = wrap(u''.join(self.output_buffer))
        self.output_file.write(output)
        self.output_file.write(u'\n')
        self.output_buffer = []

    def run(self, bst_script, citations, bib_files, bbl_file, min_crossrefs):
        self.bst_script = iter(bst_script)
        self.citations = citations
        self.bib_files = bib_files
        self.output_file = bbl_file
        self.min_crossrefs = min_crossrefs

        for i in self.bst_script:
            commandname = 'command_' + i
            if hasattr(self, commandname):
                getattr(self, commandname)()
            else:
                print 'Unknown command', commandname

        self.output_file.close()

    def command_entry(self):
        for id in self.get_token():
            name = id.value()
            self.add_variable(name, Field(self, name))
        self.add_variable('crossref', Crossref(self))
        for id in self.get_token():
            name = id.value()
            self.add_variable(name, EntryInteger(self, name))
        for id in self.get_token():
            name = id.value()
            self.add_variable(name, EntryString(self, name))

    def command_execute(self):
#        print 'EXECUTE'
        self.get_token()[0].execute(self)

    def command_function(self):
        name = self.get_token()[0].value()
        body = self.get_token()
        self.vars[name] = Function(body)

    def command_integers(self):
#        print 'INTEGERS'
        for id in self.get_token():
            self.vars[id.value()] = Integer()

    def command_iterate(self):
        self._iterate(self.citations)

    def _iterate(self, citations):
        f = self.vars[self.get_token()[0].value()]
        for key in citations:
            self.current_entry_key = key
            self.current_entry = self.bib_data.entries[key]
            f.execute(self)
        self.currentEntry = None

    def command_macro(self):
        name = self.get_token()[0].value()
        value = self.get_token()[0].value()
        self.macros[name] = value

    def expand_wildcard_citations(self, citations):
        for citation in citations:
            if citation == '*':
                for key in self.bib_data.entries.iterkeys():
                    yield key
            else:
                yield citation

    def add_crossreferenced_citations(self, citations):
        citation_set = set(citations)
        extra_citations = self.bib_data.get_extra_citations(self.min_crossrefs)
        return citations + [citation for citation in extra_citations if citation not in citation_set]

    def command_read(self):
#        print 'READ'
        p = self.bib_format(encoding=self.bib_encoding, macros=self.macros, person_fields=[])
        self.bib_data = p.parse_files(self.bib_files)
        citations = list(self.expand_wildcard_citations(self.citations))
        self.citations = self.add_crossreferenced_citations(citations)
#        for k, v in self.bib_data.iteritems():
#            print k
#            for field, value in v.fields.iteritems():
#                print '\t', field, value
#        pass

    def command_reverse(self):
        self._iterate(reversed(self.citations))

    def command_sort(self):
        def key(citation):
            return self.bib_data.entries[citation].vars['sort.key$']
        self.citations.sort(key=key)

    def command_strings(self):
        #print 'STRINGS'
        for id in self.get_token():
            self.vars[id.value()] = String()

    @staticmethod
    def is_missing_field(field):
        return isinstance(field, MissingField)
