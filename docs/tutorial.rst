========
Tutorial
========

You should have completed the steps in :ref:`Installation` and the service sections,
that is having the following file(s) reside in the directory for your posts:

* :mod:`Blogger service <bpy.services.blogger>`: :ref:`brc.py` and :ref:`b.dat`; or
* :mod:`WordPress service <bpy.services.wordpress>`: :ref:`brc.py`

Let's create a first post, ``my-first-post.rst``:

.. code:: rst

  .. !b
     title: My First Post
     labels: blogging

  Hooray, posting frm commandline!

Then issue the command to post it to the service::

  $ b.py post my-first-post.rst

If it runs without problem, then open the file again, the header part would
have been edited and may look like:

.. code:: rst

  .. !b
     kind: post
     url: http://[...].blogspot.com/2013/01/my-first-post.html
     labels: blogging
     id_affix: 5e5f
     blog: <THE BLOG ID>
     id: <THE POST ID>
     title: My First Post

.. seealso:: For the detail of header, please see :doc:`header`.

Now, you spot there is a typo ``frm`` and you fix it. To update the post, run
the same command as posting::

  $ b.py post my-first-post.rst

The ``blog`` and ``id`` in the header tells :doc:`b.py` which post to update.
