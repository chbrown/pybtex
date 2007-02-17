# Copyright 2007 Andrey Golovizin
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

from builtins import builtins
from pybtex.database.input import bibtex

from pybtex.core import Entry
valid_roles = Entry.valid_roles
del Entry


class BibTeXError(Exception):
    pass


class Variable(object):
    def __init__(self, value = None):
        self.set(value)
    def set(self, value):
        self.validate(value)
        self._value = value
    def validate(self, value):
        if not (isinstance(value, self.value_type) or value is None):
            raise ValueError('Invalid value for BibTeX %s: %s' % (self.__class__.__name__, value))
    def execute(self, interpreter):
        if self.value() is None:
            raise ValueError('undefined %s variable' % self.__class__.__name__)
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
    def __repr__(self):
        return str(self.value())


class EntryInteger(Integer, EntryVariable):
    pass


class String(Variable):
    value_type = basestring
    def __repr__(self):
        return '"%s"' % self.value()


class EntryString(String, EntryVariable):
    pass


class MissingField(object):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return 'MISSING<%s>' % self.name


class Field(object):
    def __init__(self, interpreter, name):
        self.interpreter = interpreter
        self.name = name

    def execute(self, interpreter):
        self.interpreter.push(self.value())

    def value(self):
        #FIXME: need to do something with names
        if self.name in valid_roles:
            return 'Foo Bar Baz, jr'
        try:
            value = self.interpreter.current_entry.fields[self.name]

            #FIXME that's because of (ugly) defaultdict never failing
            if not value:
                value = None
            return value

        except KeyError:
            return MissingField


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
    def __init__(self, body = []):
        self.body = body
    def execute(self, interpreter):
        print 'executing function', self.body
        for element in self.body:
            element.execute(interpreter)
    def __repr__(self):
        return repr(self.body)


class FunctionLiteral(Function):
    def execute(self, interpreter):
        interpreter.push(Function(self.body))


class Interpreter(object):
    def __init__(self):
        self.stack = []
        self.vars = dict(builtins)
        self.macros = {}

    def push(self, value):
        print 'push <%s>' % value
        self.stack.append(value)
        print 'stack:', self.stack

    def pop(self):
        value = self.stack.pop()
        print 'pop <%s>' % value
        return value

    def getToken(self):
        return self.bst_script.next()

    def add_variable(self, name, value):
        if name in self.vars:
            raise BibTeXError('variable %s already declared' % name)
        self.vars[name] = value

    def output(self, string):
        self.output_file.write(string)

    def run(self, bst_script, citations, bib_file, bbl_file):
        self.bst_script = iter(bst_script)
        self.citations = citations
        self.bib_file = bib_file
        self.output_file = open(bbl_file, 'w')

        for i in self.bst_script:
            commandname = 'command_' + i
            if hasattr(self, commandname):
                getattr(self, commandname)()
            else:
                print 'Unknown command', commandname

        self.output_file.close()

    def command_entry(self):
        for id in self.getToken():
            name = id.value()
            self.add_variable(name, Field(self, name))
        for id in self.getToken():
            name = id.value()
            self.add_variable(name, EntryInteger(self, name))
        for id in self.getToken():
            name = id.value()
            self.add_variable(name, EntryString(self, name))

    def command_execute(self):
#        print 'EXECUTE'
        self.getToken()[0].execute(self)

    def command_function(self):
        name = self.getToken()[0].value()
        body = self.getToken()
        self.vars[name] = Function(body)

    def command_integers(self):
#        print 'INTEGERS'
        for id in self.getToken():
            self.vars[id.value()] = Integer()

    def command_iterate(self):
        f = self.vars[self.getToken()[0].value()]
        for key, entry in self.bib_data.iteritems():
            self.current_entry = entry
            self.current_entry_key = key
            f.execute(self)
        self.currentEntry = None

    def command_macro(self):
        name = self.getToken()[0].value()
        value = self.getToken()[0].value()
        self.macros[name] = value

    def command_read(self):
        print 'READ'
        p = bibtex.Parser()
        self.bib_data = p.parse_file(filename=self.bib_file, macros=self.macros)
#        for k, v in self.bib_data.iteritems():
#            print k
#            for field, value in v.fields.iteritems():
#                print '\t', field, value
#        pass

    def command_reverse(self):
        print 'REVERSE'
        self.getToken()

    def command_sort(self):
        print 'SORT'

    def command_strings(self):
        #print 'STRINGS'
        for id in self.getToken():
            self.vars[id.value()] = String()
