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

*b.py* can be installed via ``pip``::

  pip install b.py

Or install to user-site, meaning no root required and install at your home
directory::

  pip install --user b.py

To upgrade::

  pip install --upgrade b.py

To uninstall::

  pip uninstall b.py


.. _Dependencies:

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
| AsciiDoc         | AsciiDoc_::                                        | 2      |
|                  |                                                    |        |
|                  |   pip install asciidoc                             |        |
+------------------+----------------------------------------------------+--------+
| HTML             | None                                               | 2 / 3  |
+------------------+----------------------------------------------------+--------+
| Markdown         | Markdown_::                                        | 2 / 3  |
|                  |                                                    |        |
|                  |   pip install markdown                             |        |
+------------------+----------------------------------------------------+--------+
| reStructuredText | reStructuredText_::                                | 2 / 3  |
|                  |                                                    |        |
|                  |   pip install distutils                            |        |
+------------------+----------------------------------------------------+--------+
| Text             | None                                               | 2 / 3  |
+------------------+----------------------------------------------------+--------+
| **Others**                                                                     |
+------------------+----------------------------------------------------+--------+
| lnkckr           | lnkckr_::                                          | 2 / 3  |
|                  |                                                    |        |
|                  |   pip install lnkckr                               |        |
+------------------+----------------------------------------------------+--------+
| smartypants      | smartypants_ >= 1.8.0::                            | 2 / 3  |
|                  |                                                    |        |
|                  |   pip install smartypants                          |        |
+------------------+----------------------------------------------------+--------+
| **Tests**                                                                      |
+------------------+----------------------------------------------------+--------+
| DOC8             | doc8_::                                            | 2 / 3  |
|                  |                                                    |        |
|                  |   pip install doc8                                 |        |
+------------------+----------------------------------------------------+--------+
| isort            | isort_::                                           | 2 / 3  |
|                  |                                                    |        |
|                  |   pip install isort                                |        |
+------------------+----------------------------------------------------+--------+
| PEP8             | pep8_::                                            | 2 / 3  |
|                  |                                                    |        |
|                  |   pip install pep8                                 |        |
+------------------+----------------------------------------------------+--------+
| Pyflakes         | pyflakes_::                                        | 2 / 3  |
|                  |                                                    |        |
|                  |   pip install pyflakes                             |        |
+------------------+----------------------------------------------------+--------+
| Pylint           | pylint_::                                          | 2 / 3  |
|                  |                                                    |        |
|                  |   pip install pylint                               |        |
+------------------+----------------------------------------------------+--------+
| install\_test    | * virtualenv_::                                    | 2 / 3  |
|                  |                                                    |        |
|                  |     pip install pylint                             |        |
|                  |                                                    |        |
|                  | * make                                             |        |
+------------------+----------------------------------------------------+--------+

__ https://developers.google.com/blogger/docs/3.0/api-lib/python
.. _python-wordpress-xmlrpc: https://github.com/maxcutler/python-wordpress-xmlrpc

.. _AsciiDoc: http://www.methods.co.nz/asciidoc/
.. _Markdown: http://pypi.python.org/pypi/Markdown
.. _reStructuredText: http://docutils.sourceforge.net/rst.html

.. _smartypants: http://pypi.python.org/pypi/smartypants
.. _lnkckr: https://bitbucket.org/livibetter/lnkckr

.. _doc8: https://pypi.python.org/pypi/doc8
.. _isort: https://pypi.python.org/pypi/isort
.. _pep8: https://pypi.python.org/pypi/pep8
.. _pyflakes: https://pypi.python.org/pypi/pyflakes
.. _pylint: https://pypi.python.org/pypi/pylint
.. _virtualenv: https://pypi.python.org/pypi/virtualenv


Services and Handlers
=====================

A *Service* is a blogging platform, such as Blogger or WordPress. For supported
services, see :mod:`bpy.services`.

A *Handler* handles the processing of markup language. For supported handlers,
see :mod:`bpy.handlers`.
