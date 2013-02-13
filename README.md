b.py
====

> *Publishing (technical) posts to Blogger in your favorite markup language seamlessly without much fuss.*

**b.py** is a Python program which enables [Blogger][] bloggers to blog from command-line.

Current status
--------------

* Python: 2.7
* System: Linux
* Markup handlers: AsciiDoc, HTML, Markdown, reStructuredText, Text
* Post data

    API v3 only supports `insert` and `update` on posts resources, no pages support at this moment.

    * Title
    * Labels
    * Content

* Miscellaneous

    * [smartypants][] for all handlers.

* Tests/checks

    * Unittest: `python setup.py test`
    * PEP8 (4-space indentation is ignored): `python setup.py pep8`
    * Pyflakes: `python setup.py pyflakes`
    * Pylint: `python setup.py pylint`

I wish *b.py* can support major operating systems and many markup languages someday, even different blogging platform, if possible.

*If anything is unclear since this is a new project, open an [issue][issues] for it.*

Dependencies
------------

* [Google APIs Client Library for Python][GoogleAPI]

        easy_install --upgrade google-api-python-client

Installation
------------

    $ pip install b.py

### Authorization

You need to authorize *b.py* to access your Blogger account. Simply using `blogs` command (see *Commands* section) would get you into the authorization process:

    $ b.py blogs

Once you follow the steps and finish, there should be a `b.dat` credential file created under the current working directory, you should keep it safe.

### Basic configuration file

Beside the `b.dat` above, you may also need a `brc.py`, the *b.py* local configuration file. For starter, the following setting should be sufficient:

    blog = <THE BLOG ID>

You can use `blogs` command to quickly get the blog ID.

Commands
--------

### `blogs`

List blogs. This can be used for blog IDs lookup.

### `post`

Post or update a blog post.

### `generate`

Generate HTML file at `/tmp/draft.html`.

The generation can output a preview html at `/tmp/preview.html` if there is `tmpl.html`. It will replace `%%Title%%` with post title and `%%Content%%` with generated HTML.

### `checklink`

Check links in generated HTML using [lnkckr][].

Work (post) flow
----------------

You should have completed the steps in *Installation* section, that is having `bpy.rc` and `b.dat` reside in the directory for your posts.

Let's create a first post, `my-first-post.rst`:

    .. !b
       title: My First Post
       labels: blogging

    Hooray, posting frm commandline!

Then issue the command to post it to Blogger:

    $ b.py post my-first-post.rst

If it runs without problem, then open the file again, the header part would have been edited and may look like:

    .. !b
       kind: post
       url: http://[...].blogspot.com/2013/01/my-first-post.html
       labels: blogging
       id_affix: 5e5f
       blog: <THE BLOG ID>
       id: <THE POST ID>
       title: My First Post

The detail of header, please see *Header* section.

Now, you spot there is a typo `frm` and you fix it. To update the post, run the same command as posting:

    $ b.py post my-first-post.rst

The `blog` and `id` in the header tells *b.py* which post to update.

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

Markup handlers and their IDs, libraries, and extensions:

* [AsciiDoc][] (`AsciiDoc`): `.asciidoc`
* HTML (`HTML`): `.html`, `.htm`, `.raw`
* [Markdown][] (`Markdown`): `.md`, `.mkd`, `.mkdn`, `.mkdown`, `.markdown`
* [reStructuredText][] (`reStructuredText`): `.rst`
* Text (`Text`): `.txt`, `.text`

[AsciiDoc]: http://www.methods.co.nz/asciidoc/
[Markdown]: http://pypi.python.org/pypi/Markdown
[reStructuredText]: http://docutils.sourceforge.net/rst.html

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

### AsciiDoc

No options are available at this moment.

### HTML

HTML handler simply takes the file content as its output, and assume it's valid HTML, therefore the handler doesn't edit or validate the content.

No options are available at this moment.

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
          'register_directives': {
            'dir_name': MyDir,
          },
          'register_roles': {
            'role_name': MyRole,
          },
          'settings_overrides': {
            'footnote_references': 'brackets',
          },
        },
      },
    }

#### Custom Directives and Roles

For adding your own custom reStructuredText directives or roles, you can do it in `brc.py` with one of the following method:

* by calling register functions of docutils directly,
* by adding in b.py's option as shown above, or
* by using decorator of b.py, for example:

        :::python
        from docutils.parsers.rst import Directive
        from bpy.handlers.rst import register_directive, register_role

        @register_directive('mydir')
        class MyDir(Directive):
          pass

        @register_role('myrole')
        def myrole(name, rawtext, text, lineno, inliner, options=None, content=None):
          pass

### Text

The Text handler for plain text always escape HTML, and add `<br/>` if not `pre_wrap`.

You can specify the following options for plain text in `brc.py`, for example:

    :::python
    handlers = {
      'Text': {
        'options': {
          'pre_wrap': False
        },
      },
    }

`pre_wrap` will wrap output in `<pre/>` tag.

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

Links
-----

* [PyPI][]

License
-------

    This project is licensed under the MIT License, see COPYING.
    Copyright (C) 2011-2013 by Yu-Jie Lin.

[Blogger]: http://www.blogger.com
[smartypants]: http://pypi.python.org/pypi/smartypants
[GoogleAPI]: https://developers.google.com/blogger/docs/3.0/api-lib/python
[markdown-config]: http://packages.python.org/Markdown/reference.html#markdown
[settings-overrides]: http://docutils.sourceforge.net/docs/user/config.html#html4css1-writer
[issues]: https://bitbucket.org/livibetter/b.py/issues
[PyPI]: http://pypi.python.org/pypi/b.py
[lnkckr]: https://bitbucket.org/livibetter/lnkckr
