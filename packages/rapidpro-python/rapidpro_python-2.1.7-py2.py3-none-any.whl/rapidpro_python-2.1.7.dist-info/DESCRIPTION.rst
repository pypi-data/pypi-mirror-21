RapidPro Python Client
======================

|Build Status| |Coverage Status| |PyPI Release|

Official Python client library for the
`RapidPro <http://rapidpro.github.io/rapidpro/>`__. Supports latest
Python 2 and 3.

Visit `here <http://rapidpro-python.readthedocs.org/>`__ for complete
documentation.

Installation
------------

::

    pip install rapidpro-python

Example
-------

.. code:: python

    from temba_client.v2 import TembaClient
    client = TembaClient('rapidpro.io', 'your-api-token')
    for contact in client.get_contacts(group='Reporters').iterfetches(retry_on_rate_exceed=True):
        print(contact.name)

If you don't know your API token then visit the `API
Explorer <http://rapidpro.io/api/v2/explorer>`__

Development
-----------

For discussions about future development, see the `RapidPro Developers
Group <https://groups.google.com/forum/#!forum/rapidpro-dev>`__.

To run the tests:

::

    nosetests --with-coverage --cover-erase --cover-package=temba_client --cover-html

.. |Build Status| image:: https://travis-ci.org/rapidpro/rapidpro-python.svg?branch=master
   :target: https://travis-ci.org/rapidpro/rapidpro-python
.. |Coverage Status| image:: https://coveralls.io/repos/github/rapidpro/rapidpro-python/badge.svg?branch=master
   :target: https://coveralls.io/github/rapidpro/rapidpro-python
.. |PyPI Release| image:: https://img.shields.io/pypi/v/rapidpro-python.svg
   :target: https://pypi.python.org/pypi/rapidpro-python/


