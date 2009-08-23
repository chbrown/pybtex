#!/usr/bin/env python

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

"""Various tools for generating Pybtex documentation."""

from .man import generate_manpages
from .html import generate_html, generate_site

generators = {
    'manpages': generate_manpages,
    'html': generate_html,
    'site': generate_site,
}

def generate_docs(doc_path, doc_types):
    for doc_type in doc_types:
        generate = generators[doc_type]
        print 'Generating', doc_type
        generate(doc_path)
