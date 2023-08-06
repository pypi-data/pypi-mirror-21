import asyncio
import pytest
from unittest import mock

from aioes import Elasticsearch
from aioes.exception import (
    NotFoundError,
    RequestError,
    TransportError,
    )


MESSAGES = [
    {
        "user": "Johny Mnemonic",
        "birthDate": "2109-11-15T14:12:12",
        "message": "trying out Elasticsearch",
        "skills": ["Python", "PHP", "HTML", "C++", ".NET", "JavaScript"],
        "counter": 0
    },
    {
        "user": "Sidor Spiridonovich",
        "birthDate": "2009-01-11T11:02:11",
        "message": "trying in Elasticsearch",
        "skills": ["Java", "1C", "C++", ".NET", "JavaScript"],
        "counter": 0
    },
    {
        "user": "Fedor Poligrafovich",
        "birthDate": "1969-12-15T14:12:12",
        "message": "trying out everything",
        "skills": ["MODULA", "ADA", "PLM", "BASIC", "Python"],
        "counter": 0
    },
    {
        "user": "Super",
        "birthDate": "1912-11-15T14:12:12",
        "message": "trying out ssdff  everything",
        "skills": ["MODULA", "ADA", "PLM", "BASIC", "Python"],
        "counter": 10
    },
]

INDEX = 'test_elasticsearch'


@asyncio.coroutine
def test_ping(client):
    """ ping """

    class R:
        @asyncio.coroutine
        def perform_request(self, a, b):
            yield
            raise TransportError

        def close(self):
            pass

    data = yield from client.ping()
    assert data
    client._transport = R()
    yield from client.ping()


@asyncio.coroutine
def test_info(client):
    """ test_info """
    data = yield from client.info()
    assert data['cluster_name'] == 'elasticsearch'


@asyncio.coroutine
def test_create(client):
    """ create index """
    data = yield from client.create(
        INDEX, 'tweet',
        {
            'user': 'Bob',
            'skills': ['C', 'Python', 'Assembler'],
            'date': '2009-11-15T14:12:12'
        },
        '1',
        routing='Bob')
    assert data['_index'] == INDEX
    assert data['_type'] == 'tweet'
    assert data['_version'] == 1
    assert data['created']
    # test for conflict (BROKEN)
    # with pytest.raises(ConflictError):
    #     yield from client.create(index, 'tweet', {}, '1')


@asyncio.coroutine
def test_index(client):
    """ auto-create index """
    data = yield from client.index(INDEX, 'tweet', {}, '1')
    assert data['_index'] == INDEX
    assert data['_type'] == 'tweet'
    assert data['_id'] == '1'
    assert data['_version'] == 1
    assert data['created']
    # test increment version
    data = yield from client.index(INDEX, 'tweet', {}, '1')
    assert data['_version'] == 2
    assert not data['created']


@pytest.mark.es_tag(max=(2, 4))
@asyncio.coroutine
def test_index__external_version(client):
    data = yield from client.index(INDEX, 'tweet', {}, '12',
                                   version_type='external',
                                   version=122,
                                   timestamp='2009-11-15T14:12:12',
                                   ttl='1d',
                                   consistency='one',
                                   timeout='5m',
                                   refresh=True,
                                   replication='async')
    assert data['_version'] == 122
    assert data['created']


@pytest.mark.es_tag(min=(5, 0))
@asyncio.coroutine
def test_index__external_version_2(client):
    data = yield from client.index(INDEX, 'tweet', {}, '12',
                                   version_type='external',
                                   version=122,
                                   timestamp='2009-11-15T14:12:12',
                                   ttl='1d',
                                   timeout='5m',
                                   refresh=True,
                                   )
    assert data['_version'] == 122
    assert data['created']


@pytest.mark.parametrize('exc,kwargs', [
    (RequestError, dict(parent='1', percolate='')),
    (TypeError, dict(consistency=1)),
    (ValueError, dict(consistency='1')),
    (TypeError, dict(replication=1)),
    (ValueError, dict(replication='1')),
    (TypeError, dict(op_type=1)),
    (ValueError, dict(op_type='1')),
    (TypeError, dict(version_type=1)),
    (ValueError, dict(version_type='1')),
    ])
@asyncio.coroutine
def test_index__errors(client, exc, kwargs):
    with pytest.raises(exc):
        assert (yield from client.index(INDEX, 'type', {}, **kwargs)) is None


@pytest.mark.es_tag(min=(5, 0))
@pytest.mark.parametrize('deprecated', [
    dict(consistency='one'),
    dict(replication='async'),
    ], ids=repr)
@asyncio.coroutine
def test_index__deprecated_params(client, deprecated):
    with pytest.raises(RequestError):
        assert (yield from client.index(INDEX, 'tweet', {}, '12',
                                        **deprecated)) is None


@asyncio.coroutine
def test_exist(client):
    """ exists """
    id = '100'
    # test non-exist
    data = yield from client.exists(INDEX, id,
                                    refresh=True,
                                    realtime=True,
                                    preference='_local')
    assert not data
    # test exist
    yield from client.index(INDEX, 'exist',
                            {'user': 'opa', 'tim': 'none'},
                            id,
                            routing='opa')
    data = yield from client.exists(INDEX, id,
                                    routing='opa')
    assert data
    data = yield from client.exists(INDEX, id, parent='1')
    assert not data


@asyncio.coroutine
def test_get(client):
    """ get """
    id = '200'
    yield from client.index(INDEX, 'test_get', MESSAGES[1], id)
    data = yield from client.get(INDEX, id,
                                 realtime=True,
                                 refresh=True)
    assert data['_id'] == id
    assert data['_index'] == INDEX
    assert data['_type'] == 'test_get'
    assert data['_version'] == 1
    assert data['found']
    assert data['_source'] == MESSAGES[1]
    data = yield from client.get(INDEX, id,
                                 _source=False)
    assert '_source' not in data
    data = yield from client.get(INDEX, id,
                                 _source_exclude='counter',
                                 _source_include='*')
    assert 'counter' not in data
    with pytest.raises(NotFoundError):
        yield from client.get(INDEX, id, parent='1')
    with pytest.raises(TypeError):
        yield from client.get(INDEX, id,
                              version_type=1)
    with pytest.raises(ValueError):
        yield from client.get(INDEX, id,
                              version_type='1')


@pytest.mark.es_tag(
    max=(2, 4),
    reason="version & version_type are not in 5.2")
@asyncio.coroutine
def test_get_source(client):
    """ get_source """
    yield from client.index(INDEX,
                            'test_get_source',
                            MESSAGES[0],
                            '1')
    data = yield from client.get_source(INDEX, '1')
    assert data == MESSAGES[0]
    data = yield from client.get_source(INDEX, '1', refresh=1)
    assert data == MESSAGES[0]
    data = yield from client.get_source(INDEX, '1', refresh=False)
    assert data == MESSAGES[0]

    id = '200'
    yield from client.index(
        INDEX, 'test_get_source', MESSAGES[2], id,
        routing='Poligrafovich', refresh=True,
        )
    data = yield from client.get_source(INDEX, id,
                                        routing='Poligrafovich',
                                        preference='_local',
                                        version=1,
                                        version_type='internal',
                                        realtime=True,
                                        refresh=True)
    assert data == MESSAGES[2]
    data = yield from client.get_source(INDEX, id,
                                        routing='Poligrafovich',
                                        _source_exclude='counter',
                                        _source_include='*')
    assert 'counter' not in data
    with pytest.raises(NotFoundError):
        yield from client.get_source(INDEX, id, parent='1')
    with pytest.raises(TypeError):
        yield from client.get_source(INDEX, id,
                                     version_type=1)
    with pytest.raises(ValueError):
        yield from client.get_source(INDEX, id,
                                     version_type='1')


@asyncio.coroutine
def test_delete(client, es_tag):
    """ delete """
    yield from client.index(INDEX, 'testdoc', MESSAGES[2], '1')
    data = yield from client.delete(INDEX, 'testdoc', '1')
    assert data['found']

    if es_tag < (5, 0):
        kwargs = dict(consistency='one',
                      replication='async')
    else:
        kwargs = dict()
    with pytest.raises(NotFoundError):
        data = yield from client.delete(INDEX, 'testdoc', '1',
                                        refresh=True,
                                        timeout='5m',
                                        routing='test',
                                        parent='1',
                                        **kwargs)


@pytest.mark.parametrize('exc,kwargs', [
    (TypeError, dict(consistency=1)),
    (ValueError, dict(consistency='1')),
    (TypeError, dict(replication=1)),
    (ValueError, dict(replication='1')),
    (TypeError, dict(version_type=1)),
    (ValueError, dict(version_type='1')),
])
@asyncio.coroutine
def test_delete__errors(client, exc, kwargs):
    with pytest.raises(exc):
        yield from client.delete(INDEX, 'type', {}, **kwargs)


@asyncio.coroutine
def test_update(client, es_tag):
    """ update """
    script = {
        "doc": {
            "counter": 123
        }
    }
    yield from client.index(INDEX, 'testdoc', MESSAGES[2],
                            '1',
                            routing='Fedor')
    yield from client.update(INDEX, 'testdoc', '1',
                             script,
                             version_type='internal',
                             version=1,
                             routing='Fedor')
    data = yield from client.get(INDEX, '1', routing='Fedor')
    assert data['_source']['counter'] == 123
    assert data['_version'] == 2

    if es_tag < (5, 0):
        kwargs = dict(consistency='one',
                      replication='async',
                      lang='en',
                      )
    else:
        kwargs = dict()
    data = yield from client.update(INDEX, 'testdoc', '1',
                                    script,
                                    timestamp='2009-11-15T14:12:12',
                                    ttl='1d',
                                    timeout='5m',
                                    refresh=True,
                                    retry_on_conflict=2,
                                    routing='Fedor',
                                    **kwargs)


@pytest.mark.es_tag(max=(2, 4))
@asyncio.coroutine
def test_update__not_found(client):
    with pytest.raises(NotFoundError):
        yield from client.update(
            INDEX, 'testdoc', '1',
            script='{}',
            fields='user',
            parent='1')


@pytest.mark.parametrize('exc,kwargs', [
    (TypeError, dict(consistency=1)),
    (ValueError, dict(consistency='1')),
    (TypeError, dict(replication=1)),
    (ValueError, dict(replication='1')),
    (TypeError, dict(version_type=1)),
    (ValueError, dict(version_type='1')),
])
@asyncio.coroutine
def test_update__errors(client, exc, kwargs):
    with pytest.raises(exc):
        assert (yield from client.update(
            INDEX, 'type', {}, **kwargs)) is None


@asyncio.coroutine
def test_search(client, es_tag):
    """ search """
    yield from client.index(INDEX, 'testdoc',
                            MESSAGES[0], '1',
                            refresh=True)
    yield from client.index(INDEX, 'testdoc',
                            MESSAGES[1], '2',
                            refresh=True)
    yield from client.index(INDEX, 'testdoc',
                            MESSAGES[2], '3',
                            refresh=True)
    data = yield from client.search(INDEX,
                                    'testdoc',
                                    q='skills:Python')
    assert data['hits']['total'] == 2
    assert 'skills' in data['hits']['hits'][0]['_source']
    assert 'skills' in data['hits']['hits'][1]['_source']

    if es_tag > (5, 0):
        kwargs = dict(stored_fields='skills,user')
    else:
        kwargs = dict(fields='skills,user',
                      lowercase_expanded_terms=True)

    data = yield from client.search(INDEX,
                                    'testdoc',
                                    q='skills:Python',
                                    _source_exclude='skills',
                                    analyzer='standard',
                                    default_operator='AND',
                                    analyze_wildcard=True,
                                    version=2,
                                    timeout='5m',
                                    allow_no_indices=True,
                                    ignore_unavailable=True,
                                    df='_all',
                                    explain=True,
                                    from_=0,
                                    expand_wildcards='open',
                                    lenient=True,
                                    preference='random',
                                    scroll='1s',
                                    search_type='query_then_fetch',
                                    size=100,
                                    sort='user:true',
                                    stats=True,
                                    **kwargs)
    assert 'skills' not in data['hits']['hits'][0]['_source']
    assert 'skills' not in data['hits']['hits'][1]['_source']
    with pytest.raises(TypeError):
        yield from client.search(default_operator=1,
                                 indices_boost=False)
    with pytest.raises(ValueError):
        yield from client.search(doc_type='testdoc',
                                 q='skills:Python',
                                 routing='Sidor',
                                 source='Query DSL',
                                 suggest_field='user',
                                 suggest_text='test',
                                 suggest_mode='missing',
                                 suggest_size=100,
                                 default_operator='1')

    with pytest.raises(TypeError):
        yield from client.search(INDEX,
                                 'testdoc',
                                 q='skills:Python',
                                 suggest_mode=1)
    with pytest.raises(ValueError):
        yield from client.search(INDEX,
                                 'testdoc',
                                 q='skills:Python',
                                 suggest_mode='1')

    with pytest.raises(TypeError):
        yield from client.search(INDEX,
                                 'testdoc',
                                 q='skills:Python',
                                 search_type=1)
    with pytest.raises(ValueError):
        yield from client.search(INDEX,
                                 'testdoc',
                                 q='skills:Python',
                                 search_type='1')

    with pytest.raises(TypeError):
        yield from client.search(INDEX,
                                 'testdoc',
                                 q='skills:Python',
                                 expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.search(INDEX,
                                 'testdoc',
                                 q='skills:Python',
                                 expand_wildcards='1')


@pytest.mark.es_tag(min=(2, 0), reason='fails on 1.7, bad test')
@asyncio.coroutine
def test_count(client):
    """ count """
    yield from client.index(INDEX, 'testdoc',
                            MESSAGES[0], '1',
                            refresh=True)
    yield from client.index(INDEX, 'testdoc',
                            MESSAGES[1], '2',
                            refresh=True)
    yield from client.index(INDEX, 'testdoc',
                            MESSAGES[2], '3',
                            refresh=True)
    data = yield from client.count(
        INDEX, 'testdoc', q='skills:Python')
    assert data['count'] == 2
    data = yield from client.count(
        INDEX, 'testdoc', q='skills:Python',
        ignore_unavailable=True,
        expand_wildcards='open',
        allow_no_indices=False,
        min_score=1,
        preference='random')
    assert data['count'] == 0

    with pytest.raises(TypeError):
        yield from client.count(
            INDEX, 'testdoc',
            expand_wildcards=1)

    with pytest.raises(ValueError):
        yield from client.count(
            INDEX, 'testdoc', q='skills:Python',
            expand_wildcards='1',
            routing='Sidor',
            source='Query DSL')


@asyncio.coroutine
def test_explain(client, es_tag):
    """ explain """
    yield from client.index(INDEX, 'testdoc',
                            MESSAGES[0], '1',
                            refresh=True)
    yield from client.index(INDEX, 'testdoc',
                            MESSAGES[1], '2',
                            refresh=True)
    yield from client.index(INDEX, 'testdoc',
                            MESSAGES[2], '3',
                            refresh=True)

    data = yield from client.explain(
        INDEX, 'testdoc', '3',
        q='skills:Python')
    assert data['matched']

    if es_tag > (5, 0):
        kwargs = dict(stored_fields='user,counter')
    else:
        kwargs = dict(fields='user,counter',
                      lowercase_expanded_terms=False,
                      )

    data = yield from client.explain(
        INDEX, 'testdoc', '1',
        q='skills:Python',
        analyze_wildcard=True,
        _source=False,
        _source_include='user',
        _source_exclude='counter',
        analyzer='standard',
        default_operator='and',
        df='_all',
        lenient=True,
        preference='random',
        **kwargs)
    assert data['matched']

    with pytest.raises(TypeError):
        yield from client.explain(
            INDEX, 'testdoc', '1',
            q='skills:Python',
            default_operator=1)
    with pytest.raises(ValueError):
        yield from client.explain(
            INDEX, 'testdoc', '1',
            default_operator='1',
            parent='2',
            routing='Sidor',
            source='DSL Query')


@pytest.mark.xfail
@asyncio.coroutine
def test_delete_by_query(client):
    """ delete_by_query """
    DQ = {"query": {"term": {"user": "Fedor Poligrafovich"}}}

    yield from client.index(INDEX, 'testdoc', MESSAGES[3], '1')
    yield from client.index(INDEX, 'testdoc', MESSAGES[2], '2')
    # data = yield from client.delete(index, 'testdoc', '1')
    # self.assertTrue(data['found'], data)

    data = yield from client.delete_by_query(
        INDEX,
        'testdoc',
        q='user:Fedor Poligrafovich'
    )
    assert '_indices' in data
    with pytest.raises(TransportError):
        yield from client.delete_by_query(
            body=DQ,
            allow_no_indices=True,
            analyzer='standard',
            df='_all',
            expand_wildcards='open',
            consistency='all',
            default_operator='AND',
            ignore_unavailable=True,
            replication='async',
            routing='Fedor',
            source='',
            timeout='100ms')
    with pytest.raises(TypeError):
        yield from client.delete_by_query(default_operator=1)
    with pytest.raises(ValueError):
        yield from client.delete_by_query(default_operator='1')
    with pytest.raises(TypeError):
        yield from client.delete_by_query(consistency=1)
    with pytest.raises(ValueError):
        yield from client.delete_by_query(consistency='1')
    with pytest.raises(TypeError):
        yield from client.delete_by_query(replication=1)
    with pytest.raises(ValueError):
        yield from client.delete_by_query(replication='1')
    with pytest.raises(TypeError):
        yield from client.delete_by_query(expand_wildcards=1)
    with pytest.raises(ValueError):
        yield from client.delete_by_query(expand_wildcards='1')


@asyncio.coroutine
def test_msearch(client, es_tag):
    """ msearch """
    queries = [
        {"_index": INDEX},
        {"query": {"match_all": {}}, "from": 0, "size": 10},
        {"_index": INDEX},
        {"query": {"match_all": {}}}
    ]

    yield from client.index(INDEX, 'testdoc',
                            MESSAGES[0], '1',
                            refresh=True)
    yield from client.index(INDEX, 'testdoc',
                            MESSAGES[1], '2',
                            refresh=True)
    yield from client.index(INDEX, 'testdoc',
                            MESSAGES[2], '3',
                            refresh=True)

    data = yield from client.msearch(queries)
    assert len(data['responses']) > 0
    if es_tag < (5, 0):
        # 'count' is removed in 5.0
        data = yield from client.msearch(queries, search_type='count')
        assert len(data['responses']) > 0


@pytest.mark.parametrize('exc,kwargs', [
    (TypeError, dict(search_type=1)),
    (ValueError, dict(search_type='1')),
])
@asyncio.coroutine
def test_msearch__errors(client, exc, kwargs):
    queries = [
        {"_index": INDEX},
        {"query": {"match_all": {}}, "from": 0, "size": 10},
        {"_index": INDEX},
        {"query": {"match_all": {}}}
    ]
    with pytest.raises(exc):
        assert (yield from client.msearch(queries, **kwargs)) is None


@asyncio.coroutine
def test_bulk(client, es_tag):
    bulks = [
        {"index": {"_index": INDEX, "_type": "type1", "_id": "1"}},
        {"name": "hiq", "age": 10},
        {"index": {"_index": INDEX, "_type": "type1", "_id": "2"}},
        {"name": "hiq", "age": 10},
        {"index": {"_index": INDEX, "_type": "type1", "_id": "3"}},
        {"name": "hiq", "age": 10}
    ]

    data = yield from client.bulk(bulks)
    assert not data['errors']
    assert 3 == len(data['items'])
    if es_tag >= (5, 0):
        kwargs = {}
    else:
        kwargs = dict(consistency='one',
                      replication='async')
    data = yield from client.bulk(
        bulks,
        refresh=True,
        routing='hiq',
        timeout='1s',
        **kwargs
    )
    with pytest.raises(TypeError):
        yield from client.bulk(bulks, consistency=1)
    with pytest.raises(ValueError):
        yield from client.bulk(bulks, consistency='1')
    with pytest.raises(TypeError):
        yield from client.bulk(bulks, replication=1)
    with pytest.raises(ValueError):
        yield from client.bulk(bulks, replication='1')


@asyncio.coroutine
def test_mget(client, es_tag):
    """ mget """
    yield from client.index(
        INDEX, 'testdoc', MESSAGES[0], '1', refresh=True)
    yield from client.index(
        INDEX, 'testdoc', MESSAGES[1], '2', refresh=True)
    yield from client.index(
        INDEX, 'testdoc', MESSAGES[2], '3', refresh=True)
    body = {
        "docs": [
            {"_index": INDEX, "_type": "testdoc", "_id": "1"},
            {"_index": INDEX, "_type": "testdoc", "_id": "2"}
        ]
    }
    data = yield from client.mget(body)
    assert len(data['docs']) == 2
    if es_tag > (5, 0):
        kwargs = dict(stored_fields='user,skills',
                      _source=True)
    else:
        kwargs = dict(fields='user,skills',
                      parent='')
    data = yield from client.mget(
        body,
        _source_exclude='birthDate',
        _source_include='user,skills',
        realtime=True,
        refresh=True,
        preference='random',
        **kwargs
    )
    assert 'docs' in data
    assert len(data) == 1
    doc = data['docs'][0]
    if es_tag < (5, 0):
        assert 'fields' in doc
        assert 'skills' in doc['fields']
        assert 'user' in doc['fields']
        assert 'birthDate' not in doc['fields']
        assert 'message' not in doc['fields']
        assert 'counter' not in doc['fields']
    assert '_source' in doc
    assert 'skills' in doc['_source']
    assert 'user' in doc['_source']
    assert 'birthDate' not in doc['_source']
    assert 'message' not in doc['_source']
    assert 'counter' not in doc['_source']
    # yield from client.mget(body, routing='Sidor')  # XXX?


@asyncio.coroutine
def test_suggest(client):
    """ search """
    mapping = {
        "testdoc": {
            "properties": {
                "birthDate": {
                    "type": "date",
                    "format": "dateOptionalTime"
                },
                "counter": {
                    "type": "long"
                },
                # this one is different
                "message": {
                    "type": "completion"
                },
                "skills": {
                    "type": "string"
                },
                "user": {
                    "type": "string"
                }
            }
        }
    }

    yield from client.indices.create(INDEX)
    yield from client.indices.put_mapping(
        INDEX,
        'testdoc',
        mapping,
    )
    yield from client.index(INDEX, 'testdoc',
                            MESSAGES[0], '1',
                            refresh=True)
    yield from client.index(INDEX, 'testdoc',
                            MESSAGES[1], '2',
                            refresh=True)
    b = {
        "my-suggestion": {
            "text": "trying out",
            "completion": {
                "field": "message"
            }
        }
    }

    data = yield from client.suggest(
        INDEX,
        body=b,
    )
    results = data['my-suggestion'][0]['options']
    assert len(results) == 1
    assert results[0]['text'] == 'trying out Elasticsearch'


@pytest.mark.es_tag(max=(5, 0), reason="Deprecated since 5.0")
@asyncio.coroutine
def test_percolate(client):
    mapping = {
        "testdoc": {
            "properties": {
                "message": {
                    "type": "string"
                }
            }
        }
    }
    yield from client.indices.create(INDEX)
    yield from client.indices.put_mapping(
        INDEX,
        'testdoc',
        mapping,
    )

    percolator = {
        "query": {
            "match": {
                "message": "bonsai tree"
            }
        }
    }
    # register percolator
    yield from client.index(INDEX, '.percolator',
                            percolator, '1',
                            refresh=True)

    b = {
        "doc": {
            "message": "A new bonsai tree in the office"
        }
    }
    # percolate a doc from b
    data = yield from client.percolate(
        INDEX,
        'testdoc',
        body=b,
    )
    assert data['total'] == 1
    assert data['matches'][0] == {'_index': INDEX, '_id': '1'}

    # percolate_count gives only count, no matches
    data = yield from client.count_percolate(
        INDEX,
        'testdoc',
        body=b,
    )

    assert data['total'] == 1
    assert 'matches' not in data


@pytest.mark.es_tag(max=(5, 0), reason="Deprecated in 5.0")
@asyncio.coroutine
def test_mpercolate(client, es_tag):
    if es_tag >= (5, 0):
        mapping = {
            "testdoc": {
                "properties": {
                    "message": {
                        "type": "text"
                    }
                }
            }
        }
    else:
        mapping = {
            "testdoc": {
                "properties": {
                    "message": {
                        "type": "string"
                    }
                }
            }
        }
    yield from client.indices.create(INDEX)
    yield from client.indices.put_mapping(INDEX, 'testdoc', mapping)

    percolator = {
        "query": {
            "match": {
                "message": "bonsai tree"
            }
        }
    }
    # register percolator
    yield from client.index(INDEX, '.percolator',
                            percolator, '1',
                            refresh=True)

    body = [
        {
            'percolate': {
                'index': INDEX,
                'type': 'testdoc',
            }
        },
        {
            "doc": {
                "message": "A new bonsai tree in the office"
            }
        }
    ]

    data = yield from client.mpercolate(body, INDEX, 'testdoc')

    assert len(data['responses']) == 1
    item = data['responses'][0]
    assert item['total'] == 1
    assert item['matches'][0] == {'_index': INDEX, '_id': '1'}


@asyncio.coroutine
def test_termvector(client, es_tag):
    if es_tag > (5, 0):
        mapping = {
            "testdoc": {
                "properties": {
                    "message": {
                        "type": "text",
                        "term_vector": "with_positions_offsets_payloads",
                        "store": True,
                    }
                }
            }
        }
    else:
        mapping = {
            "testdoc": {
                "properties": {
                    "message": {
                        "type": "string",
                        "term_vector": "with_positions_offsets_payloads",
                        "store": True,
                    }
                }
            }
        }
    yield from client.indices.create(INDEX)
    yield from client.indices.put_mapping(INDEX, 'testdoc', mapping)

    doc = {'message': 'Hello world'}
    yield from client.index(INDEX, 'testdoc', doc, '1', refresh=True)

    data = yield from client.termvector(INDEX, 'testdoc', '1')

    vector_data = data['term_vectors']['message']
    assert vector_data['field_statistics'] == {
        "sum_doc_freq": 2,
        "doc_count": 1,
        "sum_ttf": 2
    }
    assert 'hello' in vector_data['terms']
    assert 'world' in vector_data['terms']


@asyncio.coroutine
def test_mtermvectors(client, es_tag):
    if es_tag >= (5, 0):
        mapping = {
            "testdoc": {
                "properties": {
                    "message": {
                        "type": "text",
                        "term_vector": "with_positions_offsets_payloads",
                        "store": True,
                    }
                }
            }
        }
    else:
        mapping = {
            "testdoc": {
                "properties": {
                    "message": {
                        "type": "string",
                        "term_vector": "with_positions_offsets_payloads",
                        "store": True,
                    }
                }
            }
        }
    yield from client.indices.create(INDEX)
    yield from client.indices.put_mapping(INDEX, 'testdoc', mapping)

    doc = {'message': 'Hello world'}

    yield from client.index(INDEX, 'testdoc', doc, '1', refresh=True)

    doc = {'message': 'Second term'}
    yield from client.index(INDEX, 'testdoc', doc, '2', refresh=True)

    data = yield from client.mtermvectors(
        INDEX, 'testdoc', ids='1,2'
    )

    assert len(data['docs']) == 2
    assert 'term_vectors' in data['docs'][0]
    assert 'term_vectors' in data['docs'][1]


@asyncio.coroutine
def test_scripts_management(client):
    script = {'script': 'log(_score * 2)'}

    # adding
    yield from client.put_script('groovy', 'test_script', script)

    # getting and checking
    got_script = yield from client.get_script('groovy', 'test_script')
    assert script['script'] == got_script['script']

    # deleting
    yield from client.delete_script('groovy', 'test_script')
    with pytest.raises(NotFoundError):
        got_script = yield from client.get_script(
            'groovy', 'test_script'
        )


@pytest.mark.xfail
@asyncio.coroutine
def test_scripts_execution(client):
    script = {
        'script': '2*val',
    }
    query = {
        "query": {
            "match": {
                "user": "Johny Mnemonic"
            }
        },
        "script_fields": {
            "test1": {
                "lang": "painless",
                "script_id": "calculate-score",
                "params": {
                    "val": 2,
                }
            }
        }
    }

    yield from client.index(INDEX, 'testdoc',
                            MESSAGES[0], '1',
                            refresh=True)

    yield from client.put_script('groovy', 'calculate-score', script)
    data = yield from client.search(INDEX, 'testdoc', query)
    res = data['hits']['hits'][0]['fields']['test1'][0]
    assert res == 4  # 2*2


@asyncio.coroutine
def test_templates_management(client, es_tag):
    template = {
        "template": {
            "query": {
                "match": {
                    "user": "{{query_string}}"
                }
            }
        }
    }

    yield from client.put_template('test_template', template)

    data = yield from client.get_template('test_template')
    if es_tag >= (5, 0):
        expected = {'lang': 'mustache',
                    '_id': 'test_template',
                    'found': True,
                    'template':
                        '{"query":{"match":{"user":"{{query_string}}"}}}'}
    else:
        expected = {'lang': 'mustache',
                    '_version': mock.ANY,
                    '_id': 'test_template',
                    'found': True,
                    'template':
                        '{"query":{"match":{"user":"{{query_string}}"}}}'}
    assert data == expected

    yield from client.delete_template('test_template')
    with pytest.raises(NotFoundError):
        yield from client.get_template('test_template')


@asyncio.coroutine
def test_template_search(client, es_tag):
        template = {
            "template": {
                "query": {
                    "match": {
                        "user": "{{query_string}}"
                    }
                }
            }
        }
        if es_tag >= (2, 0):
            search_body = {
                "id": "test_template",
                "params": {
                    "query_string": "Johny Mnemonic"
                }
            }
        else:
            search_body = {
                "template": {
                    "id": "test_template"
                },
                "params": {
                    "query_string": "Johny Mnemonic"
                }
            }
        yield from client.index(
            INDEX, 'testdoc', MESSAGES[0], '1',
            refresh=True
        )

        yield from client.put_template('test_template', template)

        data = yield from client.search_template(
            INDEX, 'testdoc', body=search_body
        )
        assert data['hits']['total'] == 1


@asyncio.coroutine
def test_search_shards(client):
    yield from client.index(
        INDEX, 'testdoc', MESSAGES[0], '1',
        refresh=True
    )
    data = yield from client.search_shards(
        INDEX, 'testdoc'
    )
    assert 'nodes' in data
    assert len(data['nodes']) > 0
    assert 'shards' in data
    assert len(data['shards']) > 0


def test__repr__(loop):
    cl = Elasticsearch([], loop=loop)
    assert repr(cl) == '<Elasticsearch [<Transport []>]>'
    cl = Elasticsearch(['localhost:9200'], loop=loop)
    assert repr(cl) == (
        "<Elasticsearch [<Transport ["
        "TCPEndpoint(scheme='http', host='localhost', port=9200)"
        "]>]>")
