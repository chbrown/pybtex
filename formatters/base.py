import locale
import codecs
import utils
import latex

class Formatter:
    def __init__(self, entries, encoding = locale.getpreferredencoding()):
        self.separator = '\n\\newblock\n'
        self.word_separator = ', '
        self.entries = entries
        self.encoding = encoding
        self.strings = {}
    def newblock(self):
        self.output('\n\\newblock\n')
    
    def newline(self):
        self.output('\n')

    def join_with_separators(self, l, default_separator):
        first = True
        try:
            result = [l[0]]
        except IndexError:
            result = []
        for element in l[1:]:
            if isinstance(element, list):
                if element[0]:
                    result.append(element[1] + element[0])
            elif element:
                result.append(default_separator + element)
        return "".join(result)   
            
        
    def format_sentense(self, sentense):
        if isinstance(sentense, list):
            text = self.join_with_separators(sentense, self.word_separator)
        else:
            text = sentense 

        return text

            
    def write_item(self, entry):
        self.output('\n\n\\bibitem{%s}\n' % entry.key)
        f = getattr(self, "format_" + entry.type.lower())
        sentenses = []
        for sentense in f(entry):
            sentenses.append(latex.add_period(self.format_sentense(sentense)))
        text = self.join_with_separators(sentenses, self.separator)
        self.output(text)

    def output_bibliography(self, filename):
        self.f = codecs.open(filename, "w", self.encoding)
        self.output = self.f.write
        maxlen = max([len(e.label) for e in self.entries])
        #FIXME: determine label width proprely
        self.output('\\begin{thebibliography}{%s}' % ('8' * maxlen))
        index = 1
        for entry in self.entries:
            self.write_item(entry)
            index += 1
        self.output('\n\\end{thebibliography}\n')
        self.f.close()
        del self.f
