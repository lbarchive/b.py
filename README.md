b.sh (b.py)
===========

> *Publishing (technical) posts to Blogger in your favorite markup language seamlessly without much fuss.*

**b.sh** is a program which enables [Blogger][] bloggers to blog from command-line. *[b.py][]* is the current implementation on Blogger V3 API, written in Python 2.7 at this moment. No support for Python 3 yet, because of [Google APIs Client Library][GoogleAPI] only supports Python 2.5-2.7.

As the extension suggests, *[b.sh][]* was written in shell script and requires [GoogleCL][]. *b.sh* is deprecated due to the flaw in Blogger GData V2 API, which adds `<br/>` before each newline `\n`, rendering the posting via API unusable. The project's name is *b.sh* and will be used continuously even though it's no longer written in shell script.

Current status
--------------

* Python: 2.7
* System: Linux
* Markup handlers

    * Markdown
    * reStructuredText

* Post data

    API v3 only supports `insert` and `update` on posts resources, no pages support at this moment.
  
    * Title
    * Labels
    * Content

* Miscellaneous

    * [smartypants][] for all handlers.

I wish *b.sh* can support major operating systems and many markup languages someday, even different blogging platform, if possible.

*If anything is unclear since this is a new project, open an [issue][issues] for it.*

Dependencies
------------

* [Google APIs Client Library for Python][GoogleAPI]

        easy_install --upgrade google-api-python-client

Installation
------------

Assume

* Home directory is `/home/me/`.
* Clone this project to `/home/me/b.sh`.
* Posts stored at `/home/me/posts`.

The installation process:

    # clone b.sh
    $ cd ~
    $ hg clone https://bitbucket.org/livibetter/b.sh

    # set up search path for `b.py` in .bashrc
    # PATH=$PATH:/home/me/b.sh
    # then re-login for new $PATH

    # authorize and find blog ID you want to post
    $ b.py blogs
    # Note: there should be a `/home/user/posts/b.dat` credential file, which
    # should be kept safe.

    # add a local configuration
    $ cd /home/me/posts
    $ echo 'blog = <blog id>' > brc.py

Commands
--------

### `blogs`

List blogs. This can be used for blog IDs lookup.

### `post`

Post or update a blog post.

### `generate`

Generate HTML file at `/tmp/draft.html`.

The generation can output a preview html at `/tmp/preview.html` if there is `tmpl.html`. It will replace `%%Title%%` with post title and `%%Content%%` with generated HTML.

Work (post) flow
----------------

You should have completed the steps in *Installation* section, that is having `/home/me/posts/bpy.rc` and `/home/me/posts/b.dat`.

    # create the post
    $ cd /home/me/posts
    $ echo << EOF > my-first-post.rst
    .. !b
       title: my first post
       labels: blogging

    This is my **first post**.
    EOF

    # post it on Blogger
    $ b.py post my-new-post.rst

Once the post is posted successfully, *b.py* will update the header, adding blog ID, post ID, post URL, and some others. You can edit and run `b.py post my-new-post.rst` again to update the post.

Header
------

A header is used to specify the meta-data of a post, such as title or labels, it is also used to store information which is needed to update a post later on, such as `id`.

In reStructuredText (different markup has different style of header), a header look like

    .. !b
       kind: post
       title: Title of "something."
       labels: comma, separated, list
       blog: 12345
       id: 54321
       id_affix: foobar
       url: http://example.com/2013/01/title-of-something.html

In normal usage, you may specify `title` and `labels`. `title` will override the post title, if this is missed, the post title will be the filename without extension.

`kind`, `blog`, `id`, and `url` are automatically added after a successful posting. `url` doesn't actually mean anything, just for you to have a record of the URL of a post.

`kind` is the type of the posting, default is `post` and currently only supports `post`.

`blog` and `id` are very important, they are used in updating post and they should not be edited by you.

`id_affix` is the affix to HTML element ID, see also the General Options of Handlers.

Configuration
-------------

### `brc.py`

It's the configuration that *b.py* reads from current working directory. Currently, only `blog` and `handlers` are used, it may read like:

    :::python
    blog = 12345
    handlers = {
      ... # see Handler section
      }

Handlers
--------

Markup handlers and their IDs:

* Markdown: `Markdown`
* reStructuredText: `reStructuredText`

### General options

The general options are supported by all handlers, defined in `BaseHandler`, but they have to be specified per handler basis, the following sample code shows the options and their default value:

    :::python
    handlers = {
      '<MARKUP HANDLER ID>': {
        'options': {
          # prefix string to HTML ID to avoid conflict
          'id_affix': None,

          # string to prepend to actual markup
          'markup_prefix': '',

          # string to append to actual markup
          'markup_suffix': '',

          # use smartypant to process the output of markup processor
          'smartypants': False,
        },
      },
    }

`id_affix` is used to avoid conflict across posts' HTML element ID. It may be a prefix or suffix, depending on handler's implementation and markup library's support. It has three types of value:

1. `None`: no affix to ID.
2. non-empty string: the string is the affix.
3. empty string: the affix is generated automatically.

Currently supported markup handler:

* reStructuredText 

`markup_prefix` and `markup_suffix` can be useful for adding header and footer content for posts. Another useful case in reStructuredText is you can use it for setting up some directives, for example `.. sectnum::`, so you can ensure all posts have prefixing section number if in use conjunction with `.. contents::`.

If `smartypants` is enabled, then all generated HTML from markup processor will be processed by [smartypants][] library.

### Markdown

You can specify [configuration][markdown-config] for Python Markdown in `brc.py`, for example:

    :::python
    handlers = {
      'Markdown': {
        'options': {
          config: {
            'extensions': ['extension1', 'extension2'],
            'tab_length': 8,
          },
        },
      },
    }


### reStructuredText

You can specify [settings-overrides][] for reStructuredText in `brc.py`, for example:

    :::python
    handlers = {
      'reStructuredText': {
        'options': {
          'settings_overrides': {
            'footnote_references': 'brackets',
          },
        },
      },
    }


### Writing a custom handler

A sample handler `sample_handler.py`:

    :::python
    from bpy.handlers import base

    class Handler(base.BaseHandler):
      PREFIX_HEAD = ''
      PREFIX_END = '
      HEADER_FMT = '%s: %s'

      def _generate(self, markup=None):
        if markup is None:
          markup = self.markup

        html = do_process(markup)
        return html

And corresponding setting in `brc.py`:

    :::python
    import re

    handlers = {
      'SampleHandler': {
        'match': re.compile(r'.*\.ext$'),
        'module': 'sample_handler',
      },
    }

Help and Support
----------------

Please use [Issues][issues] to file a bug report or request a new feature.

Feel free to contribute and create a pull request.

License
-------

    This project is licensed under the MIT License, see COPYING.
    Copyright (C) 2011-2013 by Yu-Jie Lin.

[b.sh]: https://bitbucket.org/livibetter/b.sh/src/tip/b.sh
[b.py]: https://bitbucket.org/livibetter/b.sh/src/tip/b.sh
[Blogger]: http://www.blogger.com
[GoogleCL]: http://code.google.com/p/googlecl/
[smartypants]: http://pypi.python.org/pypi/smartypants
[GoogleAPI]: https://developers.google.com/blogger/docs/3.0/api-lib/python
[markdown-config]: http://packages.python.org/Markdown/reference.html#markdown
[settings-overrides]: http://docutils.sourceforge.net/docs/user/config.html#html4css1-writer
[issues]: https://bitbucket.org/livibetter/b.sh/issues
