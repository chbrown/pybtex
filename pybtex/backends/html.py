# Copyright (C) 2008, 2009  Andrey Golovizin
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

from xml.sax.saxutils import escape
from pybtex.backends import BackendBase
import pybtex.io

file_extension = 'html'

PROLOGUE = """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head><meta name="generator" content="Pybtex">
<meta http-equiv="Content-Type" content="text/html; charset=%s">
<title>Bibliography</title>
</head>
<body>
<dl>
"""

class Writer(BackendBase):
    symbols = {
        'ndash': '&ndash;',
        'newblock': '\n',
        'nbsp': '&nbsp;'
    }
    tags = {
         'emph': 'em',
    }
    
    def format_text(self, text):
        return escape(text)

    def format_tag(self, tag_name, text):
        tag = self.tags[tag_name]
        return r'<%s>%s</%s>' % (tag, text, tag)
    
    def write_prologue(self, maxlen):
        encoding = self.encoding or pybtex.io.get_default_encoding()
        self.output(PROLOGUE % encoding)

    def write_epilogue(self):
        self.output('</dl></body></html>\n')

    def write_entry(self, key, label, text):
        self.output('<dt>%s</dt>\n' % label)
        self.output('<dd>%s</dd>\n' % text)
