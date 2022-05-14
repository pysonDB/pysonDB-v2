import json
from pathlib import Path

from pysondb.db import PysonDB


TEST_FINAL_DATA = {
    'version': 2,
    'keys': ['age', 'name'],
    'data': {
        '0': {
            'age': 3,
            'name': 'test'
        }
    }
}


def _new_gen_id(n):
    yield str(n)
    yield from _new_gen_id(n + 1)


def test_autoupdate(tmpdir, mocker):
    f = tmpdir.join('test.json')
    _ids = _new_gen_id(0)
    mocker.patch('pysondb.db.PysonDB._gen_id', wraps=lambda: next(_ids))
    db = PysonDB(f.strpath, auto_update=False)
    db.add({
        'name': 'test', 'age': 3
    })

    assert db.auto_update is False
    assert db._au_memory == TEST_FINAL_DATA
    assert Path(f.strpath).is_file() is False


def test_autoupdate_force_load(tmpdir, mocker):
    f = tmpdir.join('test.json')
    _ids = _new_gen_id(0)
    mocker.patch('pysondb.db.PysonDB._gen_id', wraps=lambda: next(_ids))
    f.write(json.dumps(TEST_FINAL_DATA))
    db = PysonDB(f.strpath, auto_update=False)

    db.force_load()
    assert db.auto_update is False
    assert db._au_memory == TEST_FINAL_DATA


def test_autoupdate_commit(tmpdir, mocker):
    f = tmpdir.join('test.json')
    _ids = _new_gen_id(0)
    mocker.patch('pysondb.db.PysonDB._gen_id', wraps=lambda: next(_ids))
    db = PysonDB(f.strpath, auto_update=False)
    db.add({
        'name': 'test', 'age': 3
    })
    db.commit()

    assert db.auto_update is False
    assert json.loads(f.read()) == TEST_FINAL_DATA


def test_autoupdate_accidental_commit(tmpdir):
    f = tmpdir.join('test.json')
    db = PysonDB(f.strpath)
    db.commit()

    assert db.auto_update is True


def test_autoupdate_accidental_force_load(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_FINAL_DATA))

    db = PysonDB(f.strpath)
    db.force_load()

    assert db.auto_update is True
