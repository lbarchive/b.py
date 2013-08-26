======
Header
======

A header is used to specify the meta-data of a post, such as title or labels,
it is also used to store information which is needed to update a post later on,
such as ``id``.

In reStructuredText (different markup has different style of header), a header
look like

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

In normal usage, you may specify ``title`` and ``labels``. ``title`` will
override the post title, if this is missed, the post title will be the filename
without the extension.

``service``, ``kind``, ``blog``, ``id``, and ``url`` are automatically added
after a successful posting. ``url`` doesn't actually mean anything, just for
you to have a record of the URL of a post.

``service`` is the service is used for processing.

``kind`` is the type of the posting, ``post`` or ``page``, default is ``post``
and currently Blogger service only supports ``post``.

``categories`` is the catgories, only WordPress service uses this.

``draft`` is the post status, ``true``, ``yes``, or ``1`` for draft post,
otherwise published post. Only WordPress service supports this.

``blog`` and ``id`` are very important, they are used in updating post and they
should not be edited by you.

``id_affix`` is the affix to HTML element ID, see also the General Options of
Handlers.
