from pybtex import utils
from pybtex.richtext import Tag
from pybtex.formatters.backends import BackendBase
import codecs

class Writer(BackendBase):
    symbols = {
        'ndash': '-',
        'newblock': ''
    }
    
    def format_tag(self, tag_name, text):
        return text
    
    def write_item(self, entry):
    	self.output("[%s] " % entry.label)
        self.output(entry.text.render(self))
	self.output('\n')
