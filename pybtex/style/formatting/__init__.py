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

import locale
import codecs
from pybtex.core import FormattedEntry
from pybtex.richtext import Text

def default_phrase(*args, **kwargs):
    kwargs['sep'] = Text(Symbol('newblock'), ' ')
    kwargs['add_period'] = True
    kwargs['add_periods'] = True
    return Phrase(*args, **kwargs)

class FormatterBase:
    def format_entries(self, entries):
        l = []
        for entry in entries:
            f = getattr(self, "format_" + entry.type)
            text = f(entry)
            l.append(FormattedEntry(entry.key, text, entry.label))
        return l
