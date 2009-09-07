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

from pyparsing import (Suppress, QuotedString, Word,
        alphas, printables, Regex, lineno, line, col,
        Forward, ZeroOrMore, OneOrMore, Group,
        restOfLine, StringEnd, ParserElement, downcaseTokens)
from pybtex.bibtex.interpreter import (Integer, String, QuotedVar,
        Identifier, FunctionLiteral, BibTeXError)
import pybtex.io

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
restrictedPrintables = ''.join(c for c in printables if not c in '#%^&{}~\\')
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

# sloooooow
# bstGrammar.ignore(comment)

# somewhat faster
def strip_comment(line):
    """Strip the commented part of the line."

    >>> print strip_comment('a normal line')
    a normal line
    >>> print strip_comment('a normal line% and a comment')
    a normal line
    >>> print strip_comment('"100% compatibility" is a myth')
    "100% compatibility" is a myth
    >>> print strip_comment('"100% compatibility" is a myth% or not?')
    "100% compatibility" is a myth

    """
    quotes = 0
    pos = 0
    for char in line:
        if char == '"':
            quotes += 1
        elif char == '%':
            if quotes % 2 == 0:
                break 
        pos += 1
    return line[:pos]

def parse_file(filename, encoding):
    bst_file = pybtex.io.open_unicode(filename, encoding=encoding)
    bst = ''.join(strip_comment(line) for line in bst_file)
    return bstGrammar.parseString(bst)


if __name__ == '__main__':
    import sys
    print parse_file(sys.argv[1])
