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
# along with rdiff-backup; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

"""convert bibliography database from one format to another
"""
from os import path
from pybtex import find_plugin

class ConvertError(Exception):
    pass

def convert(input, from_format, to_format, output=None, input_encoding=None, output_encoding=None):
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

    bib_data = input_format.Parser(input_encoding).parse_file(input)
    output_format.Writer(output_encoding).write(bib_data, output)
