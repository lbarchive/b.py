#!/usr/bin/env python
# Copyright (C) 2013 by Yu-Jie Lin
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from abc import abstractmethod, ABCMeta
from os.path import basename, splitext
import re
import sys

import smartypants
from smartypants import smartyPants


class BaseHandler():
  """The base clase of markup handler"""
  __metaclass__ = ABCMeta

  MERGE_HEADERS = ('kind', 'blog', 'id', 'url')
  HEADER_FMT = '%s: %s'
  PREFIX_HEAD = ''
  PREFIX_END = ''

  RE_SPLIT = re.compile(r'^(?:([^\n]*?!b.*?)\n\n)?(.*)', re.DOTALL | re.MULTILINE)
  RE_HEADER = re.compile(r'(.*?)\s*[=:]\s*(.*)\s*')

  def __init__(self, filename, options=None):

    self.filename = filename
    self.title = ''
    self.options = {}
    self.options.update(options or {})
    if filename:
      with open(filename) as f:
        self.source = f.read()
      header, markup = self.split_header_markup()
      self.title = splitext(basename(filename))[0]
    else:
      header = {}
      markup = ''
    self.header = header
    self.markup = markup
    self.modified = False

  def set_header(self, k, v):
    """Set header

    >>> class Handler(BaseHandler):
    ...   def _generate(self, source=None): return source
    >>> handler = Handler(None)
    >>> print handler.header
    {}
    >>> handler.modified
    False
    >>> handler.set_header('foo', 'bar')
    >>> handler.header
    {'foo': 'bar'}
    >>> handler.modified
    True
    """
    if k in self.header and self.header[k] == v:
      return

    self.header[k] = v
    self.modified = True

  def merge_header(self, header):
    """Merge header

    >>> class Handler(BaseHandler):
    ...   def _generate(self, source=None): return source
    >>> handler = Handler(None)
    >>> handler.merge_header({'id': 12345, 'bogus': 'blah'})
    >>> handler.header
    {'id': 12345}
    >>> handler.modified
    True
    """
    for k, v in header.items():
      if k not in self.MERGE_HEADERS:
        continue
      if k == 'blog':
        v = v['id']
      elif k == 'kind':
        v = v.replace('blogger#', '')
      self.set_header(k, v)

  @abstractmethod
  def _generate(self, markup=None):
    """Generate HTML of markup source"""
    raise NotImplementError

  def generate(self, markup=None):
    """Generate HTML
    
    >>> class Handler(BaseHandler):
    ...   def _generate(self, markup=None): return markup
    >>> handler = Handler(None)
    >>> print handler.generate('foo "bar"')
    foo "bar"
    >>> handler.options['smartypants'] = True
    >>> print handler.generate('foo "bar"')
    foo &#8220;bar&#8221;
    """

    if markup is None:
      markup = self.markup

    html = self._generate(markup)

    if self.options.get('smartypants', False):
      RE = smartypants.tags_to_skip_regex 
      pattern = RE.pattern.replace('|code', '|code|tt')
      pattern = pattern.replace('|script', '|script|style')
      RE = re.compile(pattern, RE.flags)
      smartypants.tags_to_skip_regex = RE
      html = smartyPants(html)

    return html.encode('utf-8')

  def generate_header(self, header=None):
    """Generate header in text for writing back to the file
    
    >>> class Handler(BaseHandler):
    ...   PREFIX_HEAD = 'foo '
    ...   PREFIX_END = 'bar'
    ...   HEADER_FMT = '--- %s: %s'
    ...   def _generate(self, source=None): pass
    >>> handler = Handler(None)
    >>> print handler.generate_header({'title': 'foobar'})
    foo !b
    --- title: foobar
    bar
    <BLANKLINE>
    >>> print handler.generate_header({'labels': ['foo', 'bar']})
    foo !b
    --- labels: foo, bar
    bar
    <BLANKLINE>
    """
    if header is None:
      header = self.header

    lines = [self.PREFIX_HEAD + '!b']
    for k, v in header.items():
      if k == 'labels':
        v = ', '.join(v)
      lines.append(self.HEADER_FMT % (k, v))
    lines.append(self.PREFIX_END)
    return '\n'.join(filter(None, lines)) + '\n'

  def generate_title(self, title=None):
    """Generate title for posting
    
    >>> class Handler(BaseHandler):
    ...   def _generate(self, source=None): return source
    >>> handler = Handler(None)
    >>> print handler.generate_title('foo "bar"')
    foo "bar"
    >>> handler.options['smartypants'] = True
    >>> print handler.generate_title('foo "bar"')
    foo &#8220;bar&#8221;
    >>> print repr(handler.generate_title('foo\\nbar\\n\\n'))
    'foo bar'
    """
    if title is None:
      title = self.header.get('title', self.title)

    title = self.generate(title)
    title = title.replace('<p>', '').replace('</p>', '')
    # no trailing newlines
    title = title.rstrip('\n')
    title = title.replace('\n', ' ')
    return title

  def generate_post(self):
    """Generate dict for merging to post object of API"""
    post = {'title': self.generate_title()}
    for k in ('blog', 'id', 'labels'):
      if k not in self.header:
        continue
      if k == 'blog':
        post[k] = {'id': self.header[k]}
      else:
        post[k] = self.header[k]
    return post

  def split_header_markup(self, source=None):

    if source is None:
      source = self.source

    header, markup = self.RE_SPLIT.match(source).groups()

    _header = {}
    if header:
      for item in header.split('\n'):
        m = self.RE_HEADER.match(item)
        if not m:
          continue
        k, v = map(str.strip, m.groups())
        if k == 'labels':
          v = [label.strip() for label in v.split(',')]
        _header[k] = v
    header = _header

    return header, markup

  def update_source(self, header=None, markup=None, only_returned=False):

    if header is None:
      header = self.header
    if markup is None:
      markup = self.markup

    source = self.generate_header(header) + \
             '\n' + \
             markup
    if not only_returned:
      self.source = source
    return source

  def write(self, forced=False):
    """Write source back to file"""
    if not self.modified:
      if not forced:
        return
    else:
      self.update_source()

    with open(self.filename, 'w') as f:
      f.write(self.source)
    self.modified = False
