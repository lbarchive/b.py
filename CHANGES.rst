=======
CHANGES
=======

Version 0.11.0 (2016-02-26T06:04:23Z)
=====================================

* require to provide OAuth client ID and secret

Version 0.10.1 (2016-01-31T23:01:48Z)
=====================================

* fix missing ``labels`` header causing exception for WordPress service
* add note about ``$HOME/.local/bin`` in ``$PATH`` for user scheme installation

Version 0.10.0 (2015-06-30T19:13:44Z)
=====================================

* fix ``UnicodeDecodeError`` when filename with Unicode characters
* add ``-d``/``--debug`` for debugging messages
* show warning about ``stdout`` encoding not ``UTF-*``, and set ``errors`` to ``replace``

Version 0.9.1 (2015-05-28T20:17:33Z)
====================================

* fix Blogger authentication warning on the deprecation of ``oauth2client.tools.run`` by switching_ to ``run_flow``.

  .. _switching: https://github.com/pydata/pandas/issues/8327#issuecomment-97282417

Version 0.9.0 (2014-09-09T03:06:03Z)
====================================

* Makefile

  * fix ``doc`` for ``CHANGES.rst`` prerequisite

* add ``embed_images`` configuration option to embed image files via data URI
  scheme for all but text handler (pull request #2, by Adam Kemp)

  * skip ``http``, ``https``, and ``data`` schemes
  * if file not found, a message is printed out, rendered HTML tag is kept
    untouched
  * related doctest and unittest tests are added, testing ``embed_images``
    function and with ``generate``, if with text handler, it will raise
    ``RuntimeError`` or treat ``img`` tag as plain text, respectively
  * ``BaseHandler`` has class attribute ``SUPPORT_EMBED_IMAGES`` for subclass
    to turn off the support as text handler utilizing it

Version 0.8.0 (2014-08-26T12:17:09Z)
====================================

* Makefile

  + add ``test_doc8`` for doc8 test
  + add ``test_isort`` for import style check

  * rename target ``install_test`` to ``test_setup``
  * target ``test_setup``

    + add test for packages build
    + add test for ``LC_ALL=C``

+ add Python Wheel to build process

* add Blogger page draft support (#15)

  also simplify the post draft, both post and page use publish and revert
  action to update post or page for the draft status

Version 0.7.0 (2013-10-17T03:31:14Z)
====================================

* add documentation generation
* setup.py

  + add ``build_sphinx`` and ``upload_sphinx`` commands

* Makefile

  + add ``doc`` for documentation generation
  + add ``upload_doc`` for uploading to PyPI
  + add ``clean`` for cleaning up built files

* add Blogger page support (#1)
* add Blogger post draft support (#2)

  #2 is split, #15 created for page kind, which doesn't have same draft setting
  support as post kind.

Version 0.6.2 (2013-08-18T11:51:37Z)
====================================

* add test, test_pep0, test_pyflakes test_test (unittest), install_test
  Makefile targets
* update for smartypants >= 1.8.0

Version 0.6.1 (2013-08-14T07:41:25Z)
====================================

* remove smartypants Python 3 exception, which now supports Python 3 since
  v1.7.1

Version 0.6.0 (2013-08-07T21:40:36Z)
====================================

* Port to Python 3, use Unicode in Python 2
* Modularize Blogger API use, new services for adding new services
* Add ``service_options`` to rc:

  The options for a service can be specified using ``service_options`` which is
  a ``dict``. Previous ``blog``, now must be assigned within
  ``service_options``, for example:

  .. code:: python

    service = 'blogger'
    service_options = {
      'blog': 12345,
      'other_option': 'other value',
    }

  The options will be supplied when initialize the service.

* Add ``bpy.services.wordpress``

  * Options: ``username`` and ``password``
  * Headers: ``categories`` and ``draft``

* ``service`` will be added to headers

Version 0.5.2 (2013-07-29T03:37:44Z)
====================================

* fix options doesn't get read properly

Version 0.5.1 (2013-07-29T00:49:19Z)
====================================

* fix smartypants isn't optional.
* fix handler import on Windows. (#13)
* fix HTML files generation location on system other than Linux

Version 0.5.0 (2013-07-25T02:55:42Z)
====================================

* remove ``client_secrets.json``, now its data is included in code. (#11)
* fix checklink output, use lnkckr's ``print_all()``.

Version 0.4.1 (2013-03-31T14:02:39Z)
====================================

* add ``do_search`` for very simple search command
* add ``--version`` option
* fix unclear message, NameError on ``CLIENT_SECRETS``, when
  ``client_secrets.json`` isn't in the search path. (#10)

Version 0.4 (2013-02-13T13:33:19Z)
==================================

* add tests for ``register_directive`` and ``register_role`` decorators
* add setup.py pylint command
* add linkcheck command for checking links

Version 0.3.1 (2013-02-09T09:41:19Z)
====================================

* add ``register_directives`` and ``register_roles`` options of rst handler
* remove all existing directives and roles of rst handler

Version 0.3 (2013-02-06T11:31:43Z)
==================================

* fix ``update_source`` cannot handle unicode and utf8 enocded str by ensuring
  everything is utf8 encoded internally
* add Text handler for plain text
* add HTML handler

Version 0.2 (2013-02-02T12:02:10Z)
==================================

* Fix trailing newlines becoming spaces in title
* fix empty label '' in labels array
* Add handler options ``markup_prefix`` and ``markup_suffix``
* Add header and handler option ``id_affix`` to avoid HTML element ID conflict
  across posts
* Add handler for AsciiDoc

Version 0.1.2 (2013-01-18T05:47:16Z)
====================================

* Fix handler rst ``settings_overrides`` not getting updates

Version 0.1.1 (2013-01-17T20:29:46Z)
====================================

* Fix handlers not getting update of options

Version 0.1 (2013-01-17T05:22:54Z)
==================================

* First versioned release
