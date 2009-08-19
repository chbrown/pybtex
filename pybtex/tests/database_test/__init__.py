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

from unittest import TestCase
from pkg_resources import resource_stream
import yaml
from StringIO import StringIO

from pybtex.plugin import find_plugin

class DatabaseIOTest(TestCase):
    def setUp(self):
        reference_data_file = resource_stream('pybtex', 'tests/database_test/reference_data.yaml')
        self.reference_data = yaml.load(reference_data_file)

    def _test_input(self, plugin):
        parser = find_plugin('pybtex.database.input', plugin).Parser(encoding='UTF-8')
        writer = find_plugin('pybtex.database.output', plugin).Writer(encoding='UTF-8')
        stream = StringIO()
        writer.write_stream(self.reference_data, stream)
        stream.seek(0)
        parser.parse_stream(stream)
        loaded_data = parser.data
        self.assertEqual(loaded_data, self.reference_data)

    def test_bibtex_inpub(self):
        self._test_input('bibtex')

    def test_bibyaml_inpub(self):
        self._test_input('bibyaml')

    def test_bibtexml_inpub(self):
        # BibTeXML does not support TeX preambles AFAIK
        self.reference_data._preamble = []
        self._test_input('bibtexml')
