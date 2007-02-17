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

"""Built-in functions for BibTeX interpreter.

CAUTION: functions should PUSH results, not RETURN
"""


class Builtin(object):
    def __init__(self, f):
        self.f = f
    def execute(self, interpreter):
        self.f(interpreter)
    def __repr__(self):
        return '<builtin %s>' % self.f.__name__

def builtin(f):
    return Builtin(f)

@builtin
def operator_more(i):
    arg1 = i.pop()
    arg2 = i.pop()
    if arg2 > arg1:
        i.push(1)
    else:
        i.push(0)

@builtin
def operator_less(i):
    arg1 = i.pop()
    arg2 = i.pop()
    if arg2 < arg1:
        i.push(1)
    else:
        i.push(0)

@builtin
def operator_equals(i):
    arg1 = i.pop()
    arg2 = i.pop()
    if arg2 == arg1:
        i.push(1)
    else:
        i.push(0)

@builtin
def operator_asterisk(i):
    arg1 = i.pop()
    arg2 = i.pop()
    i.push(arg2 + arg1)

@builtin
def operator_assign(i):
    var = i.pop()
    value = i.pop()
    var.set(value)

@builtin
def operator_plus(i):
    arg1 = i.pop()
    arg2 = i.pop()
    i.push(arg2 + arg1)

@builtin
def operator_minus(i):
    arg1 = i.pop()
    arg2 = i.pop()
    i.push(arg2 - arg1)


@builtin
def call_type(i):
    type = i.current_entry.type
    i.vars[type].execute(i)

@builtin
def cite(i):
    i.push(i.current_entry_key)

@builtin
def duplicate(i):
    tmp = i.pop()
    i.push(tmp)
    i.push(tmp)

@builtin
def empty(i):
    #FIXME error checking
    s = i.pop()
    if s and not s.isspace():
        i.push(1)
    else:
        i.push(0)

@builtin
def if_(i):
    f1 = i.pop()
    f2 = i.pop()
    p = i.pop()
    if p > 0:
        f1.execute(i)
    else:
        f2.execute(i)

@builtin
def int_to_str(i):
    i.push(str(i.pop()))

@builtin
def newline(i):
    # FIXME bibtex does some automatic line breaking
    # needs more investigation
    i.output('\n')

@builtin
def num_names(i):
    #FIXME stub
    i.push(1)

@builtin
def pop(i):
    i.pop()

@builtin
def preamble(i):
    #FIXME stub
    i.push('')

@builtin
def skip(i):
    pass

@builtin
def warning(i):
    #FIXME stub
    msg = i.pop()
    print 'WARNING:', msg


@builtin
def width(i):
    #FIXME need to investigate bibtex' source
    s = i.pop()
    i.push(len(s))

@builtin
def write(i):
    s = i.pop()
    i.output(s)

builtins = {
        '>': operator_more,
        '<': operator_less,
        '=': operator_equals,
        '+': operator_plus,
        '-': operator_minus,
        '*': operator_asterisk,
        ':=': operator_assign,
        'call.type$': call_type,
        'cite$': cite,
        'duplicate$': duplicate,
        'empty$': empty,
        'if$': if_,
        'int.to.str$': int_to_str,
        'newline$': newline,
        'num.names$': num_names,
        'pop$': pop,
        'preamble$': preamble,
        'skip$': skip,
        'warning$': warning,
        'width$': width,
        'write$': write,
}
