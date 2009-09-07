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

import sys
import locale
import codecs

from pybtex.exceptions import PybtexError


def get_default_encoding():
    try:
        locale_encoding = locale.getpreferredencoding()
    except locale.Error:
        locale_encoding = None
    return locale_encoding or 'UTF-8'

    
def get_stream_encoding(stream):
    stream_encoding = getattr(stream, 'encoding', None)
    return stream_encoding or get_default_encoding()


def _open(opener, filename, *args, **kwargs):
    try:
        return opener(filename, *args, **kwargs)
    except EnvironmentError, error:
        raise PybtexError("unable to open_unicode %s. %s" % (filename, error.strerror))


def open_plain(filename, mode='rb'):
    return _open(open, filename, mode)


def open_unicode(filename, mode='rb', encoding=None):
    if encoding is None:
        encoding = get_default_encoding()
    return _open(codecs.open, filename, mode, encoding=encoding)


def reader(stream, encoding=None, errors='strict'):
    if encoding is None:
        encoding = get_stream_encoding(stream)
    return codecs.getreader(encoding)(stream, errors)


def writer(stream, encoding=None, errors='strict'):
    if encoding is None:
        encoding = get_stream_encoding(stream)
    return codecs.getwriter(encoding)(stream, errors)


stdout = writer(sys.stdout, errors='backslashreplace')
stderr = writer(sys.stderr, errors='backslashreplace')
