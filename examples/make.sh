#!/bin/sh

export PYTHONPATH=..
latex xampl
../scripts/pybtex xampl
latex xampl
latex xampl

echo
echo "Examine foo.dvi to see what you have just got."
