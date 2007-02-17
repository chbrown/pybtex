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


class BibTeXError(Exception):
    pass


class Variable(object):
    def __init__(self, value = None):
        self.set(value)
    def set(self, value):
        if isinstance(value, self.value_type) or value is None:
            self._value = value
        else:
            raise ValueError('Invalid value for BibTeX %s: %s' % (self.__class__.__name__, value))
    def execute(self, interpreter):
        if self._value is None:
            raise ValueError('undefined %s variable' % self.__class__.__name__)
        interpreter.push(self._value)
    def value(self):
        return self._value


class Integer(Variable):
    value_type = int
    def __repr__(self):
        return str(self.value())


class String(Variable):
    value_type = basestring
    def __repr__(self):
        return '"%s"' % self.value()


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
    def isempty(self):
        if self.body and not self.body.isspace():
            return 1
        else:
            return 0
    def __repr__(self):
        return repr(self.body)


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
        print 'ENTRY'
        self.getToken()
        self.getToken()
        self.getToken()

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
        print 'ITERATE'
        self.getToken()

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
