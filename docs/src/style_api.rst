=======================
The Style API of Pybtex
=======================

Well, to tell the truth, the style API is still undergoing heavy development
and is far from being finished yet.

Here is what it looks like.

Template language
=================

BibTeX users probably know that it has a simple stack oriented language
for defining bibliography styles. That is what is placed inside of ``.bst`` files.
For a Pythonic bibliography processor it is natural to use Python for writing styles.
Pybtex style file is just a Python module containing several functions with names
like ``format_article``, ``format_book``, etc. Every function takes a bibliography
entry as an argument and returns a formatted bibliography entry:

.. sourcecode:: python

    def format_article(entry):
        return 'Article %s' % entry.fields['title']

To make things easier we designed a simple template language:

.. sourcecode:: python

    from pybtex.template import field, join, optional

    def format_article(entry):
        template = join (' ') [
            'Article',
            field('title'),
            'by',
            field('author'),
            optional [', ', field('pages')],
            '.'
        ]
        return template.format(entry)


Rich text
=========

Pybtex was designed to produce output in multiplt formats. It means that
bibliograhy formatting functions can't just return things like
``\emph{editor}`` or ``<i>journal</i>``. We have a simple language for
producing formatted text:

.. sourcecode:: pycon

    >>> from pybtex.richtext import Text, Tag
    >>> from pybtex.backends import latex
    >>> renderer = latex.Writer()
    >>> text = Text('This is an example of a ', Tag('emph', 'rich'), ' text.')
    >>> print text.render(renderer)
    This is an example of a \emph{rich} text.


Is that all?
============

More documentation will be written when our style API
gets some form. Use the source for now.
