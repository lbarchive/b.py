# Copyright (C) 2013, 2014 Yu-Jie Lin
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


import test_bpy_handlers_base as test_base
from bpy.handlers.text import Handler


class HandlerTestCase(test_base.BaseHandlerTestCase):

  def setUp(self):

    self.handler = Handler(None)

  # =====

  def test_generate_title_pre_wrap_oneline(self):

    handler = self.handler
    handler.options['pre_wrap'] = True
    super(HandlerTestCase, self).test_generate_title_oneline()

  def test_generate_pre_wrap_multiline(self):

    handler = self.handler
    handler.options['pre_wrap'] = True
    super(HandlerTestCase, self).test_generate_title_multiline()

  def test_generate_pre_wrap_common_markup(self):

    handler = self.handler
    handler.options['pre_wrap'] = True
    super(HandlerTestCase, self).test_generate_title_common_markup()

  # =====

  def test_embed_images(self):

    handler = self.handler
    self.assertRaises(RuntimeError, handler.embed_images, ('', ))

  def test_embed_images_generate(self):

    handler = self.handler
    handler.options['embed_images'] = True

    handler.markup = '<img src="http://example.com/example.png"/>'
    html = handler.generate()
    EXPECT = '&lt;img src="http://example.com/example.png"/&gt;'
    self.assertEqual(html, EXPECT)
