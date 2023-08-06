asyncio client library for elasticsearch
=========================================

**aioes** is a asyncio_ compatible library for working with Elasticsearch_

.. image:: https://travis-ci.org/aio-libs/aioes.svg?branch=master
   :target: https://travis-ci.org/aio-libs/aioes


.. image:: https://codecov.io/gh/aio-libs/aioes/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/aio-libs/aioes

Documentation
-------------

Read **aioes** documentation on Read The Docs: http://aioes.readthedocs.io/

Example
-------

::

    import asyncio
    from aioes import Elasticsearch

    @asyncio.coroutine
    def go():
        es = Elasticsearch(['localhost:9200'])
        ret = yield from es.create(index="my-index",
                                   doc_type="test-type",
                                   id=42,
                                   body={"str": "data",
                                         "int": 1})
        assert (ret == {'_id': '42',
                        '_index': 'my-index',
                        '_type': 'test-type',
                        '_version': 1,
                        'ok': True})

        answer = yield from es.get(index="my-index",
                                   doc_type="test-type",
                                   id=42)
        assert answer['_source'] == {'str': 'data', 'int': 1}

    loop = asyncio.get_event_loop()
    loop.run_until_complete(go())


Requirements
------------

* Python_ 3.3+
* asyncio_ or Python 3.4+
* aiohttp_ 1.3+


Tests
-----

Make sure you have an instance of Elasticsearch running on port 9200
before executing the tests.

In order for all tests to work you need to add the following lines in the
``config/elasticsearch.yml`` configuration file:

Enable groovy scripts::

  script.groovy.sandbox.enabled: true

Set a repository path::

  path.repo: ["/tmp"]


The test suite uses `py.test`, simply run::

  $ py.test


License
-------

aioes is offered under the BSD license.

.. _python: https://www.python.org/downloads/
.. _asyncio: https://pypi.python.org/pypi/asyncio
.. _aiohttp: https://pypi.python.org/pypi/aiohttp
.. _Elasticsearch: http://www.elasticsearch.org/

CHANGES
-------

0.7.2 (2017-04-19)
^^^^^^^^^^^^^^^^^^

* Allow custom ``Connector`` in ``Transport``: #138, #137.

* Several typos in documentation fixed.


0.7.0 (2017-03-29)
^^^^^^^^^^^^^^^^^^

* Fix Elasticsearch 5.x compatibility issues: #48, #72, #112, #73, #123.

* Add ``stored_fields`` to ``mget``, ``search`` and ``explain`` methods (#123).

* Add ``wait_for_no_relocating_shards`` parameter in ``health`` (#123).

* Add ``filter``, ``token_filter``, ``char_filter`` params in ``analyze`` (#123).

* Add ``force_merge`` method (renamed ``optimize``) (#123).

* Add ignore_idle_threads param in hot_threads #123.

* Update project dependencies.

* Convert tests to pytest.


0.6.1 (2016-09-08)
^^^^^^^^^^^^^^^^^^

* Accept bytes as payload #42

* Convert `Elasticsearch.close()` into a coroutine.

0.6.0 (2016-09-08)
^^^^^^^^^^^^^^^^^^

* Add support for verify_ssl #43

0.5.0 (2016-07-16)
^^^^^^^^^^^^^^^^^^

* Allow scheme, username and password in connections #40


0.4.0 (2016-02-10)
^^^^^^^^^^^^^^^^^^

* Fix ES2+ compatibility in transport address regex #38

0.3.0 (2016-01-27)
^^^^^^^^^^^^^^^^^^

* Use aiohttp.ClientSession internally #36

0.2.0 (2015-10-08)
^^^^^^^^^^^^^^^^^^

* Make compatible with Elasticsearch 1.7

* Support Python 3.5

* Drop Python 3.3 support

* Relicense under Apache 2


0.1.0 (2014-10-04)
^^^^^^^^^^^^^^^^^^

* Initial release

