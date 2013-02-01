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

from bpy.handlers.mkd import Handler

import test_bpy_handlers_base as test_base


class HandlerTestCase(test_base.BaseHandlerTestCase):

  def setUp(self):

    self.handler = Handler(None)

  def test_markup_affixes(self):

    handler = self.handler
    handler.title = 'title'
    handler.markup = 'content'
    handler.options['markup_prefix'] = 'prefix-'
    handler.options['markup_suffix'] = '-suffix'

    expect = '<p>prefix-content-suffix</p>'
    self.assertEqual(handler.generate(), expect)

    expect = '<p>foobar</p>'
    self.assertEqual(handler.generate('foobar'), expect)

    expect = 'title'
    self.assertEqual(handler.generate_title(), expect)

