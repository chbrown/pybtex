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

"""Built-in functions for BibTeX interpreter.

CAUTION: functions should PUSH results, not RETURN
"""

import pybtex.io
from pybtex.bibtex.exceptions import BibTeXError
from pybtex.bibtex import utils
from pybtex.core import Person
from pybtex.bibtex.names import format as format_bibtex_name

class Builtin(object):
    def __init__(self, f):
        self.f = f
    def execute(self, interpreter):
        self.f(interpreter)
    def __repr__(self):
        return '<builtin %s>' % self.f.__name__

builtins = {}

def builtin(name):
    def _builtin(f):
        b = Builtin(f)
        builtins[name] = b
    return _builtin

@builtin('>')
def operator_more(i):
    arg1 = i.pop()
    arg2 = i.pop()
    if arg2 > arg1:
        i.push(1)
    else:
        i.push(0)

@builtin('<')
def operator_less(i):
    arg1 = i.pop()
    arg2 = i.pop()
    if arg2 < arg1:
        i.push(1)
    else:
        i.push(0)

@builtin('=')
def operator_equals(i):
    arg1 = i.pop()
    arg2 = i.pop()
    if arg2 == arg1:
        i.push(1)
    else:
        i.push(0)

@builtin('*')
def operator_asterisk(i):
    arg1 = i.pop()
    arg2 = i.pop()
    i.push(arg2 + arg1)

@builtin(':=')
def operator_assign(i):
    var = i.pop()
    value = i.pop()
    var.set(value)

@builtin('+')
def operator_plus(i):
    arg1 = i.pop()
    arg2 = i.pop()
    i.push(arg2 + arg1)

@builtin('-')
def operator_minus(i):
    arg1 = i.pop()
    arg2 = i.pop()
    i.push(arg2 - arg1)

@builtin('add.period$')
def add_period(i):
    s = i.pop()
    if s and not s.rstrip('}')[-1] in '.?!':
        s += '.'
    i.push(s)

@builtin('call.type$')
def call_type(i):
    type = i.current_entry.type
    i.vars[type].execute(i)

@builtin('change.case$')
def change_case(i):

    mode = i.pop()
    string = i.pop()

    if not mode:
        raise BibTeXError('empty mode string passed to change.case$')
    mode_letter = mode[0].lower()
    if not mode_letter in ('l', 'u', 't'):
        raise BibTeXError('incorrect change.case$ mode: %s' % mode)

    i.push(utils.change_case(string, mode_letter))

@builtin('chr.to.int$')
def chr_to_int(i):
    s = i.pop()
    try:
        value = ord(s)
    except TypeError:
        raise BibTeXError('%s passed to chr.to.int$', s)
    i.push(value)

@builtin('cite$')
def cite(i):
    i.push(i.current_entry_key)

@builtin('duplicate$')
def duplicate(i):
    tmp = i.pop()
    i.push(tmp)
    i.push(tmp)

@builtin('empty$')
def empty(i):
    #FIXME error checking
    s = i.pop()
    if s and not s.isspace():
        i.push(0)
    else:
        i.push(1)

@builtin('format.name$')
def format_name(i):
    format = i.pop()
    n = i.pop()
    names = i.pop()
    name = utils.split_name_list(names)[n - 1]
    i.push(format_bibtex_name(name, format))

@builtin('if$')
def if_(i):
    f1 = i.pop()
    f2 = i.pop()
    p = i.pop()
    if p > 0:
        f2.execute(i)
    else:
        f1.execute(i)

@builtin('int.to.chr$')
def int_to_chr(i):
    n = i.pop()
    try:
        char = chr(n)
    except ValueError:
        raise BibTeXError('%i passed to int.to.chr$', n)
    i.push(char)

@builtin('int.to.str$')
def int_to_str(i):
    i.push(str(i.pop()))

@builtin('missing$')
def missing(i):
    f = i.pop()
    if i.is_missing_field(f):
        i.push(1)
    else:
        i.push(0)

@builtin('newline$')
def newline(i):
    i.newline()

@builtin('num.names$')
def num_names(i):
    names = i.pop()
    i.push(len(utils.split_name_list(names)))

@builtin('pop$')
def pop(i):
    i.pop()

@builtin('preamble$')
def preamble(i):
    i.push(i.bib_data.preamble())

@builtin('purify$')
def purify(i):
    s = i.pop()
    i.push(utils.bibtex_purify(s))

@builtin('quote$')
def quote(i):
    i.push('"')

@builtin('skip$')
def skip(i):
    pass

@builtin('substring$')
def substring(i):
    length = i.pop()
    start = i.pop()
    string = i.pop()
    i.push(utils.bibtex_substring(string, start, length))

@builtin('stack$')
def stack(i):
    while i.stack:
        print >>pybtex.io.stdout, i.pop()

@builtin('swap$')
def swap(i):
    tmp1 = i.pop()
    tmp2 = i.pop()
    i.push(tmp1)
    i.push(tmp2)

@builtin('text.length$')
def text_length(i):
    s = i.pop()
    i.push(utils.bibtex_len(s))

@builtin('text.prefix$')
def text_prefix(i):
    l = i.pop()
    s = i.pop()
    i.push(utils.bibtex_prefix(s, l))

@builtin('top$')
def top(i):
    print >>pybtex.io.stdout, i.pop()

@builtin('type$')
def type_(i):
    i.push(i.current_entry.type)

@builtin('warning$')
def warning(i):
    msg = i.pop()
    print >>pybtex.io.stderr, 'Warning--' + msg

@builtin('while$')
def while_(i):
    f = i.pop()
    p = i.pop()
    while True:
        p.execute(i)
        if i.pop() <= 0:
            break
        f.execute(i)

@builtin('width$')
def width(i):
    #FIXME need to investigate bibtex' source
    s = i.pop()
    i.push(utils.bibtex_len(s))

@builtin('write$')
def write(i):
    s = i.pop()
    i.output(s)
