import json

import pytest

from pysondb.db import PysonDB


TEST_DATA = {
    'version': 2,
    'keys': ['age', 'name'],
    'data': {
        '2352346': {
            'age': 4,
            'name': 'mathew_first'
        },
        '1234567': {
            'age': 9,
            'name': 'new_user'
        }
    }
}


@pytest.mark.parametrize(
    'condition,output',
    (
        (lambda x: x['age'] >= 4, {'2352346': {'age': 4, 'name': 'mathew_first'},
         '1234567': {'age': 9, 'name': 'new_user'}}),
        (lambda x: x['name'] == 'new_user', {
         '1234567': {'age': 9, 'name': 'new_user'}}),
        (lambda x: x['age'] >= 4 and x['name'] == 'mathew_first',
         {'2352346': {'age': 4, 'name': 'mathew_first'}})
    )
)
def test_get_by_query(tmpdir, condition, output):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))
    db = PysonDB(f.strpath)

    assert db.get_by_query(condition) == output


def test_get_by_query_no_matches(tmpdir):
    pass


@pytest.mark.parametrize(
    'condition',
    (
        [1, 2],
        {'age': 4, 'name': 3}
    )
)
def test_get_by_query_type_error(tmpdir, condition):
    f = tmpdir.join('test.json')
    db = PysonDB(f.strpath)

    with pytest.raises(TypeError):
        db.get_by_query(condition)
