import json
import pytest
from pysondb.db import PysonDB
from pysondb.errors import UnknownKeyError


TEST_DATA = {
    'version': 2,
    'keys': ['age', 'name', 'toy'],
    'data': {
        '2352346': {
            'age': 4,
            'name': 'mathew_first',
            'toy': 'car',
        },
        '1234567': {
            'age': 9,
            'name': 'new_user',
            'toy': 'ball',
        }
    }
}


def test_get_all_select_keys(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))

    db = PysonDB(f.strpath)
    assert db.get_all_select_keys(['age']) == {
        '2352346': {
            'age': 4,
        },
        '1234567': {
            'age': 9,
        }
    }
    assert db.get_all_select_keys(['name', 'toy']) == {
        '2352346': {
            'name': 'mathew_first',
            'toy': 'car',
        },
        '1234567': {
            'name': 'new_user',
            'toy': 'ball',
        }
    }


def test_get_all_select_keys_empty_file(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps({'version': 2, 'keys': [], 'data': {}}))

    db = PysonDB(f.strpath)
    assert db.get_all_select_keys([]) == {}

def test_get_all_select_keys_wrong_key(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))

    db = PysonDB(f.strpath)
    with pytest.raises(UnknownKeyError):
        db.get_all_select_keys(['wrong_key'])
