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


import argparse as ap
import httplib2
import imp
import json
import os
from os import path
from os.path import dirname, realpath
import re
import sys
import traceback

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage as BaseStorage
from oauth2client.tools import run


__program__ = 'b.py'
__author__ = 'Yu-Jie Lin'
__copyright__ = 'Copyright 2013, Yu Jie Lin'
__license__ = 'MIT'
__version__ = '0.1'
__website__ = 'http://bitbucket.org/livibetter/b.sh'


# API stuff
###########

# global stuff
http = None
service = None

# filename of credentials
CLIENT_SECRETS = path.join(dirname(realpath(sys.argv[0])),
                           'client_secrets.json')
API_SCOPE ='https://www.googleapis.com/auth/blogger'
NOTFOUND_MESSAGE = 'Could not found client_secrets.json'
API_STORAGE = 'b.dat'


class Storage(BaseStorage):
  """Inherit the API Storage to suppress CredentialsFileSymbolicLinkError
  """

  def __init__(self, filename):

    super(Storage, self).__init__(filename)
    self._filename_link_warned = False

  def _validate_file(self):

    if os.path.islink(self._filename) and not self._filename_link_warned:
      print 'File: %s is a symbolic link.' % self._filename
      self._filename_link_warned = True


# b.py stuff
############

# filename of local configuration without '.py' suffix.
BRC = 'brc'
TEMPLATE_PATH = path.join(os.getcwd(), 'tmpl.html')

# handlers for markup files
handlers = {
  'Markdown': {
    'match': re.compile(r'.*\.(markdown|md(own)?|mkdn?)$'),
    'module': path.join('bpy', 'handlers', 'mkd'),
  },
  'reStructuredText': {
    'match': re.compile(r'.*\.rst$'),
    'module': path.join('bpy', 'handlers', 'rst'),
  },
}


def parse_args():

  p = ap.ArgumentParser()
  sp = p.add_subparsers(help='commands')

  pblogs = sp.add_parser('blogs', help='list blogs')
  pblogs.set_defaults(subparser=pblogs, command='blogs')

  pgen = sp.add_parser('generate', help='generate html')
  pgen.add_argument('filename')
  pgen.set_defaults(subparser=pgen, command='generate')

  ppost = sp.add_parser('post', help='post or update a blog post')
  ppost.add_argument('filename')
  ppost.set_defaults(subparser=ppost, command='post')

  args = p.parse_args()
  return args


def load_config():

  rc = None
  try:
    search_path = [os.getcwd()]
    _mod_data = imp.find_module(BRC, search_path)
    print 'Loading local configuration...'
    try:
      rc = imp.load_module(BRC, *_mod_data)
    finally:
      if _mod_data[0]:
        _mod_data[0].close()
  except ImportError as e:
    pass
  except Exception as e:
    traceback.print_exc()
    print 'Error in %s, aborted.' % _mod_data[1]
    sys.exit(1)
  return rc


def find_handler(filename):

  search_path = [os.getcwd()] + sys.path
  module = None
  for name, hdlr in handlers.items():
    if hdlr['match'].match(filename):
      try:
        _mod_data = imp.find_module(hdlr['module'], search_path)
        try:
          module = imp.load_module(name, *_mod_data)
        finally:
          if _mod_data[0]:
            _mod_data[0].close()
          if module:
            break
      except ImportError:
        print 'Cannot load module %s of handler %s' % (hdlr['module'], name)
      except Exception as e:
        traceback.print_exc()
  if module:
    return module.Handler(filename, hdlr.get('options', {}))
  return None


def posting(post, http, service):

  posts = service.posts()

  if 'id' in post:
    print 'Updating post...'
    req = posts.update(blogId=post['blog']['id'], postId=post['id'], body=post)
  else:
    print 'Posting new post...'
    req = posts.insert(blogId=post['blog']['id'], body=post)

  resp = req.execute(http=http)
  return resp


def get_http_service():

  global http, service

  if http and service:
    return http, service

  FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
                                 scope=API_SCOPE,
                                 message=NOTFOUND_MESSAGE)

  storage = Storage(API_STORAGE)
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = run(FLOW, storage)

  http = httplib2.Http()
  http = credentials.authorize(http)
  service = build("blogger", "v3", http=http)

  return http, service


def main():

  args = parse_args()

  rc = load_config()
  if rc:
    if hasattr(rc, 'handlers'):
      for name, handler in rc.handlers.items():
        if name in handlers:
          handler.update(rc.handlers[name])
        handler[name] = rc.handlers[name].copy()

  if args.command == 'blogs':
    http, service = get_http_service()
    blogs = service.blogs()
    req = blogs.listByUser(userId='self')
    resp = req.execute(http=http)
    print '%-20s: %s' % ('Blog ID', 'Blog name')
    for blog in resp['items']:
      print '%-20s: %s' % (blog['id'], blog['name'])
  elif args.command in ('generate', 'post'):
    handler = find_handler(args.filename)
    if not handler:
      print 'No handler for the file!'
      sys.exit(1)

    hdr = handler.header

    post = {
      'kind': 'blogger#post',
      'content': handler.generate(),
    }
    if rc:
      if hasattr(rc, 'blog'):
        post['blog'] = {'id': rc.blog}
    post.update(handler.generate_post())

    if args.command == 'generate':
      with open('/tmp/draft.html', 'w') as f:
        f.write(post['content'])

      if args.command == 'generate' and path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH) as f:
          html = f.read()
        html = html.replace('%%Title%%', post['title'])
        html = html.replace('%%Content%%', post['content'])
        with open('/tmp/preview.html', 'w') as f:
          f.write(html)
      return

    if 'blog' not in post:
      print 'You need to specify which blog to post on in either brc.py or header of %s.' % handler.filename
      sys.exit(1)

    http, service = get_http_service()
    resp = posting(post, http, service)

    handler.merge_header(resp)
    handler.write()


if __name__ == '__main__':
  main()