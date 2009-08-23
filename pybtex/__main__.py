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
import optparse
from os import path
from optparse import make_option
from pybtex.cmdline import CommandLine

class PybtexCommandLine(CommandLine):
    prog = 'pybtex'
    args = '[options] auxfile.aux'

    options = (
        (None, (
            make_option('-f', '--bibliography-format', dest='bib_format'),
            make_option('-b', '--output-backend', dest='output_backend'),
            make_option('-e', '--engine', dest='engine'),
            make_option('--label-style', dest='label_style'),
            make_option('--name-style', dest='name_style'),
            make_option('--abbreviate-names', action='store_true', dest='abbreviate_names'),
        )),
        ('encoding options', (
            make_option('--bibtex-encoding', dest='bib_encoding'),
            make_option('--bst-encoding', dest='bst_encoding'),
            make_option('--output-encoding', dest='output_encoding'),
        )),
    )
    option_defaults = {
        'engine': 'bibtex',
    }

    def run(self, options, args):
        from pybtex.plugin import find_plugin

        filename = args[0]
        ext = path.splitext(filename)[1]
        if not ext:
            filename = path.extsep.join([filename, 'aux'])

        kwargs = {}
        if options.label_style:
            kwargs['label_style'] = find_plugin('style.labels', options.label_style)
        if options.name_style:
            kwargs['name_style'] = find_plugin('style.names', options.name_style)
        if options.output_backend:
            kwargs['output_backend'] = find_plugin('backends', options.output_backend)
        if options.bib_format:
            kwargs['bib_format'] = find_plugin('database.input', options.bib_format)
        kwargs['abbreviate_names'] = bool(options.abbreviate_names)
        for option in ('bib_encoding', 'output_encoding', 'bst_encoding'):
            value = getattr(options, option)
            if value:
                kwargs[option] = value

        if options.engine == 'bibtex':
            from pybtex import bibtex as engine
        elif options.engine == 'pybtex':
            import pybtex as engine
        else:
            opt_parser.error('unknown engine %s' % options.engine)

        engine.make_bibliography(filename, **kwargs)

def main():
    PybtexCommandLine().main()

if __name__ == '__main__':
    from pybtex.exceptions import PybtexError
    try:
        main()
    except PybtexError, error:
        print 'ERROR: %s.' % error
        sys.exit(1)
