#!/usr/bin/env python

# Copyright (C) 2006, 2007, 2008, 2009  Andrey Golovizin
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

import sys
import re
from os import path
from tempfile import mkdtemp
from shutil import rmtree
from subprocess import Popen, PIPE

from pybtex.database.output import bibtex
from pybtex.database import BibliographyData
from pybtex.core import Person, Entry


writer = bibtex.Writer(encoding='ascii')


def write_aux(filename, citations):
    with open(filename, 'w') as aux_file:
        for citation in citations:
            aux_file.write('\\citation{%s}\n' % citation)
        aux_file.write('\\bibdata{test}\n')
        aux_file.write('\\bibstyle{test}\n')


def write_bib(filename, database):
    writer.write_file(database, filename)


def write_bst(filename, style):
    with open(filename, 'w') as bst_file:
        bst_file.write(style)
        bst_file.write('\n')


def run_bibtex(style, database, citations=None):
    if citations is None:
        citations = database.entries.keys()
    tmpdir = mkdtemp(prefix='pybtex_test_')
    try:
        write_bib(path.join(tmpdir, 'test.bib'), database)
        write_aux(path.join(tmpdir, 'test.aux'), citations)
        write_bst(path.join(tmpdir, 'test.bst'), style)
        bibtex = Popen(('bibtex', 'test'), cwd=tmpdir, stdout=PIPE, stderr=PIPE)
        stdout, stderr = bibtex.communicate()
        if bibtex.returncode:
            raise ValueError(stdout)
        with open(path.join(tmpdir, 'test.bbl')) as bbl_file:
            result = bbl_file.read()
        return result
    finally:
        pass
        rmtree(tmpdir)


def execute(code, database=None):
    if database is None:
        database = BibliographyData(entries={'test_entry': Entry('article')})
    bst = """
        ENTRY {name format} {} {}
        FUNCTION {article}
        {
            %s write$ newline$
        }
        READ
        ITERATE {call.type$}
    """.strip() % code
    [result] = run_bibtex(bst, database).splitlines()
    return result


def format_name(name, format):
    return execute('"%s" #1 "%s" format.name$' % (name, format))


def parse_name(name):
    space = re.compile('[\s~]+')
    formatted_name = format_name(name, '{ff}|{vv}|{ll}|{jj}')
    parts = [space.sub(' ', part.strip()) for part in formatted_name.split('|')]
    first, von, last, junior = parts
    return Person(first=first, prelast=von, last=last, lineage=junior)


def main():
    args = sys.argv[1:2]
    if len(args) != 1:
        print "usage: run_bibtex 'some bibtex code'"
        sys.exit(1)
    code = args[0]
    print execute(code)


if __name__ == '__main__':
    main()
