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


"""Unicode-aware IO routines."""


import locale
import codecs


def get_default_encoding():
    try:
        locale_encoding = locale.getpreferredencoding()
    except locale.Error:
        locale_encoding = None
    return locale_encoding or 'UTF-8'

    
def open(filename, mode='rb', encoding=None):
    if encoding is None:
        encoding = get_default_encoding()
    return codecs.open(filename, mode, encoding=encoding)


def reader(stream, encoding=None):
    if encoding is None:
        encoding = get_default_encoding()
    return codecs.getreader(encoding)(stream)


def writer(stream, encoding=None):
    if encoding is None:
        encoding = get_default_encoding()
    return codecs.getwriter(encoding)(stream)
