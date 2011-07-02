from pybtex.bibtex.interpreter import (
    Integer, String, QuotedVar, Identifier, FunctionLiteral,
)

from pybtex.bibtex.bst import parse_file


test_data = (
    'plain',
    'apacite',
    'jurabib',
)


def check_bst_parser(dataset_name):
    module = __import__('pybtex.tests.bst_parser_test.{0}'.format(dataset_name), globals(), locals(), 'bst')
    correct_result = module.bst
    actual_result = list(parse_file(dataset_name + '.bst'))

    # XXX pyparsing return list-like object which are not equal to plain lists
    assert repr(actual_result) == repr(correct_result)

 
def test_bst_parser():
    for dataset_name in test_data:
        yield check_bst_parser, dataset_name
