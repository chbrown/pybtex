import re
import utils

is_terminated = re.compile(r'.*[.?!][{}\s]*$')
def emph(s):
    return r"\emph{%s}" % s

def it(s):
    return r"\textit{%s}" %s

def bf(s):
    return r"\textbf{%s}"

def sc(s):
    return r"\textsc{%s}"

def add_period(s):
    if is_terminated.match(s) is None:
        return s + "."
