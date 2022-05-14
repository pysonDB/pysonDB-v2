import json

import pytest

from pysondb.db import PysonDB
from pysondb.errors import IdDoesNotExistError


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


def test_get_by_id(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA, indent=4))
    db = PysonDB(f.strpath)

    assert db.get_by_id('2352346') == {'age': 4, 'name': 'mathew_first'}


def test_get_by_id_id_does_no_exist_error(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA, indent=4))
    db = PysonDB(f.strpath)

    with pytest.raises(IdDoesNotExistError):
        db.get_by_id('1212121')


@pytest.mark.parametrize(
    'data',
    (
        2235235,
        [1, 2],
        (1, 2, 3),
        {1, 2, 3},
        {'2': '4'}
    )
)
def test_get_id_type_error(tmpdir, data):
    f = tmpdir.join('test.json')
    db = PysonDB(f.strpath)

    with pytest.raises(TypeError):
        db.get_by_id(data)
