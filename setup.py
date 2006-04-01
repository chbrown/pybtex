#!/usr/bin/env python

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

import sys
import os
from glob import glob1
from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.dep_util import newer
from distutils.log import info

progname = 'pybtex'
from pybtex import __version__ as version

def list_modules():
    modules = []
    def add(art, dirname, filenames):
        dirs = dirname.split(os.path.sep)
        if '.svn' in dirs:
            return
        module = '.'.join(dirs)
        modules.append(module)
    os.path.walk(progname, add, None)
    return modules

class InstallData(install_data):
    def run(self):
        # we don't usually have the tools to compile po files in win32
        if sys.platform != 'win32':
            self.data_files.extend(self._compile_po_files())

        install_data.run(self)

    def _compile_po_files(self):
        data_files = []
        for po in glob1('po', '*.po'):
            lang = os.path.splitext(po)[0]
            po = os.path.join('po', po)
            mo = os.path.join('locale', lang,
                              'LC_MESSAGES', '%s.mo' % progname)

            if not os.path.exists(mo) or newer(po, mo):
                directory = os.path.dirname(mo)
                if not os.path.exists(directory):
                    info("creating %s" % directory)
                    os.makedirs(directory)
                cmd = 'msgfmt -o %s %s' % (mo, po)
                info('compiling %s -> %s' % (po, mo))
                if os.system(cmd) != 0:
                    raise SystemExit("Error while running msgfmt")
            dest = os.path.dirname(os.path.join('share', mo))
            data_files.append((dest, [mo]))

        return data_files

data_files=[]
setup(name=progname,
    version=version,
    description='Bibtex-compatible bibliography processor in Python',
    long_description='''Pybtex is just another bibliography processor.
As the name suggests, pybtex is designed much after BibTeX and written
in Python. Please note that the correct spelling is just pybtex, without
that TeX-like camel-casing, which we considered too boring to type.''',
    author='Andrey Golovizin',
    author_email='golovizin@gorodok.net',
    url='http://pybtex.sourceforge.net/',
    license='GPL-2',
    platforms=['platform-independent'],
    classifiers=[
        'License :: OSI-Approved Open Source :: GNU General Public License (GPL)',
        'Intended Audience :: by End-User Class :: End Users/Desktop',
        'Development Status :: 3 - Alpha',
        'Topic :: Formats and Protocols :: Data Formats :: TeX/LaTeX',
        'Topic :: Formats and Protocols :: Data Formats :: XML',
        'Topic :: Scientific/Engineering',
        'Topic :: Text Editors :: Text Processing',
        'Programming Language :: Python',
        'Operating System :: Grouping and Descriptive Categories :: OS Independent',
        'User Interface :: Textual :: Command-line'
    ],
    packages=list_modules(),
    scripts=[os.path.join('scripts', progname)],
    data_files=data_files,
    cmdclass={'install_data': InstallData}
    )
