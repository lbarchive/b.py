============
Introduction
============

  *Publishing (technical) posts to Blogger or WordPress in your favorite markup
  language seamlessly without much fuss.*

**b.py** is a Python program which enables Blogger_ or WordPress_ bloggers to
blog from command-line.

.. _Blogger: http://www.blogger.com
.. _WordPress: http://wordpress.org


.. _Installation:

Installation
============

::

  $ pip install b.py

Or install to user-site, meaning no root required and install at your home
directory::

  $ pip install --user b.py

To upgrade::

  $ pip install --upgrade b.py

To uninstall::

  $ pip uninstall b.py


Dependencies
============

+------------------+----------------------------------------------------+--------+
| name             | dependency                                         | Python |
+==================+====================================================+========+
| **Services**                                                                   |
+------------------+----------------------------------------------------+--------+
| Blogger          | `Google APIs Client Library for Python`__::        | 2      |
|                  |                                                    |        |
|                  |   pip install google-api-python-client             |        |
+------------------+----------------------------------------------------+--------+
| WordPress        | python-wordpress-xmlrpc_::                         | 2 / 3  |
|                  |                                                    |        |
|                  |   pip install python-wordpress-xmlrpc              |        |
+------------------+----------------------------------------------------+--------+
| **Handlers**                                                                   |
+------------------+----------------------------------------------------+--------+
| AsciiDoc         | AsciiDoc_                                          | 2      |
+------------------+----------------------------------------------------+--------+
| HTML             | None                                               | 2 / 3  |
+------------------+----------------------------------------------------+--------+
| Markdown         | Markdown_                                          | 2 / 3  |
+------------------+----------------------------------------------------+--------+
| reStructuredText | reStructuredText_                                  | 2 / 3  |
+------------------+----------------------------------------------------+--------+
| Text             | None                                               | 2 / 3  |
+------------------+----------------------------------------------------+--------+
| **Others**                                                                     |
+------------------+----------------------------------------------------+--------+
| lnkckr           | lnkckr_                                            | 2 / 3  |
+------------------+----------------------------------------------------+--------+
| smartypants      | smartypants_ >= 1.8.0                              | 2 / 3  |
+------------------+----------------------------------------------------+--------+
| **Tests**                                                                      |
+------------------+----------------------------------------------------+--------+
| PEP8             |                                                    | 2 / 3  |
+------------------+----------------------------------------------------+--------+
| Pyflakes         |                                                    | 2 / 3  |
+------------------+----------------------------------------------------+--------+
| Pylint           |                                                    | 2 / 3  |
+------------------+----------------------------------------------------+--------+
| install\_test    | virtualenv, make                                   | 2 / 3  |
+------------------+----------------------------------------------------+--------+

__ https://developers.google.com/blogger/docs/3.0/api-lib/python
.. _python-wordpress-xmlrpc: https://github.com/maxcutler/python-wordpress-xmlrpc

.. _AsciiDoc: http://www.methods.co.nz/asciidoc/
.. _Markdown: http://pypi.python.org/pypi/Markdown
.. _reStructuredText: http://docutils.sourceforge.net/rst.html

.. _smartypants: http://pypi.python.org/pypi/smartypants
.. _lnkckr: https://bitbucket.org/livibetter/lnkckr


Services and Handlers
=====================

A *Service* is a blogging platform, such as Blogger or WordPress. For supported
services, see :mod:`bpy.services`.

A *Handler* handles the processing of markup language. For supported handlers,
see :mod:`bpy.handlers`.
