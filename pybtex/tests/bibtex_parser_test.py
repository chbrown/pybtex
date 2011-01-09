from pybtex.database import BibliographyData
from pybtex.core import Entry, Person
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
    (
        """
            @article{Me2010, author="Brett, Matthew", title="An article
            @article{something, author={Name, Another}, title={not really an article}}
            "}
            @article{Me2009,author={Nom de Plume, My}, title="A short story"}
        """,
        BibliographyData(
            entries={
                u'Me2010': Entry(u'article',
                    fields={
                        u'title': u'An article @article{something, author={Name, Another}, title={not really an article}}'
                    },
                    persons={u'author': [Person(u'Brett, Matthew')]}
                ),
                u'Me2009': Entry(u'article',
                    fields={u'title': u'A short story'},
                    persons={u'author': [Person(u'Nom de Plume, My')]}
                )
            }
        ),
    ),
    (
        """
            Both the articles register despite the comment block
            @Comment{
            @article{Me2010, title="An article"}
            @article{Me2009, title="A short story"}
            }
            These all work OK without errors
            @Comment{and more stuff}

            Last article to show we can get here
            @article{Me2011, }
        """,
        BibliographyData({
            'Me2011': Entry('article'),
            'Me2010': Entry('article', fields={'title': 'An article'}),
            'Me2009': Entry('article', fields={'title': 'A short story'}),
        }),
    ),
    (
        # FIXME: check warnings
        """
            The @ here parses fine in both cases
            @article{Me2010,
                title={An @tey article}}
            @article{Me2009, title="A @tey short story"}
        """,
        BibliographyData({
            'Me2010': Entry('article', {'title': 'An @tey article'}),
            'Me2009': Entry('article', {'title': 'A @tey short story'}),
        }),
    ),
]


def _test(bibtex_input, correct_result):
    parser = Parser(encoding='UTF-8')
    parser.parse_stream(StringIO(bibtex_input))
    result = parser.data
    assert result == correct_result


def test_bibtex_parser():
    for bibtex_input, correct_result in test_data:
        yield _test, bibtex_input, correct_result
