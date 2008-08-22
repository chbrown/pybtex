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

from pybtex.backends import BackendBase

file_extension = 'bbl'

class Writer(BackendBase):
    symbols = {
        'ndash': '--',
        'newblock': '\n\\newblock ',
        'nbsp': '~'
    }
    
    def format_tag(self, tag_name, text):
        return r'\%s{%s}' % (tag_name, text)
    
    def write_prologue(self, maxlen):
        self.output('\\begin{thebibliography}{%s}' % ('8' * maxlen))

    def write_epilogue(self):
        self.output('\n\n\\end{thebibliography}\n')

    def write_entry(self, key, label, text):
        self.output('\n\n\\bibitem[%s]{%s}\n' % (label, key))
        self.output(text)
