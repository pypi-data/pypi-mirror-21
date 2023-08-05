python-logmein-api-client
=========================

|Build Status| |Requirements Status|

LogMeIn API python client.

Package
-------

Example

.. code:: python

    from logmeinapi import client as logmein

    # Using default configuration
    client = logmein.Client()

    # Using specific endpoint
    client = logmein.Client(endpoint='toto')

Credentials
-----------

Credentials are fetched from, in priority order: - ./logmein.conf
(script directory) - $HOME/.logmein.conf - /etc/logmein.conf

Example

.. code:: ini

    [default]
    ; general configuration: default endpoint
    endpoint=account

    [account1]
    ; configuration specific to 'account1' endpoint
    companyId=1234
    psk=abcde

    [account2]
    ; other configuration
    companyId=4321
    psk=abcde

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

.. |Build Status| image:: https://travis-ci.org/alkivi-sas/python-logmein-api-client.svg?branch=master
   :target: https://travis-ci.org/alkivi-sas/python-logmein-api-client
.. |Requirements Status| image:: https://requires.io/github/alkivi-sas/python-logmein-api-client/requirements.svg?branch=master
   :target: https://requires.io/github/alkivi-sas/python-logmein-api-client/requirements/?branch=master


