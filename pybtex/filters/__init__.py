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

class FindFilterError(Exception):
    pass


def find_filter(type, name = None):
    def import_(s):
        m = __import__(type, globals(), locals(), [s])
        try:
            return getattr(m, s)
        except AttributeError:
            return None

    if name is None:
        name = import_('default')
    f = import_(name)
    if f is None:
        try:
            newname = import_('filetypes')[name]
        except KeyError:
            newname = name
        f= import_(newname)
        if f is None:
            raise FindFilterError('input filter for %s not found' % name)
    return f.Filter()
