# Copyright (C) 2006, 2007, 2008  Andrey Golovizin
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

"""convert bibliography database from one format to another
"""
from os import path
from pybtex.plugin import find_plugin

class ConvertError(Exception):
    pass

def convert(input, from_format, to_format, output=None, input_encoding=None, output_encoding=None, parser_options={}):
    input_format = find_plugin('database.input', from_format)
    output_format = find_plugin('database.output', to_format)
    
    base_filename, ext = path.splitext(input)
    if not ext:
        input = path.extsep.join([input, input_format.file_extension])

    if output:
        if not path.splitext(output)[1]:
            output = path.extsep.join([output, output_format.file_extension])
    else:
        output = path.extsep.join([base_filename, output_format.file_extension])

    if input == output:
        raise ConvertError('input and output file can not be the same')

    bib_data = input_format.Parser(input_encoding, **parser_options).parse_file(input)
    output_format.Writer(output_encoding).write(bib_data, output)
