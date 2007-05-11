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

    @BOOK{strunk-and-white,
        author = "Strunk, Jr., William and E. B. White",
        title = "The Elements of Style",
        publisher = "Macmillan",
        edition = "Third",
        year = 1979
    }


For detailed description of the BibTeX format please refer to the
`BibTeX documentation <http://www.ctan.org/info?id=bibtex>`_.

BibTeXML
--------

BibTeXML format attempts to combine the simplicity of BibTeX format with the
power of XML. Here is like the above BibTeX bibliography entry wolud look like:

.. sourcecode:: xml

    <bibtex:entry id="strunk-and-white">
    <bibtex:book>
    <bibtex:title>The Elements of Style</bibtex:title>
    <bibtex:publisher>Macmillan<bibtex:publisher>
    <bibtex:edition>Third</bibtex:edition>
    <bibtex:year>1979</bibtex:year>
    <bibtex:author>
            <bibtex:person>
                <bibtex:first>William</bibtex:first>
                <bibtex:lineage>Jr.</bibtex:lineage>
                <bibtex:last>Strunk</bibtex:last>
            </bibtex:person>
            <bibtex:person>
                <bibtex:first>E.</bibtex:first>
                <bibtex:middle>B.</bibtex:first>
                <bibtex:last>White</bibtex:last>
            </bibtex:person>
    </bibtex:author>
    </bibtex:book>
    </bibtex:entry>

See `the official BibTeXML site <http://bibtexml.sourceforge.net>`_ for more details.

YAML
----

We choosed to create our own format to use with Pybtex. It is quite similar to BibTeXML
but based on YAML and therefore much less verbose.

.. sourcecode:: yaml
    strunk-and-white:
        type: book
        author: Strunk, Jr., William and E. B. White
        title: The Elements of Style
        publisher: Macmillan
        edition: Third
        year: 1979
    }

See `<http://yaml.org>`_ for more details.

Output formats
==============

- LaTeX
- plain text
- HTML (work in progress)

Support for other formats can be added easily. If you really need it,
please `file a feature request`_.


Bibliography style formats
==========================

- BibTeX ``.bst`` files
- Pybtex own pythonic `style API <style_api.txt>`_

.. _file a feature request: http://sourceforge.net/tracker/?group_id=151578&atid=781409
