======
Header
======

A header is used to specify the meta-data of a post, such as title or labels,
it is also used to store information which is needed to update a post later on,
such as ``id``.

Generally, header can be simply formed as the following regardless which markup
language handler you use::

  !b
  key1: value1
  key2: value2

  post content goes here

The handler will automatically reformed the header into *comment* after posting
or updating, the format of comment depends on the markup language. For example,
in reStructuredText, a header look like

.. code:: rst

  .. !b
     service: blogger
     kind: post
     title: Title of "something."
     labels: comma, separated, list
     categories: another, comma, separated, list
     draft: False
     blog: 12345
     id: 54321
     id_affix: foobar
     url: http://example.com/2013/01/title-of-something.html

Making header into comment, so it wouldn't be rendered out if it's processed by
tools other than *b.py*.


Keys
====

``service``:
  used for processing.

  It could be added automatically after successfully posting.

  .. seealso:: :doc:`apidoc/bpy.services`

``blog``:
  used in updating post and should not be edited by the user normally.

  It could be added automatically after successfully posting.
  
``id``:
  used in updating post and should not be edited by the user normally.

  It could be added automatically after successfully posting.

``title``:
  override the post title.
  
  If not specified, the post title will be the filename without the extension.

``kind``:
  type of the posting, ``post`` or ``page``, default is ``post``.
  
  It could be added automatically after successfully posting.

``labels``:
  labels or tags, comma-separated list.

``categories``:
  categories, comma-separated list.
  
  Only WordPress service uses this.

``draft``:
  the post status, ``true``, ``yes``, or ``1`` for draft post, otherwise
  published post.

  .. note:: Blogger page doesn't support draft status setting.

``url``:
  link of the post.

  It could be added automatically after successfully posting.

``id_affix``:
  the affix to HTML element ID.

  .. seealso:: :ref:`id_affix` in handler options.
