import json

from pysondb.db import PysonDB


FINAL_DATA = {
    'version': 2,
    'keys': ['age', 'name'],
    'data': {
        '1': {
            'age': 4,
            'name': 'mathew_first'
        },
        '2': {
            'age': 9,
            'name': 'new_user'
        }
    }
}


def get_nums(n):
    yield str(n)
    yield from get_nums(n + 1)


def test_id_generator_incremental_id(tmpdir):
    f = tmpdir.join('test.json')
    nums = get_nums(1)
    db = PysonDB(f.strpath)
    db.set_id_generator(lambda: next(nums))
    assert db.add_many([
        {'age': 4, 'name': 'mathew_first'},
        {'age': 9, 'name': 'new_user'}
    ], json_response=True) == {'1': {'age': 4, 'name': 'mathew_first'}, '2': {'age': 9, 'name': 'new_user'}}
    assert json.loads(f.read()) == FINAL_DATA
