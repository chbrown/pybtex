# Copyright (C) 2009  Andrey Golovizin
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

# Based on autodoc_man.py from bzr-1.16.1.

"""Generate man pages for pybtex and pybtex-convert.
"""

import os
import sys
from datetime import datetime

from pybtex.__version__ import version


def write_manpage(outfile, main_obj):
    """Assembles a man page"""
    now = datetime.utcnow()
    params = {
        "cmd": main_obj.prog,
        "description": main_obj.description,
        "datestamp": now.strftime('%Y-%m-%d'),
        "timestamp": now.strftime('%Y-%m-%d %H:%M:%S +0000'),
        "version": version,
    }
    outfile.write(man_preamble % params)
    outfile.write(man_escape(man_head % params))

    write(outfile, format_synopsis(main_obj))
    write(outfile, format_description(main_obj))
    write(outfile, format_help(main_obj))

def write(outfile, lines):
    for line in lines:
        outfile.write(man_escape(line))
        outfile.write('\n')

def man_escape(string):
    """Escapes strings for man page compatibility"""
    result = string.replace("\\","\\\\")
    result = result.replace("`","\\`")
#    result = result.replace("'","\\'")
    result = result.replace("-","\\-")
    return result


def format_synopsis(main_obj):
    yield '.SH "SYNOPSIS"'
    yield '.B "%s"' % main_obj.prog
    for part in format_args(main_obj):
        yield part

def format_args(main_obj):
    for arg in main_obj.args.split():
        if arg.startswith('[') and arg.endswith(']'):
            yield '['
            yield '.I "%s"' % arg[1:-1]
            yield ']'
        else:
            yield '.I "%s"' % arg

def format_description(main_obj):
    yield '.SH "DESCRIPTION"'
    yield main_obj.long_description

def format_help(main_obj):
    opt_parser = main_obj.opt_parser
    for part in format_option_group(opt_parser, 'general optons', opt_parser.option_list):
        yield part
    for option_group in opt_parser.option_groups:
        for part in format_option_group(opt_parser, option_group.title, option_group.option_list):
            yield part


def format_option_group(opt_parser, name, options):
    yield '.SH "%s"' % name.upper()
    for option in options:
        for part in format_option(opt_parser, option):
            yield part


def format_option(opt_parser, option):
    yield '.TP'
    yield '.B "%s"' % opt_parser.formatter.format_option_strings(option)
    if option.help:
        yield option.help


man_preamble = """\
.\\\"Man page for Pybtex (%(cmd)s)
.\\\"
.\\\" Generation time: %(timestamp)s
.\\\"
"""


man_head = """\
.TH %(cmd)s 1 "%(datestamp)s" "%(version)s" "Pybtex"

.SH "NAME"
%(cmd)s - %(description)s
"""

def generate_manpage(man_dir, main_obj):
    man_filename = os.path.join(man_dir, '%s.1' % main_obj.prog)
    with open(man_filename, 'w') as man_file:
        write_manpage(man_file, main_obj)


def generate_manpages(doc_dir):
    man_dir = os.path.join(doc_dir, 'man1')
    from pybtex.__main__ import main as pybtex
    from pybtex.database.convert.__main__ import main as pybtex_convert
    generate_manpage(man_dir, pybtex)
    generate_manpage(man_dir, pybtex_convert)
