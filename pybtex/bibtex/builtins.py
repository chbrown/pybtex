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

class Builtin(object):
    def __init__(self, f):
        self.f = f
    def execute(self, interpreter):
        self.f(interpreter)

def builtin(f):
    return Builtin(f)

@builtin
def operator_assign(i):
    var = i.pop()
    value = i.pop()
    var.set(value)

@builtin
def empty(i):
    #FIXME error checking
    s = i.pop()
    if s and not s.isspace():
        i.push(1)
    else:
        i.push(0)

@builtin
def preamble(i):
    #FIXME stub
    i.push('')

@builtin
def skip(i):
    pass

builtins = {
        ':=': operator_assign,
        'empty$': empty,
        'preamble$': preamble,
        'skip$': skip,
}
