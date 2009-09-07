#!/usr/bin/env python

# Copyright 2006 Andrey Golovizin
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

from optparse import make_option

from pybtex.cmdline import CommandLine

class PybtexConvertCommandLine(CommandLine):
    prog = 'pybtex-convert'
    args = '[options] in_filename out_filename' 
    description = 'convert between bibliography database formats'
    long_description = """

pybtex-convert converts bibliography database files between supported formats
(currently BibTeX, BibTeXML and YAML).

    """.strip()

    num_args = 2

    options = (
        (None, (
            make_option(
                '-f', '--from', action='store', type='string', dest='from_format',
                help='input format', metavar='FORMAT',
            ),
            make_option(
                '-t', '--to', action='store', type='string', dest='to_format',
                help='output format', metavar='FORMAT',
            ),
            make_option(
                '--allow-keyless-bibtex-entries',
                action='store_true', dest='allow_keyless_entries',
                help='allow BibTeX entries without keys and generate unnamed-<number> keys for them'
            ),
        )),
        ('encoding options', (
            make_option(
                '-e', '--encoding',
                action='store', type='string', dest='encoding',
                help='default encoding',
                metavar='ENCODING',
            ),
            make_option(
                '--input-encoding',
                action='store', type='string', dest='input_encoding',
                metavar='ENCODING',
            ),
            make_option(
                '--output-encoding',
                action='store', type='string', dest='output_encoding',
                metavar='ENCODING',
            ),
        )),
    )
    option_defaults = {
        'allow_keyless_entries': False,
    }

    def run(self, options, args):
        from pybtex.database.convert import convert, ConvertError

        convert(args[0], args[1],
                options.from_format,
                options.to_format,
                input_encoding=options.input_encoding or options.encoding,
                output_encoding=options.output_encoding or options.encoding,
                parser_options = {'allow_keyless_entries': options.allow_keyless_entries})

main = PybtexConvertCommandLine()

if __name__ == '__main__':
    main()
