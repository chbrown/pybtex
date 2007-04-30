======================
The Features of Pybtex
======================

Bibliography formats
====================

BibTeX
------

BibTeX format is very simple and easy to learn. Those who have used BibTeX
should be already familiar with it. The others will probably catch the idea
from the following example:

.. sourcecode:: bibtex

    @comment(sdf)

    @article{
        title = "Functional Programming in Python",
        author = "John Doe",
        journal = "The International Python Jounal", 
        volume = 13,
        pages = "208-224",
        year = 2007
    }

For detailed description of the BibTeX format please refer to the
`BibTeX documentation <http://www.ctan.org/info?id=bibtex>`_.

BibTeXML
--------

BibTeXML format attempts to combine the simplicity of BibTeX format with the
power of XML. Here is what it looks like:

.. sourcecode:: xml

    <bibtex:entry id="ruckenstein-diffusion">
    <bibtex:article>
    <bibtex:language>English</bibtex:language>
    <bibtex:title>Surround</bibtex:title>
    <bibtex:journal>Some Looooooooooooooooooooooooong Journal</bibtex:journal>
    <bibtex:ages>888-895</bibtex:ages>
    <bibtex:volume>36</bibtex:volume>
    <bibtex:year>1997</bibtex:year>
    <bibtex:author>
            <bibtex:person>
            <bibtex:first>Hongquin</bibtex:first>
            <bibtex:last>Liu</bibtex:last>
            </bibtex:person>
            <bibtex:person>
            <bibtex:first>Eli</bibtex:first>
            <bibtex:last>Ruckenstein</bibtex:last>
            </bibtex:person>
    </bibtex:author>
    </bibtex:article>
    </bibtex:entry>

`BibTeXML <http://bibtexml.sourceforge.net>`_

YAML
----

YAML is a data definition language.

.. sourcecode:: yaml

    entries:
        debil: debil

See `<http://yaml.org>`_ for more details.

Output formats
==============

- LaTeX
- plain text
- HTML (in progress)

Support for other formats can be added easily. If you really need it,
please `file a feature request`_.


Bibliography styles
===================

- BibTeX ``.bst`` files
- Pybtex own pythonic `style API <style_api.txt>`_

.. _file a feature request: http://sourceforge.net/tracker/?group_id=151578&atid=781409
