from pybtex.database import BibliographyData
from pybtex.core import Entry
from pybtex.database.input.bibtex import Parser
from cStringIO import StringIO

test_data = [
    (
        '''
        ''',
        BibliographyData(),
    ),
    (
        '''@ARTICLE{
                test,
                title={Polluted
                    with {DDT}.
            },
        }''',
        BibliographyData({u'test': Entry('article', {u'title': 'Polluted with {DDT}.'})}),
    ),
    (
        '''@ARTICLE{
                test,
                title="Nested braces  and {"quotes"}",
        }''',
        BibliographyData({u'test': Entry('article', {u'title': 'Nested braces and {"quotes"}'})}),
    ),
]


def _test(bibtex_input, correct_result):
    parser = Parser(encoding='UTF-8')
    parser.parse_stream(StringIO(bibtex_input))
    result = parser.data
    assert result == correct_result

def test_bibtex_parser():
    for bibtex_input, correct_result in test_data:
        _test(bibtex_input, correct_result)
