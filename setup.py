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
# along with pybtex; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

import sys
import os
from glob import glob1
from setuptools import setup, find_packages
from distutils.command.sdist import sdist
from distutils.dep_util import newer

progname = 'pybtex'
from pybtex.__version__ import version

class Sdist(sdist):
    def run(self):
        from pybtex.database.convert import convert
        bibtex_yaml = os.path.join('examples', 'foo.yaml')
        bibtexml = os.path.join('examples', 'foo.bibtexml')
        bibtex = os.path.join('examples', 'foo.bib')
        if not os.path.exists(bibtex) or newer(bibtex_yaml, bibtex):
            convert(bibtex_yaml, bibtex)
        if not os.path.exists(bibtexml) or newer(bibtex_yaml, bibtexml):
            convert(bibtex_yaml, bibtexml)

        from docs import generate
        generate.main('local')

        sdist.run(self)

README = open(os.path.join(os.path.dirname(__file__), 'README')).read()

setup(name=progname,
    version=version,
    description='A BibTeX-compatible bibliography processor in Python',
    long_description=README,
    author='Andrey Golovizin',
    author_email='golovizin@gmail.com',
    url='http://pybtex.sourceforge.net/',
    license='GPL-2',
    platforms=['platform-independent'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Text Editors :: Text Processing',
        'Topic :: Text Processing :: Markup :: LaTeX',
        'Topic :: Text Processing :: Markup :: XML'
    ],
    install_requires = [
        'pyparsing>=1.4.5',
        'PyYAML>=3.01'
    ],
    packages=find_packages(exclude=['docs']),
    scripts=[os.path.join('scripts', progname), os.path.join('scripts', progname + "-convert")],
    include_package_data=True,
    cmdclass={'sdist' : Sdist},
    zip_safe=True,
    )
