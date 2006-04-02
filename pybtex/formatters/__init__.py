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
import labels
import names
import styles
import backends
import backends.latex

class FindPluginError(Exception):
    pass
def find_plugin(type, name):
    def import_(s):
        m = __import__(type, globals(), locals(), [s])
        try:
            return getattr(m, s)
        except AttributeError:
            return None

    f = import_(name)
    if f is None:
        raise FindPluginError('plugin %s not found in %s' % (name, type))
    return f
