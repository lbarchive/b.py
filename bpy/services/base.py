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


from __future__ import print_function
import codecs
from io import StringIO
import os
from os import path
from tempfile import gettempdir

HAS_LNKCKR = False
try:
  from lnkckr.checkers.html import Checker
  HAS_LNKCKR = True
except ImportError:
  pass

TEMPLATE_PATH = path.join(os.getcwd(), 'tmpl.html')


class Service(object):
  """The base clase of markup handler"""

  service_name = 'base'

  def __init__(self, blog_id=None, filename=None):

    self.blog_id = blog_id
    self.filename = filename

  def post(self):
    """Publish the post to the service"""
    raise NotImplementedError

  def generate(self):

    handler, post = self.make_handler_post(self.filename)
    with codecs.open(path.join(gettempdir(), 'draft.html'), 'w',
                     encoding='utf8') as f:
      f.write(post['content'])

    if path.exists(TEMPLATE_PATH):
      with codecs.open(TEMPLATE_PATH, encoding='utf8') as f:
        html = f.read()
      html = html.replace('%%Title%%', post['title'])
      html = html.replace('%%Content%%', post['content'])
      with codecs.open(path.join(gettempdir(), 'preview.html'), 'w',
                       encoding='utf8') as f:
        f.write(html)

  def checklink(self):

    if not HAS_LNKCKR:
      print('You do not have lnkckr library')
      return
    handler, post = self.make_handler_post(self.filename)
    c = Checker()
    c.process(StringIO(post['content']))
    c.check()
    print()
    c.print_all()

  def search(self, q):
    """Search posts"""
    raise NotImplementedError
