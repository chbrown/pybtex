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

import re


whitespace_re = re.compile('(\s)')

def wrap(string, width=79):
    def wrap_chunks(chunks, width, initial_indent='', subsequent_indent='  '):
        space_len = 1
        line = []
        lines = []
        current_width = 0
        indent = initial_indent

        def output(line, indent):
            if line:
                if line[0] == ' ':
                    line.pop(0)
                lines.append(indent + ''.join(line).rstrip())

        for chunk in chunks:
            max_width = width - len(indent)
            chunk_len = len(chunk)
            if current_width + chunk_len <= max_width:
                line.append(chunk)
                current_width += chunk_len
            else:
                output(line, indent)
                indent = subsequent_indent
                line = [chunk]
                current_width = chunk_len
        output(line, indent)
        return lines

    chunks = whitespace_re.split(string)
    return '\n'.join(wrap_chunks(chunks, width))


def bibtex_substring(string, start, length):
    """
    Return a substring of the given length, starting from the given position.

    start and length are 1-based. If start is < 0, it is counted from the end
    of the string.

    >>> print bibtex_substring('abcdef', 1, 3)
    abc
    >>> print bibtex_substring('abcdef', 2, 3)
    bcd
    >>> print bibtex_substring('abcdef', 2, 1000)
    bcdef
    >>> print bibtex_substring('abcdef', -1, 1)
    f
    >>> print bibtex_substring('abcdef', -1, 2)
    ef
    >>> print bibtex_substring('abcdef', -2, 3)
    cde
    >>> print bibtex_substring('abcdef', -2, 1000)
    abcde
    """

    if start > 0:
        start0 = start - 1
        end0 = start0 + length
    elif start < 0:
        end0 = len(string) + start + 1
        start0 = end0 - length
    else:
        raise BibTeXError('start=0 passed to substring$')
    return string[start0:end0]


def bibtex_len(string):
    r"""Return the number of characters in the string.

    Braces are ignored. "Special characters" are ignored. A "special character"
    is a substring at brace level 1, if the first character after the opening
    brace is a backslash, like in "de la Vall{\'e}e Poussin".

    >>> print bibtex_len(r"de la Vall{\'e}e Poussin")
    20
    >>> print bibtex_len(r"de la Vall{e}e Poussin")
    20
    >>> print bibtex_len(r"de la Vallee Poussin")
    20
    >>> print bibtex_len(r'\ABC 123')
    8
    >>> print bibtex_len(r'{\abc}')
    1
    >>> print bibtex_len(r'{\abc')
    1
    >>> print bibtex_len(r'}\abc')
    4
    >>> print bibtex_len(r'\abc}')
    4
    >>> print bibtex_len(r'\abc{')
    4
    >>> print bibtex_len(r'level 0 {1 {2}}')
    11
    >>> print bibtex_len(r'level 0 {\1 {2}}')
    9
    >>> print bibtex_len(r'level 0 {1 {\2}}')
    12
    """
    length = 0
    for char, brace_level in scan_bibtex_string(string):
        if char not in '{}':
            length += 1
    return length


def bibtex_prefix(string, num_chars):
    """Return the firxt num_char characters of the string.

    Braces and "special characters" are ignored, as in bibtex_len.  If the
    resulting prefix ends at brace level > 0, missing closing braces are
    appended.

    >>> print bibtex_prefix('abc', 1)
    a
    >>> print bibtex_prefix('abc', 5)
    abc
    >>> print bibtex_prefix('ab{c}d', 3)
    ab{c}
    >>> print bibtex_prefix('ab{cd}', 3)
    ab{c}
    >>> print bibtex_prefix('ab{cd', 3)
    ab{c}
    >>> print bibtex_prefix(r'ab{\cd}', 3)
    ab{\cd}
    >>> print bibtex_prefix(r'ab{\cd', 3)
    ab{\cd}

    """
    def prefix():
        length = 0
        for char, brace_level in scan_bibtex_string(string):
            yield char
            if char not in '{}':
                length += 1
            if length >= num_chars:
                break
        for i in range(brace_level):
            yield '}'
    return ''.join(prefix())


def bibtex_purify(string):
    r"""Strip special characters from the string.

    >>> print bibtex_purify('Abc 1234')
    Abc 1234
    >>> print bibtex_purify('Abc  1234')
    Abc  1234
    >>> print bibtex_purify('Abc-Def')
    Abc Def
    >>> print bibtex_purify('Abc-~-Def')
    Abc   Def
    >>> print bibtex_purify('{XXX YYY}')
    XXX YYY
    >>> print bibtex_purify('{XXX {YYY}}')
    XXX YYY
    >>> print bibtex_purify(r'XXX {\YYY} XXX')
    XXX  XXX
    >>> print bibtex_purify(r'{XXX {\YYY} XXX}')
    XXX YYY XXX
    >>> print bibtex_purify(r'\\abc def')
    abc def
    >>> print bibtex_purify('a@#$@#$b@#$@#$c')
    abc
    """

    def purify_iter():
        for char, brace_level in scan_bibtex_string(string):
            if brace_level == 1 and char.startswith('\\'):
                pass
            elif char.isalnum():
                yield char
            elif char.isspace() or char in '-~':
                yield ' '
    return ''.join(purify_iter())


class LookAheadIterator(object):
    def __init__(self, seq):
        self.iterable = iter(seq)
        self.buffer = []

    def __iter__(self):
        return self

    def peek(self):
        if self.buffer:
            return self.buffer[0]
        else:
            try:
                self.buffer.append(self.iterable.next())
            except StopIteration:
                return None
            else:
                return self.buffer[0]

    def poke(self, token):
        self.buffer.insert(0, token)

    def next(self):
        if self.buffer:
            return self.buffer.pop()
        else:
            return self.iterable.next()


def scan_bibtex_string(string):
    """ Yield (char, brace_level) tuples.

    "Special characters", as in bibtex_len, are treated as a single character

    """

    def scan(chars, level=0):
        results = find_closing_brace(chars, level)
        if level == 1 and chars.peek() == '\\':
            return group(results, level)
        else:
            return results

    def group(results, level):
        yield ''.join(char for char, _ in results), level
    
    def find_closing_brace(chars, level):
        for char in chars:
            if char == '{':
                yield char, level + 1
                for item in scan(chars, level + 1):
                    yield item
            elif char == '}' and level > 0:
                chars.poke(char)
                return
            else:
                yield char, level
    
    return scan(LookAheadIterator(string))


def split_name_list(string):
    """
    Split a list of names, separated by ' and '.

    >>> split_name_list('Johnson and Peterson')
    ['Johnson', 'Peterson']
    >>> split_name_list('Armand and Peterson')
    ['Armand', 'Peterson']
    >>> split_name_list('Armand and anderssen')
    ['Armand', 'anderssen']
    >>> split_name_list('What a Strange{ }and Bizzare Name! and Peterson')
    ['What a Strange{ }and Bizzare Name!', 'Peterson']
    >>> split_name_list('What a Strange and{ }Bizzare Name! and Peterson')
    ['What a Strange and{ }Bizzare Name!', 'Peterson']
    """
    return split_tex_string(string, ' and ')

def split_tex_string(string, sep=None, strip=True, filter_empty=False):
    """Split a string using the given separator (regexp).

    Everything at brace level > 0 is ignored.
    Separators at the edges of the string are ignored.

    >>> split_tex_string('')
    []
    >>> split_tex_string('     ')
    []
    >>> split_tex_string('   ', ' ', strip=False, filter_empty=False)
    [' ', ' ']
    >>> split_tex_string('.a.b.c.', r'\.')
    ['.a', 'b', 'c.']
    >>> split_tex_string('.a.b.c.{d.}.', r'\.')
    ['.a', 'b', 'c', '{d.}.']
    >>> split_tex_string('Matsui      Fuuka')
    ['Matsui', 'Fuuka']
    >>> split_tex_string('{Matsui      Fuuka}')
    ['{Matsui      Fuuka}']
    >>> split_tex_string('a')
    ['a']
    >>> split_tex_string('on a')
    ['on', 'a']
    """

    if sep is None:
        sep = '[\s~]+'
        filter_empty = True
    sep_re = re.compile(sep)
    brace_level = 0
    name_start = 0
    result = []
    string_len = len(string)
    pos = 0
    for pos, char in enumerate(string):
        if char == '{':
            brace_level += 1
        elif char == '}':
            brace_level -= 1
        elif brace_level == 0 and pos > 0:
            match = sep_re.match(string[pos:])
            if match:
                sep_len = len(match.group())
                if pos + sep_len < string_len:
                    result.append(string[name_start:pos])
                    name_start = pos + sep_len
    if name_start < string_len:
        result.append(string[name_start:])
    if strip:
        result = [part.strip() for part in result]
    if filter_empty:
        result = [part for part in result if part]
    return result
