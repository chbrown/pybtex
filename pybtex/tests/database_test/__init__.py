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
        loaded_data = parser.parse_stream(stream)
        self.assertEqual(loaded_data, self.reference_data)

    def test_bibtex_inpub(self):
        self._test_input('bibtex')

    def test_bibyaml_inpub(self):
        self._test_input('bibyaml')

    def test_bibtexml_inpub(self):
        # BibTeXML does not support TeX preambles AFAIK
        self.reference_data._preamble = []
        self._test_input('bibtexml')
