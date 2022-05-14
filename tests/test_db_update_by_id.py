import json

import pytest

from pysondb.db import PysonDB
from pysondb.errors import IdDoesNotExistError
from pysondb.errors import UnknownKeyError


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


def test_update_by_id(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))
    db = PysonDB(f.strpath)

    db.update_by_id('1234567', {'age': 69})
    assert json.loads(f.read()) == {'version': 2, 'keys': ['age', 'name'], 'data': {'2352346': {
        'age': 4, 'name': 'mathew_first'}, '1234567': {'age': 69, 'name': 'new_user'}}}


def test_update_by_id_id_does_not_exists(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))
    db = PysonDB(f.strpath)

    with pytest.raises(IdDoesNotExistError):
        db.update_by_id('23526556', {'age': 69})


def test_update_by_id_unknown_key_error(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))
    db = PysonDB(f.strpath)

    with pytest.raises(UnknownKeyError):
        db.update_by_id('534535', {'place': 'GB'})
