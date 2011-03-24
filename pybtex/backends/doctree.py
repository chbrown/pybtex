"""Doctree backend for pybtex."""

import docutils.nodes

from pybtex.backends import BaseBackend
import pybtex.richtext

class Backend(BaseBackend):
    name = 'doctree'

    symbols = {
        'ndash': docutils.nodes.inline(u'\u2013', u'\u2013'),
        'newblock': docutils.nodes.inline(u' ', u' '),
        'nbsp': docutils.nodes.inline(u'\u00a0', u'\u00a0')
    }
    tags = {
         'emph': docutils.nodes.emphasis,
    }

    def format_text(self, text):
        return docutils.nodes.inline(text, text)

    def format_tag(self, tag_name, text):
        tag = self.tags[tag_name]
        if isinstance(text, basestring):
            return tag(text, text)
        else:
            # must be a docutils node
            node = tag('', '')
            node.children.append(text)
            return node

    def write_entry(self, key, label, text):
        # This is a very simple implementation, does not include key
        # and label yet.
        node = docutils.nodes.paragraph()
        node.children.append(text)
        return node

    def render_sequence(self, text):
        """Return backend-dependent representation of sequence *text*
        of rendered Text objects.
        """
        if len(text) != 1:
            node = docutils.nodes.inline('', '')
            node.children.extend(text)
            return node
        else:
            return text[0]

    def write_to_doctree(self, formatted_entries, doctree):
        """Append all entries to *doctree*."""
        for entry in formatted_entries:
            doctree.append(
                self.write_entry(
                    entry.key, entry.label, entry.text.render(self)))
