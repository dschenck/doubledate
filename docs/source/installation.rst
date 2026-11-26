Installation
============
.. include:: ../fragments/badges.rst

:code:`doubledate` is hosted on `PyPI <https://pypi.org/project/doubledate/>`_ and requires
Python 3.11 or later. You can install it using pip:

::

    $ pip install doubledate

or, with `uv <https://docs.astral.sh/uv/>`_:

::

    $ uv add doubledate

Upgrading :code:`doubledate` is just as simple with pip:

::

    $ pip install doubledate --upgrade

Installing a specific version of :code:`doubledate`:

::

    $ pip install doubledate==0.1.0

Dependencies
-------------------------
:code:`doubledate` has the following 2 dependencies:

- `sortedcontainers <https://grantjenks.com/docs/sortedcontainers/>`_
- `python-dateutil <https://dateutil.readthedocs.io/en/stable/>`_

Dependencies are automatically installed with :code:`doubledate`, but can also be installed manually:

::

    $ pip install python-dateutil sortedcontainers
