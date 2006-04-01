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

import locale
import codecs
from pybtex.core import FormattedEntry
from pybtex.richtext import Symbol, Phrase
#from pybtex.formatters.backends import latex

class FormatterBase:
    sep = Symbol('newblock')
    def default_phrase(self, *args, **kwargs):
        kwargs['sep'] = self.sep
        kwargs['add_period'] = True
        kwargs['add_periods'] = True
        return Phrase(*args, **kwargs)
    def format_entries(self, entries):
        l = []
        for entry in entries:
            f = getattr(self, "format_" + entry.type.lower())
            text = f(entry).rich_text()
            l.append(FormattedEntry(entry.key, text, entry.label))
        return l
