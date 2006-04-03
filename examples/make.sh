#!/bin/sh

export PYTHONPATH=..
latex foo
../scripts/pybtex foo --bibtex-encoding=utf8 --latex-encoding=utf8
latex foo
latex foo

echo
echo "Examine foo.dvi to see what you have just got."
