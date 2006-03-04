import re
import utils

is_terminated = re.compile(r'.*[.?!][{}\s]*$')
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

def add_period(s):
    if is_terminated.match(s.split()[-1]) is None:
        return s + "."
    else:
        return s

def dashify(s):
    return ndash.join(dash_re.split(s))
