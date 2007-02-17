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

import re
from pyparsing import (Literal, Suppress, QuotedString, Word,
        alphas, alphanums, printables, Regex, lineno, line, col,
        Keyword, Forward, ZeroOrMore, OneOrMore, Group,
        restOfLine, StringEnd, ParserElement, downcaseTokens)
from pybtex.bibtex.interpreter import (Integer, String, QuotedVar,
        Identifier, FunctionLiteral, BibTeXError)

#ParserElement.enablePackrat()

def process_int_literal(s, loc, toks):
    try:
        return Integer(int(toks[0][1:]))
    except ValueError:
        raise BibTeXError('%i:%i invalid integer literal\n%s' %
                (lineno(loc, s), col(loc, s), line(loc, s)))

def process_string_literal(toks):
    return String(toks[0])

def process_identifier(toks):
    name = toks[0].lower()
    if name[0] == "'":
        return QuotedVar(name[1:])
    else:
        return Identifier(name)

def process_function(toks):
    return FunctionLiteral(toks[0])

comment = '%' + restOfLine
lbrace = Suppress('{')
rbrace = Suppress('}')
intLiteral = Regex(r'#-?\d+').setParseAction(process_int_literal)
stringLiteral = QuotedString('"').setParseAction(process_string_literal)
restrictedPrintables = ''.join(c for c in printables if not c in '#%^&{}_~\\')
nonnums = ''.join(c for c in restrictedPrintables if not c.isdigit())
identifier = Word(nonnums, restrictedPrintables).setParseAction(process_identifier)
token = stringLiteral | intLiteral | identifier
tokenList = Forward()
tokenList.setParseAction(process_function)
tokenList << Group(lbrace + ZeroOrMore(token | tokenList) + rbrace)
commandName = Word(alphas).setParseAction(downcaseTokens)
arg = Group(lbrace + ZeroOrMore(token | tokenList) + rbrace)
command = commandName + ZeroOrMore(arg)
bstGrammar = OneOrMore(command) + StringEnd()
bstGrammar.ignore(comment)

parse_file = bstGrammar.parseFile


if __name__ == '__main__':
    import sys
    print bstGrammar.parseFile(sys.argv[1])
