b.sh (b.py)
===========

**b.sh** is a program which enables [Blogger][] bloggers to blog from command-line. *b.sh* is the previous implementation on Blogger GData V2 API and *b.py* is the current implementation on Blogger V3 API.

[Blogger]: http://www.blogger.com

As the extension suggests, *b.sh* is written in shell script and requires [GoogleCL][]. *b.sh* is deprecated due to the flaw in Blogger GData V2 API, which adding `<br/>` after `\n`, rendering the posting via API unusable.

[GoogleCL]: http://code.google.com/p/googlecl/

*b.py* is written in Python 2.7 at this moment. No support for Python 3 yet, because of [Google APIs Client Library][GoogleAPI] only supports Python 2.5-2.7.

The project's name is *b.sh* and will be used continuously even though it's no longer written in shell script, but the main program's name is *b.py*.

[GoogleAPI]: https://developers.google.com/blogger/docs/3.0/api-lib/python


Current status
--------------

* Python: 2.7
* System: Linux
* Markup handlers

    * Markdown
    * reStructuredText


Dependencies
------------

* [Google APIs Client Library for Python][GoogleAPI]

        easy_install --upgrade google-api-python-client


Installation
------------

* Clone this repository to, say, `/home/user/b.sh/`
* Set up search path for `b.py`, e.g. `PATH=$PATH:/home/user/b.sh`
* Switch to directory where you store posts, say, `/home/user/posts/`
* Run `b.py blogs` to authorize this program to access via listing blogs.

    * Once you completed, there should be a `/home/user/posts/b.dat` credential file, which should be kept safe.

* Create a configuration file `brc.py` with the content as follows

        :::python
        blog = your_blog_id

    The blog IDs can be retrieved by `b.py blogs`, pick the right blog's ID.


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

In this section, I will explain how you can use *b.py* to post. We will assume you are in where you store your blog post markup files, say, `/home/user/posts` and the markup language is reStructuredText.

* Create and write a new post `my-new-post.rst`

    * You can also add `title` and `labels` header, header will be explained in later section.

* Post it by `b.py post my-new-post.rst`

That should be it, your new post should be published. Load the `my-new-post.rst` again, you should notice that there is something being added at top of the file.

You can edit and run `b.py post my-new-post.rst` again to update the post.


Header
------

A header is used to specify the meta-data of a post, such as title or labels, it is also used to store information which is needed to update a post later on, such as `id`.

In reStructuredText, different markup has different style of header, a header look like

    .. !b
       title: Title of "something."
       labels: comma, separated, list
       blog: 12345
       id: 54321
       url: http://example.com/2013/01/title-of-something.html

In normal usage, you may specify `title` and `labels`. `title` will override the post title, if this is missed, the post title will be the filename without extension.

`blog`, `id`, and `url` are automatically added after a successful posting. `url` doesn't actually mean anything, just for you to have a record of the URL of a post.

`blog` and `id` are very important, they are used in updating post and they should not be edited by you.


Configuration
-------------

### `brc.py`

It's the configuration that *b.py* reads from current working directory. Currently, only `blog` and `handlers` are used.

Handlers
--------

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

[markdown-config]: http://packages.python.org/Markdown/reference.html#markdown

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

[settings-overrides]: http://docutils.sourceforge.net/docs/user/config.html#html4css1-writer

### Custom handler

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


License
-------

*b.sh* is licensed under the MIT License, see `COPYING`. Copyright (C) 2011-2013 by Yu-Jie Lin.
