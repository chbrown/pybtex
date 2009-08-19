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

Using Pybtex as a bibliography files converter
==============================================

Pybtex has a simple ``pybtex-convert`` utility, which can convert bibliography
files between supported formats.

.. sourcecode:: bash

    $ pybtex-convert foo.bib foo.yaml

The conversion is not always lossless due to limitations of storage formats:

- Native BibTeX format stores personal names as single strings, while BibTexML
  and Pybtex' YAML format store first name, last name, and other name parts
  seprately.

- BibTeXML format does not support LaTeX preambles.

- PyYAML does not preserve the order of keys (this may be fixed some day).

Using Pybtex programmatically
=============================

Using the BibTeX parser
-----------------------

.. sourcecode:: python

    >>> from pybtex.database.input import bibtex
    >>> parser = bibtex.Parser()
    >>> bib_data = parser.parse_file('examples/foo.bib')
    >>> bib_data.entries.keys()
    [u'ruckenstein-diffusion', u'viktorov-metodoj', u'test-inbook', u'test-booklet']
    >>> print bib_data.entries['ruckenstein-diffusion'].fields['title']
    Predicting the Diffusion Coefficient in Supercritical Fluids
