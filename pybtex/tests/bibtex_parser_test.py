from pybtex.database import BibliographyData
from pybtex.core import Entry, Person
from pybtex.database.input.bibtex import Parser
from cStringIO import StringIO

from unittest import TestCase


class ParserTest(object):
    input = None
    correct_result = None

    def test_parser(self):
        parser = Parser(encoding='UTF-8')
        parser.parse_stream(StringIO(self.input))
        result = parser.data
        correct_result = self.correct_result
        assert result == correct_result
    

class EmptyDataTest(ParserTest, TestCase):
    input = ''
    correct_result = BibliographyData()


class BracesTest(ParserTest, TestCase):
    input = """@ARTICLE{
                test,
                title={Polluted
                    with {DDT}.
            },
    }"""
    correct_result = BibliographyData({u'test': Entry('article', {u'title': 'Polluted with {DDT}.'})})


class BracesAndQuotesTest(ParserTest, TestCase):
    input = '''@ARTICLE{
                test,
                title="Nested braces  and {"quotes"}",
        }'''
    correct_result =BibliographyData({u'test': Entry('article', {u'title': 'Nested braces and {"quotes"}'})})


class EntryInStringTest(ParserTest, TestCase):
    input = """
        @article{Me2010, author="Brett, Matthew", title="An article
        @article{something, author={Name, Another}, title={not really an article}}
        "}
        @article{Me2009,author={Nom de Plume, My}, title="A short story"}
    """
    correct_result = BibliographyData(
        entries={
            u'me2010': Entry(u'article',
                fields={
                    u'title': u'An article @article{something, author={Name, Another}, title={not really an article}}'
                },
                persons={u'author': [Person(u'Brett, Matthew')]}
            ),
            u'me2009': Entry(u'article',
                fields={u'title': u'A short story'},
                persons={u'author': [Person(u'Nom de Plume, My')]}
            )
        }
    )


class EntryInCommentTest(ParserTest, TestCase):
    input = """
        Both the articles register despite the comment block
        @Comment{
        @article{Me2010, title="An article"}
        @article{Me2009, title="A short story"}
        }
        These all work OK without errors
        @Comment{and more stuff}

        Last article to show we can get here
        @article{Me2011, }
    """
    correct_result = BibliographyData({
        'me2011': Entry('article'),
        'me2010': Entry('article', fields={'title': 'An article'}),
        'me2009': Entry('article', fields={'title': 'A short story'}),
    })


class AtTest(ParserTest, TestCase):
    # FIXME: check warnings
    input = """
        The @ here parses fine in both cases
        @article{Me2010,
            title={An @tey article}}
        @article{Me2009, title="A @tey short story"}
    """
    correct_result = BibliographyData({
        'me2010': Entry('article', {'title': 'An @tey article'}),
        'me2009': Entry('article', {'title': 'A @tey short story'}),
    })

class EntryTypesTest(ParserTest, TestCase):
    input = """
        Testing what are allowed for entry types

        These are OK
        @somename{an_id,}
        @t2{another_id,}
        @t@{again_id,}
        @t+{aa1_id,}
        @_t{aa2_id,}

        These ones not
        @2thou{further_id,}
        @some name{id3,}
        @some#{id4,}
        @some%{id4,}
    """
    correct_result = BibliographyData({
        'an_id': Entry('somename'),
        'another_id': Entry('t2'),
        'again_id': Entry('t@'),
        'aa1_id': Entry('t+'),
        'aa2_id': Entry('_t'),
    })


class FieldNamesTest(ParserTest, TestCase):
    input = """
        Check for characters allowed in field names
        Here the cite key is fine, but the field name is not allowed:
        ``You are missing a field name``
        @article{2010, 0author="Me"}

        Underscores allowed (no error)
        @article{2011, _author="Me"}

        Not so for spaces obviously (``expecting an '='``)
        @article{2012, author name = "Myself"}

        Or hashes (``missing a field name``)
        @article{2013, #name = "Myself"}

        But field names can start with +-.
        @article{2014, .name = "Myself"}
        @article{2015, +name = "Myself"}
        @article{2016, -name = "Myself"}
        @article{2017, @name = "Myself"}
    """
    correct_result = BibliographyData({
        '2011': Entry('article', {'_author': 'Me'}),
        '2014': Entry('article', {'.name': 'Myself'}),
        '2015': Entry('article', {'+name': 'Myself'}),
        '2016': Entry('article', {'-name': 'Myself'}),
        '2017': Entry('article', {'@name': 'Myself'}),
    })


class InlineCommentTest(ParserTest, TestCase):
    input = """
        "some text" causes an error like this
        ``You're missing a field name---line 6 of file bibs/inline_comment.bib``
        for all 3 of the % some text occurences below; in each case the parser keeps
        what it has up till that point and skips, so that it correctly gets the last
        entry.
        @article{Me2010,}
        @article{Me2011,
            author="Brett-like, Matthew",
        % some text
            title="Another article"}
        @article{Me2012, % some text
            author="Real Brett"}
        This one correctly read
        @article{Me2013,}
    """
    correct_result = BibliographyData({
        'me2010': Entry('article'),
        'me2013': Entry('article'),
    })
