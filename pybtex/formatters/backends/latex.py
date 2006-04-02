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

from pybtex import utils
from pybtex.richtext import Tag
from pybtex.formatters.backends import BackendBase

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
        self.output('\n\\end{thebibliography}\n')

    def write_item(self, entry):
        self.output('\n\n\\bibitem[%s]{%s}\n' % (entry.label, entry.key))
        self.output(entry.text.render(self))
