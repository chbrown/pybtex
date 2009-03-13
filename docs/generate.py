#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Generate Project Documentation
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Generates a bunch of html files containing the documentation.

    :copyright: 2006-2007 by Armin Ronacher, Georg Brandl, Ero-sennin
    :license: BSD
"""
import os
import sys
import re
import shutil
import inspect
from datetime import datetime
from cgi import escape
from glob import glob

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.core import publish_parts
from docutils.writers import html4css1

from jinja import Environment, FileSystemLoader
from jinja.filters import stringfilter

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from bzrlib import workingtree
from bzrlib.osutils import format_date

from mystyle import MyHiglightStyle

e = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))

PYGMENTS_FORMATTER = HtmlFormatter(style=MyHiglightStyle, cssclass='sourcecode')

#CHANGELOG = file(os.path.join(os.path.dirname(__file__), os.pardir, 'CHANGES'))\
#            .read().decode('utf-8')

DATE_FORMAT = '%d %B %y (%a)'

FULL_TEMPLATE = e.get_template('template.html')


def get_bzr_timestamp(filename):
    tree = workingtree.WorkingTree.open_containing(filename)[0]
    tree.lock_read()
    rel_path = tree.relpath(os.path.abspath(filename))
    file_id = tree.inventory.path2id(rel_path)
    last_revision = get_last_bzr_revision(tree.branch, file_id)
    tree.unlock()
    return last_revision.timestamp, last_revision.timezone
    

def get_last_bzr_revision(branch, file_id):
    history = branch.repository.iter_reverse_revision_history(branch.last_revision())
    last_revision_id = branch.last_revision()
    current_inventory = branch.repository.get_revision_inventory(last_revision_id)
    current_sha1 = current_inventory[file_id].text_sha1
    for revision_id in history:
        inv = branch.repository.get_revision_inventory(revision_id)
        if not file_id in inv or inv[file_id].text_sha1 != current_sha1:
            return branch.repository.get_revision(last_revision_id)
        last_revision_id = revision_id


def pygments_directive(name, arguments, options, content, lineno,
                      content_offset, block_text, state, state_machine):
    try:
        lexer = get_lexer_by_name(arguments[0])
    except ValueError:
        # no lexer found
        lexer = get_lexer_by_name('text')
    parsed = highlight(u'\n'.join(content), lexer, PYGMENTS_FORMATTER)
    return [nodes.raw('', parsed, format="html")]
pygments_directive.arguments = (1, 0, 1)
pygments_directive.content = 1
directives.register_directive('sourcecode', pygments_directive)


@stringfilter
def mark_tail(phrase, keyword, pattern = '%s<span class="tail"> %s</span>'):
    """Finds and highlights a 'tail' in the sentense.

    A tail consists of several lowercase words and a keyword.

    >>> print mark_tail('Pybtex', 'The Manual of Pybtex')
    The Manual<span class="tail"> of Pybtex</span>

    Look at the generated documentation for further explanation.
    """

    words = phrase.split()
    if words[-1] == keyword:
        pos = -[not word.islower() for word in reversed(words[:-1])].index(True) - 1
        return pattern % (' '.join(words[:pos]), ' '.join(words[pos:]))
    else:
        return phrase

e.filters['mark_tail'] = mark_tail

def create_translator(link_style):
    class Translator(html4css1.HTMLTranslator):
        def visit_reference(self, node):
            refuri = node.get('refuri')
            if refuri is not None and '/' not in refuri and refuri.endswith('.txt'):
                node['refuri'] = link_style(refuri[:-4])
            html4css1.HTMLTranslator.visit_reference(self, node)
    return Translator


class DocumentationWriter(html4css1.Writer):

    def __init__(self, link_style):
        html4css1.Writer.__init__(self)
        self.translator_class = create_translator(link_style)

    def translate(self):
        html4css1.Writer.translate(self)
        # generate table of contents
        contents = self.build_contents(self.document)
        contents_doc = self.document.copy()
        contents_doc.children = contents
        contents_visitor = self.translator_class(contents_doc)
        contents_doc.walkabout(contents_visitor)
        self.parts['toc'] = self._generated_toc

    def build_contents(self, node, level=0):
        sections = []
        i = len(node) - 1
        while i >= 0 and isinstance(node[i], nodes.section):
            sections.append(node[i])
            i -= 1
        sections.reverse()
        toc = []
        for section in sections:
            try:
                reference = nodes.reference('', '', refid=section['ids'][0], *section[0])
            except IndexError:
                continue
            ref_id = reference['refid']
            text = escape(reference.astext().encode('utf-8'))
            toc.append((ref_id, text))

        self._generated_toc = [('#%s' % href, caption) for href, caption in toc]
        # no further processing
        return []


def generate_documentation(data, link_style):
    writer = DocumentationWriter(link_style)
#    data = data.replace('[[list_of_filters]]', LIST_OF_FILTERS)\
#               .replace('[[list_of_tests]]', LIST_OF_TESTS)\
#               .replace('[[list_of_loaders]]', LIST_OF_LOADERS)\
#               .replace('[[environment_doc]]', ENVIRONMENT_DOC)\
#               .replace('[[changelog]]', CHANGELOG)
    parts = publish_parts(
        data,
        writer=writer,
        settings_overrides={
            'initial_header_level': 2,
            'field_name_limit': 50,
        }
    )
    return {
        'title':        parts['title'].encode('utf-8'),
        'body':         parts['body'].encode('utf-8'),
        'toc':          parts['toc']
    }


def handle_file(filename, fp, dst, mode):
    title = os.path.splitext(os.path.basename(filename))[0]
    content = fp.read()
    parts = generate_documentation(content, (lambda x: './%s.html' % x))
    mtime, timezone = get_bzr_timestamp(filename)
    c = dict(parts)
    c['modification_date'] = format_date(mtime, timezone, 'utc', date_fmt=DATE_FORMAT, show_offset=False)
    c['file_id'] = title
    c['mode'] = mode
    tmpl = FULL_TEMPLATE
    result = file(os.path.join(dst, title + '.html'), 'w')
    result.write(tmpl.render(c).encode('utf-8'))
    result.close()


def run(dst, mode, sources=(), handle_file=handle_file):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
    if not sources:
        sources = glob(os.path.join(path, '*.rst'))
    
    try:
        shutil.rmtree(dst)
    except OSError:
        pass
    os.mkdir(dst)
    for filename in glob(os.path.join(path, '*.css')):
        shutil.copy(filename, dst)

    pygments_css = PYGMENTS_FORMATTER.get_style_defs('.sourcecode')
    file(os.path.join(dst, 'pygments.css'), 'w').write(pygments_css)

    for fn in sources:
        if not os.path.isfile(fn):
            continue
        print 'Processing %s' % fn
        f = open(fn)
        try:
            handle_file(fn, f, dst, mode)
        finally:
            f.close()


def main(mode, dst=None, *sources):
    if dst is None:
        dst = os.path.join(os.path.dirname(__file__), 'html')
    run(os.path.realpath(dst), mode, sources)
    if mode == 'site':
        os.system('rsync -rv --delete --exclude hg/ %s ero-sennin,pybtex@web.sourceforge.net:/home/groups/p/py/pybtex/htdocs'
            % os.path.join(dst, ''))


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        args = ['local']
    main(*args)
