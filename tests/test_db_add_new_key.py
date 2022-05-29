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


def test_add_new_key(tmpdir):

    DATA_SUCCESS = {
        'version': 2,
        'keys': ['age', 'name', 'place'],
        'data': {
            '2352346': {
                'age': 4,
                'name': 'mathew_first',
                'place': 'GB'
            },
            '1234567': {
                'age': 9,
                'name': 'new_user',
                'place': 'GB'
            }
        }
    }

    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))
    db = PysonDB(f.strpath)
    db.add_new_key('place', 'GB')

    assert json.loads(f.read()) == DATA_SUCCESS


def test_add_new_key_no_default(tmpdir):
    DATA_SUCCESS = {
        'version': 2,
        'keys': ['age', 'name', 'place'],
        'data': {
            '2352346': {
                'age': 4,
                'name': 'mathew_first',
                'place': None
            },
            '1234567': {
                'age': 9,
                'name': 'new_user',
                'place': None
            }
        }
    }

    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))
    db = PysonDB(f.strpath)
    db.add_new_key('place')

    assert json.loads(f.read()) == DATA_SUCCESS


@pytest.mark.parametrize(
    'default',
    (
        (1,),
        type('test', (), {}),
    )
)
def test_add_new_key_invalid_data_type(tmpdir, default):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))
    db = PysonDB(f.strpath)

    with pytest.raises(TypeError):
        db.add_new_key(default)
