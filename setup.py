#!/usr/bin/env python

# Copyright (C) 2006, 2007, 2008, 2009  Andrey Golovizin
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

        from pybtex.docgen import generate_docs
        generate_docs(os.path.join(ROOT, 'docs'), ('html', 'manpages'))

        sdist.run(self)

ROOT = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(ROOT, 'README')).read()

if sys.version_info >= (3, 0):
    extra = {
        'use_2to3': True,
        'use_2to3_fixers': ['custom_fixers'],
    }
else:
    extra = {}

setup(name=progname,
    version=version,
    description='A BibTeX-compatible bibliography processor in Python',
    long_description=README,
    author='Andrey Golovizin',
    author_email='golovizin@gmail.com',
    url='http://pybtex.sourceforge.net/',
    license='MIT',
    platforms=['platform-independent'],
    classifiers=[
        'Development Status :: 4 - Beta',
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
    **extra
    )
