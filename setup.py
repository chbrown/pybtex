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

progname = 'pybtex'
from pybtex.__version__ import version

class Sdist(sdist):
    def run(self):
        from pybtex.database.convert import convert
        bibtex_yaml = os.path.join('examples', 'foo.yaml')
        bibtex = os.path.join('examples', 'foo.bibtex')
        if not os.path.exists(bibtex) or newer(bibtex_yaml, bibtex):
            convert(bibtex_yaml, 'bibyaml', 'bibtex')

        from docs import generate
        generate.main('local')

        sdist.run(self)

setup(name=progname,
    version=version,
    description='BibTeX-compatible bibliography processor in Python',
    long_description="""Pybtex is a drop-in replacement for BibTeX
written in Python. Please note that the correct spelling is just *Pybtex*, without
that TeX-like camel-casing, which we considered too annoying to type.""",
    author='Andrey Golovizin',
    author_email='golovizin@gmail.com',
    url='http://pybtex.sourceforge.net/',
    download_url='http://sourceforge.net/project/showfiles.php?group_id=151578',
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
    packages=find_packages(),
    setup_requires = [
        'pyparsing>=1.4.5',
        'PyYAML>=3.01'
    ],
    scripts=[os.path.join('scripts', progname), os.path.join('scripts', progname + "-convert")],
    cmdclass={'sdist' : Sdist}
    )
