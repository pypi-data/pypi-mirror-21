Flarecast Utils
===============

|Latest Version| |Development Status| |Python Versions|

Flarecast Utils combine some tools which you can use to develop your
application for the flarecast infrastructure.

Property-DB Client
------------------

Example
~~~~~~~

.. code:: python

    client = PropertyDBClient(PROPERTY_DB_REST_ADDRESS)
    payload = []

    payload.append({'test':'hello'})
    result = client.insert_property_group(dataset=DATASET,
                                          property_group_type=property_group_type,
                                          body=payload)

Global Config Loader
--------------------

Example
~~~~~~~

Load configuration
^^^^^^^^^^^^^^^^^^

.. code:: python

    # load configuration
    globalconfig = GlobalConfig('config url')
    globalconfig.load()

Use configuration
^^^^^^^^^^^^^^^^^

.. code:: python

    self.__pg = PostgresNoSQLClient("db",
                                            port=5432,
                                            user=globalconfig.DB_USER,
                                            password=globalconfig.DB_PASSWORD)

.. |Latest Version| image:: https://img.shields.io/pypi/v/flarecast-utils.svg
   :target: https://pypi.python.org/pypi?:action=display&name=flarecast-utils
.. |Development Status| image:: https://img.shields.io/pypi/status/flarecast-utils.svg
   :target: https://dev.flarecast.eu/stash/projects/INFRA/repos/utils/browse
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/flarecast-utils.svg
   :target: https://dev.flarecast.eu/stash/projects/INFRA/repos/utils/browse


