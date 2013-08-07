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

from __future__ import unicode_literals
import unittest
import sys

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
    self.assertEqual(header, {})
    self.assertEqual(markup, 'post content')

  def test_header_labels_none(self):

    handler = self.handler
    handler.source = '''!b
labels:

post content'''
    header, markup = handler.split_header_markup()
    self.assertEqual(header, {'labels': []})
    self.assertEqual(markup, 'post content')

  def test_header_labels_single(self):

    handler = self.handler
    handler.source = '''!b
labels: foobar

post content'''
    header, markup = handler.split_header_markup()
    self.assertEqual(header, {'labels': ['foobar']})
    self.assertEqual(markup, 'post content')

  def test_header_labels_two(self):

    handler = self.handler
    handler.source = '''!b
labels: foo, bar

post content'''
    header, markup = handler.split_header_markup()
    self.assertEqual(header, {'labels': ['foo', 'bar']})
    self.assertEqual(markup, 'post content')

  def test_header_labels_with_empty_label(self):

    handler = self.handler
    handler.source = '''!b
labels: foo, , bar

post content'''
    header, markup = handler.split_header_markup()
    self.assertEqual(header, {'labels': ['foo', 'bar']})
    self.assertEqual(markup, 'post content')

  # =====

  def test_merge_header(self):

    handler = self.handler
    header = {'id': '123'}

    handler.header = header.copy()
    handler.merge_header(header.copy())
    self.assertEqual(handler.header, header)

    header['id'] = '456'
    header['blah'] = 'lol'
    handler.merge_header(header.copy())
    del header['blah']
    self.assertEqual(handler.header, header)

    header['id'] = '789'
    uheader = {'id': '789'}
    handler.merge_header(uheader.copy())
    self.assertEqual(handler.header, header)
    self.assertIsInstance(handler.header['id'], type(''))

    header['id'] = '123'
    uheader = {'id': '123'}
    handler.merge_header(uheader.copy())
    self.assertEqual(handler.header, header)
    self.assertIsInstance(handler.header['id'], type(''))
    self.assertEqual(list(handler.header.keys()), ['id'])
    self.assertIsInstance(list(handler.header.keys())[0], type(''))

    handler.header = {}
    handler.merge_header(uheader.copy())
    self.assertEqual(handler.header, header)
    self.assertIsInstance(handler.header['id'], type(''))
    self.assertEqual(list(handler.header.keys()), ['id'])
    self.assertIsInstance(list(handler.header.keys())[0], type(''))

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

  # =====

  test_markup_affixes_EXPECT1 = 'prefix-content-suffix'
  test_markup_affixes_EXPECT2 = 'foobar'
  test_markup_affixes_EXPECT3 = 'title'

  def test_markup_affixes(self):

    handler = self.handler
    handler.title = 'title'
    handler.markup = 'content'
    handler.options['markup_prefix'] = 'prefix-'
    handler.options['markup_suffix'] = '-suffix'

    self.assertEqual(
      handler.generate(),
      self.test_markup_affixes_EXPECT1)

    self.assertEqual(
      handler.generate('foobar'),
      self.test_markup_affixes_EXPECT2)

    self.assertEqual(
      handler.generate_title(),
      self.test_markup_affixes_EXPECT3)

  # =====

  def test_split_header_markup(self):

    handler = self.handler
    handler.source = '''xoxo !b oxox
abc=  foo
 def:bar

post content'''
    header, markup = handler.split_header_markup()
    expect = {'abc': 'foo', 'def': 'bar'}
    self.assertEqual(header, expect)
    self.assertEqual(markup, 'post content')

    source = '%s!b\n' % handler.PREFIX_HEAD
    source += handler.HEADER_FMT % ('abc', 'foo') + '\n'
    source += handler.HEADER_FMT % ('def', 'bar') + '\n'
    if handler.PREFIX_END:
      source += handler.PREFIX_END + '\n'
    source += '\npost content'
    handler.source = source
    header, markup = handler.split_header_markup()
    self.assertEqual(header, expect)
    self.assertEqual(markup, 'post content')

  # =====

  def test_generate_header(self):

    handler = self.handler
    handler.set_header('id', '123')
    expect = '%s!b\n%s\n' % (handler.PREFIX_HEAD,
                             handler.HEADER_FMT % ('id', '123'))
    if handler.PREFIX_END:
      expect += handler.PREFIX_END + '\n'

    self.assertEqual(handler.generate_header(), expect)

  # =====

  def test_generate_title_oneline(self):

    handler = self.handler
    title = 'foobar'
    expect = 'foobar'

    result = handler.generate_title(title)
    self.assertEqual(result, expect)

  def test_generate_title_multiline(self):

    handler = self.handler
    title = 'foo\nbar\n\nblah'
    expect = 'foo bar blah'

    result = handler.generate_title(title)
    self.assertEqual(result, expect)

  test_generate_title_common_markup_EXPECT = 'foo *bar*'

  def test_generate_title_common_markup(self):

    handler = self.handler
    title = 'foo *bar*'

    result = handler.generate_title(title)
    expect = self.test_generate_title_common_markup_EXPECT
    self.assertEqual(result, expect)

  # =====

  test_generate_str_MARKUP = '\xc3\xa1'
  test_generate_str_EXPECT = '\xc3\xa1'

  def test_generate__str(self):

    handler = self.handler

    html = handler._generate(self.test_generate_str_MARKUP)
    self.assertEqual(html, self.test_generate_str_EXPECT)
    self.assertIsInstance(html, type(''))

  def test_generate_str(self):

    handler = self.handler
    handler.markup = self.test_generate_str_MARKUP

    html = handler.generate()
    self.assertEqual(html, self.test_generate_str_EXPECT)
    self.assertIsInstance(html, type(''))

  # =====

  test_smartypants_MARKUP = 'foo "bar"'
  test_smartypants_EXPECT = 'foo &#8220;bar&#8221;'

  def test_smartypants(self):

    handler = self.handler
    handler.options['smartypants'] = True
    handler.markup = self.test_smartypants_MARKUP

    if sys.version_info.major == 3:
      with self.assertRaises(NotImplementedError):
        html = handler.generate()
      return

    html = handler.generate()
    self.assertEqual(html, self.test_smartypants_EXPECT)
    self.assertIsInstance(html, type(''))

  # =====

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
      'draft': False,
      'id': '123',
      'blog': {'id': '456'}
    })

  # =====

  def test_update_source(self):

    handler = self.handler
    source = '%s!b\n%s\n' % (handler.PREFIX_HEAD,
                             handler.HEADER_FMT % ('id', '123'))
    if handler.PREFIX_END:
      source += handler.PREFIX_END + '\n'
    source += '\npost content'
    handler.source = source

    header, markup = handler.split_header_markup()
    handler.header = header
    handler.markup = markup

    handler.update_source()
    self.assertEqual(handler.source, source)

    handler.options['markup_prefix'] = 'PREFIX'

    handler.update_source()
    self.assertEqual(handler.source, source)
