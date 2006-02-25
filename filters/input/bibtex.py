#!/bin/env python
"""BibTeX parsing and pretty-printing"""

#import psyco
#psyco.full()

import codecs, locale
from pyparsing import *
from core import Entry

class BibData:
    def __init__(self):
        self.records = {}
        self.strings = {}

    def addRecord(self, s, loc, toks):
        for i in toks:
            fields = {}
            for field in i[2]:
                fields[field[0]] = field[1]
            #fields['TYPE'] = i[0]
            self.records[i[1]] = Entry(i[0], fields)

    def addString(self, s, loc, toks):
        for i in toks:
            s = i[1][0] % tuple([self.strings[arg] for arg in i[1][1]])
            self.strings[i[0]] = s

class Filter:
    def __init__(self):
        self.setEncoding(locale.getpreferredencoding())
        self.data = BibData()

        lparenth = Literal('(').suppress()
        rparenth = Literal(')').suppress()
        lbrace = Literal('{').suppress()
        rbrace = Literal('}').suppress()
        def bibtexGroup(s):
            return (lparenth + s + rparenth) | (lbrace + s + rbrace)

        equal = Literal('=').suppress()
        at = Literal('@').suppress()
        comma = Literal(',').suppress()
        quotedString = Combine( '"' + ZeroOrMore( CharsNotIn('\"\n\r') ) + '"' )
        bracedString = Forward()
        bracedString << '{' + ZeroOrMore(CharsNotIn('{}\n\r') | bracedString) + '}'
        bracedString.setParseAction(self.processBracedString)
        bibTeXString = quotedString | bracedString
        bibTeXString.setParseAction(self.decode)

        name = Word(alphanums + '!$&*+-./:;<>?[]^_`|').setParseAction(upcaseTokens)
        value = Group(delimitedList(bibTeXString | Word(alphanums).setParseAction(upcaseTokens) | Word(nums), delim='#'))

        #fields
        field = Group(name + equal + value)
        field.setParseAction(self.processField)
        fields = Dict(delimitedList(field))

        #String
        string_body = bibtexGroup(fields)#Word(alphanums).setParseAction(upcaseTokens) + equal + value))
        string = at + CaselessLiteral('STRING').suppress() + string_body
        string.setParseAction(self.data.addString)

        #Meta
        meta_body = bibtexGroup(fields)#Group(bibtexGroup(Word(alphanums).setParseAction(upcaseTokens) + equal + field_value))
        meta_body.setParseAction(self.processMeta)
        meta = at + CaselessLiteral('META') + meta_body

        #Record
        record_header = at + Word(alphas).setParseAction(upcaseTokens)
        record_name = Word(printables.replace(',', ''))
        record_body = bibtexGroup(record_name + comma + Group(fields))
        #group(record_name + comma + fields)
        #lbrace + record_name + comma + fields + rbrace
        record = Group(record_header + record_body)
        record.setParseAction(self.data.addRecord)


        #Comment
        comment_header = Word(alphas) | (at + CaselessLiteral('COMMENT'))
        comment = Suppress(comment_header + lbrace + ZeroOrMore(CharsNotIn('}')) + rbrace)

        #Raw text
        raw_text = CharsNotIn('@').suppress()

        self.BibTeX_BNF = ZeroOrMore(meta | comment | raw_text | Suppress(string) | Suppress(record)) + StringEnd()

    def setEncoding(self, e):
        self._decode = codecs.getdecoder(e)

    def decode(self, s, loc, toks):
        return map(lambda x:self._decode(x)[0], toks)

    def processBracedString(self, s, loc, toks):
        return "".join(toks)

    def processMeta(self, s, loc, toks):
        for i in toks:
            if i[0] == 'ENCODING':
                self.setEncoding(i[1][0])

    def processField(self, s, loc, toks):
        result = []
        for token in toks:
            strings = []
            args = []
            for s in token[1]:
                s = s.replace('%', '%%')
                if (s.startswith('"') and s.endswith('"')) or \
                   (s.startswith('{') and s.endswith('}')):
                    strings.append(s[1:-1])
                elif s.isdigit():
                    strings.append(str(s))
                else:
                    strings.append('%s')
                    args.append(s)
            result.append((token[0], ("".join(strings), args)))
        return result


    def parse_file(self, filename):
        """parse BibTeX file and return a tree"""
        f = open(filename)
        s = f.read()
        f.close()
        try:
            self.BibTeX_BNF.parseString(s)
            #print self.data.records
            return self.data
        except ParseException, e:
            print "%s: syntax error:" % filename
            print e
            sys.exit(1)
        except UnicodeDecodeError, e:
            print "%s: no encoding specified, using locale default" % filename
            print e
            sys.exit(1)

    def print_tree(self, tree):
        """prettyprint a tree returned from parseFile"""
        print 'Total records:', len(tree)
        for record in tree:
            print '%s:' % record[0]
            if record[0] == "STRING":
                print '\t%s = %s' % (record[1][0], ' # '.join(record[1][1]))
            else:
                print '\t%s' % record[1]
                for field in record[2]:
                    print '\t%s = %s' % (field[0], ' # '.join(field[1]))
            print
