# Copyright (C) 2010  Andrey Golovizin
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


import errno
import posixpath
from unittest import TestCase

from pybtex import io


class MockFile(object):
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode

    def __repr__(self):
        return "<mock open file '%s', mode '%s'>" % (self.name, self.mode)
    

class MockFilesystem(object):
    def __init__(self, files=(), writable_dirs=(), readonly_dirs=()):
        self.files = set(files)
        self.writable_dirs = set(writable_dirs)
        self.readonly_dirs = set(readonly_dirs)

    def add_file(self, path):
        self.files.add(path)

    def chdir(self, path):
        self.pwd = path

    def locate(self, filename):
        for path in self.files:
            if path.endswith(filename):
                return path

    def open_read(self, path, mode):
        if path in self.files:
            return MockFile(path, mode)
        else:
            raise IOError(errno.ENOENT, 'No such file or directory', path)

    def open_write(self, path, mode):
        dirname = posixpath.dirname(path)
        if dirname in self.writable_dirs:
            return MockFile(path, mode)
        else:
            raise IOError(errno.EACCES, 'Permission denied', path)

    def open(self, path, mode):
        full_path = posixpath.join(self.pwd, path)
        if 'w' in mode:
            return self.open_write(full_path, mode)
        else:
            return self.open_read(full_path, mode)


class IOTest(TestCase):
    def setUp(self):
        self.fs = MockFilesystem(
            files=(
                '/home/test/foo.bib',
                '/home/test/foo.bbl',
                '/usr/share/texmf/bibtex/bst/unsrt.bst',
            ),
            writable_dirs = ('/home/test',),
            readonly_dirs = ('/'),
        )
        self.fs.chdir('/home/test')

    def test_open_existing(self):
        file = io._open_existing(self.fs.open, 'foo.bbl', 'rb', locate=self.fs.locate)
        self.assertEqual(file.name, '/home/test/foo.bbl')
        self.assertEqual(file.mode, 'rb')
        
    def test_open_missing(self):
        self.assertRaises(
            EnvironmentError,
            io._open_existing, self.fs.open, 'nosuchfile.bbl', 'rb',
            locate=self.fs.locate,
        )

    def test_locate(self):
        file = io._open_existing(
            self.fs.open, 'unsrt.bst', 'rb', locate=self.fs.locate
        )
        self.assertEqual(file.name, '/usr/share/texmf/bibtex/bst/unsrt.bst')
        self.assertEqual(file.mode, 'rb')

    def test_create(self):
        file = io._open_or_create(self.fs.open, 'foo.bbl', 'wb', {})
        self.assertEqual(file.name, '/home/test/foo.bbl')
        self.assertEqual(file.mode, 'wb')

    def test_create_in_readonly_dir(self):
        self.fs.chdir('/')
        self.assertRaises(
            EnvironmentError,
            io._open_or_create, self.fs.open, 'foo.bbl', 'wb', {},
        )

    def test_create_in_fallback_dir(self):
        self.fs.chdir('/')
        file = io._open_or_create(
            self.fs.open, 'foo.bbl', 'wb', {'TEXMFOUTPUT': '/home/test'}
        )
        self.assertEqual(file.name, '/home/test/foo.bbl')
        self.assertEqual(file.mode, 'wb')
