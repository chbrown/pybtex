=============================
The Friendly Manual of Pybtex
=============================

Using Pybtex instead of BibTeX
==============================

Pybtex is compatible with BibTeX in many ways — just type ``pybtex`` instead of
``bibtex``.

.. sourcecode:: bash

    $ latex foo
    $ pybtex foo
    $ latex foo
    $ latex foo

Using Pybtex with (experimental) pythonic bibliography styles
=============================================================

Pybtex supports bibliography styles written in Python, although this feature
is still in development. If you want to give it a try, first examine the
sources in the ``pybtex/style`` subdirectory, then run.

.. sourcecode:: bash

    $ pybtex -e pybtex foo

As of now the only pythonic style available is
``pybtex/style/formatting/unsrt.py``. It is a partial and very incomplete port
of ``unsrt.bst``.


Using Pybtex programmatically
=============================

Using the BibTeX parser
-----------------------

.. sourcecode:: python

    >>> from pybtex.database.input import bibtex
    >>> parser = bibtex.Parser()
    >>> bib_data = parser.parse_file('foo.bib')
    >>> bib_data.entries.keys()
    ['BOOK1', 'BOOK2']
    >>> bib_data.entries['BOOK1'].fields['title']
    Book Title
