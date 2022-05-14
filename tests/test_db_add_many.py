import json

import pytest

from pysondb.db import PysonDB
from pysondb.errors import UnknownKeyError


TEST_DATA = [
    {
        'name': 'ad',
        'age': 19
    },
    {
        'name': 'fredy',
        'age':  69
    },
    {
        'name': 'mathew',
        'age': 69
    }
]

INITIAL_TEST_DATA = {
    'version': 2,
    'keys': ['age', 'name'],
    'data': {
        '2352346': {
            'age': 4,
            'name': 'mathew_first'
        }
    }
}


def _new_gen_id(n):
    yield str(n)
    yield from _new_gen_id(n + 1)


def test_add_many_empty_file(tmpdir, mocker):

    final_data = {
        'version': 2,
        'keys': ['age', 'name'],
        'data': {
            '0': {
                'name': 'ad',
                'age': 19
            },
            '1': {
                'name': 'fredy',
                'age':  69
            },
            '2': {
                'name': 'mathew',
                'age': 69
            }
        }
    }

    _ids = _new_gen_id(0)
    mocker.patch('pysondb.db.PysonDB._gen_id', wraps=lambda: next(_ids))

    f = tmpdir.join('test.json')
    db = PysonDB(f.strpath)
    db.add_many(TEST_DATA)
    assert json.loads(f.read()) == final_data


def test_add_many_non_empty_file(tmpdir, mocker):
    final_data = {
        'version': 2,
        'keys': ['age', 'name'],
        'data': {
            '2352346': {
                'age': 4,
                'name': 'mathew_first'
            },
            '0': {
                'name': 'ad',
                'age': 19
            },
            '1': {
                'name': 'fredy',
                'age':  69
            },
            '2': {
                'name': 'mathew',
                'age': 69
            }
        }
    }

    _ids = _new_gen_id(0)
    mocker.patch('pysondb.db.PysonDB._gen_id', wraps=lambda: next(_ids))
    f = tmpdir.join('test.json')
    f.write(json.dumps(INITIAL_TEST_DATA, indent=4))

    db = PysonDB(f.strpath)
    db.add_many(TEST_DATA)
    assert json.loads(f.read()) == final_data


@pytest.mark.parametrize(
    'data',
    (
        (1,),
        {'a': '3'},
        {1, 2}
    )
)
def test_add_many_type_error_for_list(tmpdir, data):
    f = tmpdir.join('test.json')
    db = PysonDB(f.strpath)

    with pytest.raises(TypeError):
        db.add_many(data)


@pytest.mark.parametrize(
    'data',
    (
        [1, 2],
        ['a', 'b'],
        [[1, 2], [3, 4]],
        [(1, 2), (3)],
        [{1, 2}]
    )
)
def test_add_many_type_error_for_dict_in_list(tmpdir, data):
    f = tmpdir.join('test.json')
    db = PysonDB(f.strpath)

    with pytest.raises(TypeError):
        db.add_many(data)


def test_add_many_unknown_key_error(tmpdir):
    f = tmpdir.join('test.json')
    db = PysonDB(f.strpath)

    with pytest.raises(UnknownKeyError):
        db.add_many(
            [
                {'name': 'ad', 'age': 4},
                {'name': 'test', 'age': 2},
                {'name': 'new_ad', 'age': 5, 'place': 'GB'}
            ]
        )


@pytest.mark.parametrize(
    'data',
    (
        {'name': 'ad', 'age': 4, 'place': 'GB'},
        {'name': 'ad'},
        {'place': 'GB', 'is_alive': True}
    )
)
def test_add_many_unknown_key_error_non_empty_file(tmpdir, data):
    f = tmpdir.join('test.json')
    f.write(json.dumps(INITIAL_TEST_DATA, indent=4))
    db = PysonDB(f.strpath)

    with pytest.raises(UnknownKeyError):
        db.add_many([
            data
        ])


@pytest.mark.parametrize(
    'data',
    (
        '',
        [],
        {}
    )
)
def test_add_many_empty_data(tmpdir, data):
    f = tmpdir.join('test.json')
    db = PysonDB(f.strpath)
    db.add_many(data)


def test_add_many_json_response(tmpdir, mocker):
    response = {
        '0': {
            'name': 'ad',
            'age': 19
        },
        '1': {
            'name': 'fredy',
            'age':  69
        },
        '2': {
            'name': 'mathew',
            'age': 69
        }
    }

    f = tmpdir.join('test.json')
    _ids = _new_gen_id(0)
    mocker.patch('pysondb.db.PysonDB._gen_id', wraps=lambda: next(_ids))

    db = PysonDB(f.strpath)
    assert db.add_many(TEST_DATA, json_response=True) == response
