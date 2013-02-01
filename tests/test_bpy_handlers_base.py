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

  def test_header_no_labels(self):
    
    handler = self.handler
    handler.source = '''!b

post content'''
    header, markup = handler.split_header_markup()
    self.assertEqual(header, {
      })
    self.assertEqual(markup, 'post content')

  def test_header_labels_none(self):
    
    handler = self.handler
    handler.source = '''!b
labels:

post content'''
    header, markup = handler.split_header_markup()
    self.assertEqual(header, {
      'labels': [],
      })
    self.assertEqual(markup, 'post content')

  def test_header_labels_single(self):
    
    handler = self.handler
    handler.source = '''!b
labels: foobar

post content'''
    header, markup = handler.split_header_markup()
    self.assertEqual(header, {
      'labels': ['foobar'],
      })
    self.assertEqual(markup, 'post content')

  def test_header_labels_two(self):
    
    handler = self.handler
    handler.source = '''!b
labels: foo, bar

post content'''
    header, markup = handler.split_header_markup()
    self.assertEqual(header, {
      'labels': ['foo', 'bar'],
      })
    self.assertEqual(markup, 'post content')

  def test_header_labels_with_empty_label(self):
    
    handler = self.handler
    handler.source = '''!b
labels: foo, , bar

post content'''
    header, markup = handler.split_header_markup()
    self.assertEqual(header, {
      'labels': ['foo', 'bar'],
      })
    self.assertEqual(markup, 'post content')

  # =====

  def test_id_affix(self):

    handler = self.handler
    handler.title = 'test'

    def test_header_override():

      handler.header['id_affix'] = None
      self.assertEqual(handler.id_affix, None)

      handler.header['id_affix'] = ''
      self.assertEqual(handler.id_affix, '098f')

      handler.header['id_affix'] = 'prefix'
      self.assertEqual(handler.id_affix, 'prefix')
      
    # -----

    self.assertEqual(handler.id_affix, None)

    # -----

    handler.options['id_affix'] = None
    self.assertEqual(handler.id_affix, None)

    test_header_override()

    # -----

    del handler.header['id_affix']

    handler.options['id_affix'] = ''
    self.assertEqual(handler.id_affix, '098f')

    test_header_override()

    # -----

    del handler.header['id_affix']

    handler.options['id_affix'] = 'prefix'
    self.assertEqual(handler.id_affix, 'prefix')

    test_header_override()

  def test_markup_affixes(self):

    handler = self.handler
    handler.title = 'title'
    handler.markup = 'content'
    handler.options['markup_prefix'] = 'prefix>'
    handler.options['markup_suffix'] = '<suffix'

    expect = 'prefix>content<suffix'
    self.assertEqual(handler.generate(), expect)

    expect = 'foobar'
    self.assertEqual(handler.generate('foobar'), expect)

    expect = 'title'
    self.assertEqual(handler.generate_title(), expect)

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
