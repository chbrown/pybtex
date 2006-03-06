import re
from pybtex import utils

dash_re = re.compile(r'-')
ndash = '--'

def emph(s):
    return r"\emph{%s}" % s

def it(s):
    return r"\textit{%s}" %s

def bf(s):
    return r"\textbf{%s}"

def sc(s):
    return r"\textsc{%s}"

def dashify(s):
    return ndash.join(dash_re.split(s))
