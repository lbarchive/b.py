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
import httplib2
import os
import sys

if sys.version_info.major == 2:
  from apiclient.discovery import build
  from oauth2client.client import OAuth2WebServerFlow
  from oauth2client.file import Storage as BaseStorage
  from oauth2client.tools import run

  API_STORAGE = 'b.dat'

  class Storage(BaseStorage):
    """Inherit the API Storage to suppress CredentialsFileSymbolicLinkError
    """

    def __init__(self, filename):

      super(Storage, self).__init__(filename)
      self._filename_link_warned = False

    def _validate_file(self):

      if os.path.islink(self._filename) and not self._filename_link_warned:
        print('File: %s is a symbolic link.' % self._filename)
        self._filename_link_warned = True

from bpy.services.base import Service as BaseService
from bpy.handlers import find_handler


class Service(BaseService):

  service_name = 'blogger'

  def __init__(self, *args, **kwargs):

    super(Service, self).__init__(*args, **kwargs)

    self.http = None
    self.service = None

  def auth(self):

    if sys.version_info.major != 2:
      msg = ('This command requires google-api-python-client, '
             'which only support Python 2')
      raise RuntimeError(msg)

    if self.http and self.service:
      return

    FLOW = OAuth2WebServerFlow(
      '56045325640.apps.googleusercontent.com',
      'xCzmIv2FUWxeQzA5yJvm4w9U',
      'https://www.googleapis.com/auth/blogger',
      auth_uri='https://accounts.google.com/o/oauth2/auth',
      token_uri='https://accounts.google.com/o/oauth2/token',
    )

    storage = Storage(API_STORAGE)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
      credentials = run(FLOW, storage)

    http = httplib2.Http()
    self.http = credentials.authorize(http)
    self.service = build("blogger", "v3", http=self.http)

  def list_blogs(self):

    self.auth()
    blogs = self.service.blogs()
    req = blogs.listByUser(userId='self')
    resp = req.execute(http=self.http)
    print('%-20s: %s' % ('Blog ID', 'Blog name'))
    for blog in resp['items']:
      print('%-20s: %s' % (blog['id'], blog['name']))

  def make_handler_post(self):

    handler = find_handler(self.filename)
    if not handler:
      print('No handler for the file!')
      sys.exit(1)

    hdr = handler.header

    post = {
      'service': self.service_name,
      # default resource kind is blogger#post
      'kind': 'blogger#%s' % hdr.get('kind', 'post'),
      'content': handler.generate(),
    }
    if isinstance(self.blog_id, int):
      post['blog'] = {'id': self.blog_id}
    post.update(handler.generate_post())

    return handler, post

  def post(self, blog_id=None):

    handler, post = self.make_handler_post()

    if 'blog' not in post:
      print('You need to specify which blog to post on '
            'in either brc.py or header of %s.' % handler.filename)
      sys.exit(1)

    self.auth()

    kind = post['kind'].replace('blogger#', '')
    title = post['title']

    if kind == 'post':
      posts = self.service.posts()
    else:
      raise ValueError('Unsupported kind: %s' % kind)

    if 'id' in post:
      print('Updating a %s: %s' % (kind, title))
      req = posts.update(blogId=post['blog']['id'], postId=post['id'],
                         body=post)
    else:
      print('Posting a new %s: %s' % (kind, title))
      req = posts.insert(blogId=post['blog']['id'], body=post)

    resp = req.execute(http=self.http)

    handler.merge_header(resp)
    handler.write()

  def search(self, blog_id, q):

    self.auth()

    fields = 'items(labels,published,title,url)'
    posts = self.service.posts()
    req = posts.search(blogId=blog_id, q=q, fields=fields)
    resp = req.execute(http=self.http)
    items = resp.get('items', [])
    print('Found %d posts on Blog %s' % (len(items), blog_id))
    print()
    for post in items:
      print(post['title'])
      labels = post.get('labels', [])
      if labels:
        print('Labels:', ', '.join(labels))
      print('Published:', post['published'])
      print(post['url'])
      print()
