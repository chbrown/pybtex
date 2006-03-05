#!/bin/env python
import sys, re

class AuxData:
    def __init__(self):
        self.style = None
        self.data = None
        self.citations = []
    def new_citation(self, s):
        for c in s.split(','):
            if not c in self.citations:
                self.citations.append(c)
    def new_style(self, s):
        self.style = s
    def new_data(self, s):
        self.data = s

def parse_file(filename):
    command = re.compile(r'\\(citation|bibdata|bibstyle){(.*)}')
    f = open(filename)
    s = f.read()
    f.close()
    b = AuxData()
    actions = {
        "citation" : b.new_citation,
        "bibstyle" : b.new_style,
        "bibdata" : b.new_data
    }
    for i in command.findall(s):
        actions[i[0]](i[1])
    return b
