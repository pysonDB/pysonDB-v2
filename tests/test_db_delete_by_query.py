import json

import pytest

from pysondb.db import PysonDB


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
            'age': 7,
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


def test_delete_by_query(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))
    db = PysonDB(f.strpath)

    assert db.delete_by_query(
        query=lambda x: x['age'] < 6
    ) == ['219520953066905460', '110180374400879352', '228563587602913112', '167833310760833974']
    assert json.loads(f.read()) == {'version': 2, 'keys': ['age', 'name', 'place'], 'data': {
        '224980674034561069': {'name': 'ad2', 'age': 7, 'place': 'UK'}}}


@pytest.mark.parametrize(
    'query',
    (
        {'a': '4'},
        [1, 2],
        1,
        '2',
        {1, 2}
    )
)
def test_delete_by_query_type_error(tmpdir, query):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))
    db = PysonDB(f.strpath)

    with pytest.raises(TypeError):
        db.delete_by_query(query)
