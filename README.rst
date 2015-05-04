========
betweeen
========

.. image:: https://pypip.in/v/betweeen/badge.png?style=flat
    :target: https://pypi.python.org/pypi/betweeen

.. image:: https://pypip.in/d/betweeen/badge.png?style=flat
    :target: https://pypi.python.org/pypi/betweeen

.. image:: https://pypip.in/status/betweeen/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/betweeen

.. image:: https://pypip.in/license/betweeen/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/betweeen

`Between <https://between.us/?lang=en>`__) of `VCNC <https://between.us/about>`__ for Python.


Installation
============

To install betweeen, simply: 

.. code-block:: console

    $ pip install betweeen

Or, you can use:

.. code-block:: console

    $ pip install betweeen

Or, you can also install manually:

.. code-block:: console

    $ git clone git://github.com/carpedm20/betweeen.git
    $ cd betweeen
    $ python setup.py install


Echo bot example
================

.. code-block:: console

    import betweeen

    client = betweeen.Client("YOUR_ID", "YOUR_PASSWORD")
    for op in client.listen():
         client.sendMessage(op.message, op.sender)


Authors
=======

Taehoon Kim / `@carpedm20 <http://carpedm20.github.io/about/>`__
