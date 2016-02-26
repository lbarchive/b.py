# Copyright (C) 2013, 2016 by Yu-Jie Lin
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

import sys
import unittest

from bpy.services.blogger import Service
from test_bpy_services_base import BaseServiceTestCase


class ServiceTestCase(BaseServiceTestCase):

  def test_no_client_id(self):

    with self.assertRaises(RuntimeError):
      Service({'service_options': {}})

  @unittest.skipIf(sys.version_info.major == 2, 'only test with Python 3')
  def test_python3_error(self):

    with self.assertRaises(RuntimeError):
      service = Service({
        'service_options': {
          'client_id': 'dummy',
          'client_secret': 'dummy',
        }
      })
      service.list_blogs()
