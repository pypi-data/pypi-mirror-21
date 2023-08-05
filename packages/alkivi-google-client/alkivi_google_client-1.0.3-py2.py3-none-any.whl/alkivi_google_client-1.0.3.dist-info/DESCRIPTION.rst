python-alkivi-google-client
===========================

|Build Status| |Requirements Status|

Google python client used at Alkivi

Package
-------

Example

.. code:: python

    from alkivi.google import client as google
    import logging

    scope = 'https://www.googleapis.com/auth/admin.directory.user.readonly'

    # Using default configuration
    google_client = google.Client(scopes=[scope])

    # Using specific endpoint
    google_client = google.Client(endpoint='account2')

    # Get directory client for Admin SDK api
    impersonate = 'toto@alkivi.fr'
    directory_client = google_client.get_directory_client(impersonate)

    # Get a gmail client for gmail API
    gmail_client = google_client.get_gmail_client()

Credentials
-----------

Credentials are fetched from, in priority order: - ./google.conf (script
directory) - $HOME/.google.conf - /etc/google.conf

Example

.. code:: ini

    [default]
    ; general configuration: default endpoint
    endpoint=account1

    [account1]
    ; configuration specific to 'account1' endpoint
    ; using can be 
    ; - service: for Service Account
    ; - oauth: for OAuth authentification
    using=service

    ; for Service Account
    service_account_key=/path/to_your_service_key.json

    [account2]
    ; other account configuration
    using=oauth

    ; for OAuth
    client_id=your_client_id
    client_secret=your_client_secret
    refresh_token=your_refresh_token

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

.. |Build Status| image:: https://travis-ci.org/alkivi-sas/python-alkivi-google-client.svg?branch=master
   :target: https://travis-ci.org/alkivi-sas/python-alkivi-google-client
.. |Requirements Status| image:: https://requires.io/github/alkivi-sas/python-alkivi-google-client/requirements.svg?branch=master
   :target: https://requires.io/github/alkivi-sas/python-alkivi-google-client/requirements/?branch=master


