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
from os import path, environ

from pybtex.exceptions import PybtexError
from pybtex.kpathsea import kpsewhich


def get_default_encoding():
    try:
        locale_encoding = locale.getpreferredencoding()
    except locale.Error:
        locale_encoding = None
    return locale_encoding or 'UTF-8'

    
def get_stream_encoding(stream):
    stream_encoding = getattr(stream, 'encoding', None)
    return stream_encoding or get_default_encoding()


def _open_existing(opener, filename, mode, locate, **kwargs):
    if not path.isfile(filename):
        found = locate(filename)
        if found:
            filename = found
    return opener(filename, mode, **kwargs)


def _open_or_create(opener, filename, mode, environ, **kwargs):
    try:
        return opener(filename, mode, **kwargs)
    except EnvironmentError, error:
        if 'TEXMFOUTPUT' in environ:
            new_filename = path.join(environ['TEXMFOUTPUT'], filename)
            try:
                return opener(new_filename, mode, **kwargs)
            except EnvironmentError:
                pass
        raise error


def _open(opener, filename, mode, **kwargs):
    write_mode = 'w' in mode
    try:
        if write_mode:
            return _open_or_create(opener, filename, mode, environ, **kwargs)
        else:
            return _open_existing(opener, filename, mode, locate=kpsewhich, **kwargs)
    except EnvironmentError, error:
        raise PybtexError("unable to open %s. %s" % (filename, error.strerror))


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
