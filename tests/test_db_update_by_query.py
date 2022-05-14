import json
from copy import deepcopy
from typing import Any
from typing import Dict

import pytest

from pysondb.db import PysonDB
from pysondb.errors import UnknownKeyError


TEST_DATA = {
    'version': 2,
    'keys': [
        'age',
        'name',
        'place'
    ],
    'data': {
        '219520953066905460': {
            'name': 'ad0',
            'age': 0,
            'place': 'US'
        },
        '110180374400879352': {
            'name': 'ad1',
            'age': 1,
            'place': 'US'
        },
        '224980674034561069': {
            'name': 'ad2',
            'age': 74574654,
            'place': 'UK'
        },
        '228563587602913112': {
            'name': 'ad3',
            'age': 3,
            'place': 'UK'
        },
        '167833310760833974': {
            'name': 'ad4',
            'age': 4,
            'place': 'IN'
        }
    }
}


def test_update_by_query(tmpdir):
    final_data: Dict[str, Any] = deepcopy(TEST_DATA)

    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))
    db = PysonDB(f.strpath)

    assert db.update_by_query(
        query=lambda x: x['place'] == 'US',
        new_data={'place': 'AU'}
    ) == ['219520953066905460', '110180374400879352']

    final_data['data']['219520953066905460']['place'] = 'AU'
    final_data['data']['110180374400879352']['place'] = 'AU'

    assert json.loads(f.read()) == final_data


def test_update_by_query_unknown_key_error(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))
    db = PysonDB(f.strpath)

    with pytest.raises(UnknownKeyError):
        db.update_by_query(
            query=lambda x: x['place'] == 'IN',
            new_data={'summer': True}
        )


@pytest.mark.parametrize(
    'query',
    (
        'a',
        [1, 2],
        (1, 3),
        {'1, 3'},
        {'a': 4, 'b': 5}
    )
)
def test_update_by_query_type_error(tmpdir, query):
    f = tmpdir.join('test.json')
    db = PysonDB(f.strpath)

    with pytest.raises(TypeError):
        db.update_by_query(query, {'name': 'ad'})


@pytest.mark.parametrize(
    'data',
    (
        [1, 2],
        1,
        'string',
        (1, 3),
        {1, 3}
    )
)
def test_new_data_type_error(tmpdir, data):
    f = tmpdir.join('test.json')
    db = PysonDB(f.strpath)

    with pytest.raises(TypeError):
        db.update_by_query(lambda _: True, data)
