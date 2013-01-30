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


import unittest
import doctest

from bpy.handlers.base import BaseHandler


class Handler(BaseHandler):

  def _generate(self, source=None):
    
    return source


class BaseHandlerTestCase(unittest.TestCase):

  def setUp(self):


    self.handler = Handler(None)

  def tearDown(self):

    self.handler = None

  def test_split_header_markup(self):

    handler = self.handler
    handler.source = '''xoxo !b oxox
abc=  foo  
 def:bar

post content'''
    header, markup = handler.split_header_markup()
    self.assertEqual(header, {
      'abc': 'foo',
      'def': 'bar',
      })
    self.assertEqual(markup, 'post content')

  def test_generate_post(self):

    handler = self.handler
    handler.source = '''!b
abc=foo
title=the title
id=123
blog: 456

post content'''
    header, markup = handler.split_header_markup()
    handler.header = header
    post = handler.generate_post()

    self.assertEqual(post, {
      'title': 'the title',
      'id': '123',
      'blog': {
        'id': '456',
        }
      })
