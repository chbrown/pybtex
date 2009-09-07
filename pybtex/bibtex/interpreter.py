# Copyright (C) 2007, 2008, 2009  Andrey Golovizin
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
        output = wrap(''.join(self.output_buffer))
        self.output_file.write(output)
        self.output_file.write('\n')
        self.output_buffer = []

    def run(self, bst_script, citations, bib_files, bbl_file):
        self.bst_script = iter(bst_script)
        self.citations = citations
        self.bib_files = bib_files
        self.output_file = bbl_file

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
        self.add_variable('crossref', Field(self, 'crossref'))
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

    def expand_wildcard_citations(self):
        for citation in self.citations:
            if citation == '*':
                for key in self.bib_data.entries.iterkeys():
                    yield key
            else:
                yield citation

    def command_read(self):
#        print 'READ'
        p = self.bib_format.Parser(encoding=self.bib_encoding, macros=self.macros, person_fields=[])
        self.bib_data = p.parse_files(self.bib_files)
        self.citations = list(self.expand_wildcard_citations())
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
