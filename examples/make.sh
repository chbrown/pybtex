#!/bin/sh

export PYTHONPATH=..
latex foo
../scripts/pybtex foo
latex foo
latex foo

echo
echo "Examine foo.dvi to see what you have just got."
