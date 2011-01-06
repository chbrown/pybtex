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
