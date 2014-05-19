========
Tutorial
========


Setting up
==========

You should have completed the steps in :ref:`Installation` and the service
sections, that is having the following file(s) reside in the directory for your
posts and all :ref:`Dependencies` installed properly.

* :mod:`Blogger service <bpy.services.blogger>`: :ref:`brc.py` and
  :ref:`b.dat`; or
* :mod:`WordPress service <bpy.services.wordpress>`: :ref:`brc.py`


Creating the first post
=======================

Let's create a first post, ``my-first-post.rst`` or ``my-first-post.md``,
whatever markup language floats your boat:

.. code:: rst

  !b
  service: blogger
  title: My First Post
  labels: blogging

  Hooray, posting frm commandline!

The first three lines are called :doc:`header`, when *b.py* sees ``!b`` in the
beginning of file, it knows what to do with the header. If you are using
WordPress, change service line to::

  service: wordpress


Posting to the service
======================

After saves the file, run the following command to post it to the service:

.. code:: sh

  b.py post my-first-post.rst

If it runs without any problems, then open the file again, the header part
should have been edited by *b.py* and may look like:

.. code:: rst

  .. !b
     service: blogger
     kind: post
     url: http://[...].blogspot.com/2013/01/my-first-post.html
     labels: blogging
     id_affix: 5e5f
     blog: <THE BLOG ID>
     id: <THE POST ID>
     title: My First Post

*b.py* will insert some data to header and make header into a comment.

.. seealso:: For the detail of header, please see :doc:`header`.


Updating the post
=================

After posting to the service, you spot there is a typo ``frm`` and you correct
it. To update the post, run the same command as posting:

.. code:: sh

  b.py post my-first-post.rst

The post should be updated on the service.

If *b.py* sees ``blog`` and ``id`` in header, then it knows that's a post
already published, so it will update it instead of creating a new post.
