import json

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


def test_get_all(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))

    db = PysonDB(f.strpath)
    assert db.get_all() == {
        '2352346': {
            'age': 4,
            'name': 'mathew_first'
        },
        '1234567': {
            'age': 9,
            'name': 'new_user'
        }
    }


def test_get_all_empty_file(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps({'version': 2, 'keys': [], 'data': {}}))

    db = PysonDB(f.strpath)
    assert db.get_all() == {}
