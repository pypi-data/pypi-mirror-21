python-alkivi-odoo-client
=========================

|Build Status| |Requirements Status|

Odoo python client used at Alkivi. Based on odoorpc on which we add
additional fonction.

Package
-------

Example

.. code:: python

    from alkivi.odoo import client as odoo

    # Using default configuration
    client = odoo.Client()

    # Using specific endpoint
    client = odoo.Client(endpoint='prod')
    # TODO

Credentials
-----------

Credentials are fetched from, in priority order: - ./odoo.conf (script
directory) - $HOME/.odoo.conf - /etc/odoo.conf

Example

.. code:: ini

    [default]
    ; general configuration: default endpoint
    endpoint=dev

    [dev]
    ; configuration specific to 'dev' endpoint
    protocol=jsonrpc+ssl
    port=443
    url=odoo.domain
    version=8.0
    db=odooDatabase
    user=pdooUser
    password=AweSomePasswOrd

    [prod]
    ; other configuration

Tests
-----

Testing is set up using `pytest <http://pytest.org>`__ and coverage is
handled with the pytest-cov plugin.

Run your tests with ``py.test`` in the root directory.

Coverage is ran by default and is set in the ``pytest.ini`` file. To see
an html output of coverage open ``htmlcov/index.html`` after running the
tests.

TODO

Travis CI
---------

There is a ``.travis.yml`` file that is set up to run your tests for
python 2.7 and python 3.2, should you choose to use it.

TODO

.. |Build Status| image:: https://travis-ci.org/alkivi-sas/python-alkivi-odoo-client.svg?branch=master
   :target: https://travis-ci.org/alkivi-sas/python-alkivi-odoo-client
.. |Requirements Status| image:: https://requires.io/github/alkivi-sas/python-alkivi-odoo-client/requirements.svg?branch=master
   :target: https://requires.io/github/alkivi-sas/python-alkivi-odoo-client/requirements/?branch=master


