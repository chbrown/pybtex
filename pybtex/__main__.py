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

from os import path
from optparse import make_option

from pybtex.cmdline import CommandLine

class PybtexCommandLine(CommandLine):
    prog = 'pybtex'
    args = '[options] auxfile.aux'
    description = 'BibTeX-compatible bibliography processor in Python'
    long_description = """

Pybtex reads citation information from a LaTeX .aux file and produces a
formatted bibliography. Pybtex understands BibTeX .bib and .bst style files and
can be used as a drop-in replacement for BibTeX.

Besides BibTeX .bib files, BibTeXML and YAML bibliography files are
supported.

It is also possible to define bibliography formatting styles in Python.

    """.strip()
    num_args = 1

    options = (
        (None, (
            make_option(
                '-f', '--bibliography-format', dest='bib_format',
                help='bibliograpy format (bibtex, bibtexml, bibyaml)',
                metavar='FORMAT',
            ),
            make_option(
                '-b', '--output-backend', dest='output_backend',
                help='output backend (latex, html, plaintext)',
                metavar='BACKEND',
            ),
            make_option(
                '-l', '--style-language', dest='style_language',
                help='style definition language to use (bibtex or python)',
                metavar='LANGUAGE',
            ),
            make_option(
                '--label-style', dest='label_style',
                help='label formatting style',
                metavar='STYLE',
            ),
            make_option(
                '--name-style', dest='name_style',
                help='name formatting style',
                metavar='STYLE',
            ),
            make_option(
                '--abbreviate-names',
                action='store_true', dest='abbreviate_names',
                help='use abbreviated name formatting style',
            ),
    )),
        ('Encoding options', (
            make_option(
                '-e', '--encoding', dest='encoding', metavar='ENCODING',
                help='default encoding',
            ),
            make_option('--bibtex-encoding', dest='bib_encoding', metavar='ENCODING'),
            make_option('--bst-encoding', dest='bst_encoding', metavar='ENCODING'),
            make_option('--output-encoding', dest='output_encoding', metavar='ENCODING'),
        )),
    )
    option_defaults = {
        'style_language': 'bibtex',
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
            value = getattr(options, option) or options.encoding
            if value:
                kwargs[option] = value

        if options.style_language == 'bibtex':
            from pybtex import bibtex as engine
        elif options.style_language == 'python':
            import pybtex as engine
        else:
            self.opt_parser.error('unknown style language %s' % options.style_language)

        engine.make_bibliography(filename, **kwargs)

main = PybtexCommandLine()

if __name__ == '__main__':
    main()
