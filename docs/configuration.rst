=============
Configuration
=============

.. _brc.py:

``brc.py``
==========

``brc.py`` is the configuration that :doc:`b.py` reads from the current working
directory, it may look like:

.. code:: python

  service = '<service id>'
  service_options = {
    # see below
  }

  # Normally, you only need settings above.
  # For customized handlers and services, you can specify:

  handlers = {
    # see below
  }

  services = {
    # see below
  }

A normal ``brc.py`` only needs ``service`` and ``service_options``, but you can
add customized handlers and services.

.. seealso:: :ref:`Service options <service-options>`

.. seealso:: :ref:`Writing a custom handler <custom-handler>`

.. seealso:: :ref:`Writing a custom service <custom-service>`
